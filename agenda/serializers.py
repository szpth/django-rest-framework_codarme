import re

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from agenda.models import Agendamento


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

    def validate_prestador(self, username):
        try:
            prestador_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "Prestador não encontrado! Verifique o nome do prestador."
            )
        return prestador_obj

    def validate_data_horario(
        self, data_horario: timezone.datetime
    ) -> timezone.datetime:
        """
        Check if data_horario is in the past
        """
        if data_horario < timezone.now():
            raise serializers.ValidationError(
                "Agendamento não pode ser feito no passado!"
            )

        if data_horario.weekday() == 5:
            if data_horario.hour < 9 or data_horario.hour >= 13:
                raise serializers.ValidationError(
                    "Agendamento fora do horário de funcionamento!"
                )
        else:
            if data_horario.hour < 9 or data_horario.hour >= 18:
                raise serializers.ValidationError(
                    "Agendamento fora do horário de funcionamento!"
                )

        if data_horario.weekday() == 6:
            raise serializers.ValidationError(
                "Não é possível agendar no domingo!"
            )

        filter = Agendamento.objects.filter(data_horario=data_horario).exclude(
            status="CA",
        )

        if filter.exists():
            raise serializers.ValidationError(
                "Agendamento já existente para este horário!"
            )

        return data_horario

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
