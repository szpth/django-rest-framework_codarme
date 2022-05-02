import re

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from agenda.models import Agendamento
from agenda.utils import get_hr_disp


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = (
            "uuid",
            "data_horario",
            "nome_cliente",
            "email_cliente",
            "telefone_cliente",
            "prestador",
            "status",
        )

    prestador = serializers.CharField()

    def validate_prestador(self, value):
        try:
            prestador_obj = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {
                    "detail": "Prestador não encontrado! Verifique o nome do prestador.",
                }
            )
        return prestador_obj

    def validate_data_horario(self, value):
        if value.weekday() == 6:
            raise serializers.ValidationError(
                {
                    "detail": "Não é possível agendar no domingo!",
                }
            )

        if get_hr_disp(value) == []:
            raise serializers.ValidationError(
                {
                    "detail": "Não há horários disponíveis!",
                }
            )

        if value < timezone.now():
            raise serializers.ValidationError(
                {
                    "detail": "Agendamento não pode ser feito no passado!",
                }
            )

        if value.weekday() == 5:
            if value.hour < 9 or value.hour >= 13:
                raise serializers.ValidationError(
                    {
                        "detail": "Agendamento fora do horário de funcionamento!",
                    }
                )
        else:
            if value.hour < 9 or value.hour >= 18:
                raise serializers.ValidationError(
                    {
                        "detail": "Agendamento fora do horário de funcionamento!",
                    }
                )

        return value

    def validate_telefone_cliente(self, is_e164: str) -> str:
        """Check if telefone_cliente is E.164 format

        Raises:
            serializers.ValidationError: Return message if is not valid.

        Returns:
            {boolean}: Return a {boolean} if is valid or not.
        """
        is_e164 = Agendamento.to_e164(is_e164)

        if not re.fullmatch(r"^[+][0-9]{13}", is_e164):
            raise serializers.ValidationError(
                "Telefone inválido! Informe um telefone celular com DDD."
            )

        return is_e164


class PrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "agendamentos"]

    agendamentos = AgendamentoSerializer(many=True, read_only=True)
