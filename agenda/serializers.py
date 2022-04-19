import re

from django.utils import timezone
from rest_framework import serializers

from agenda.models import Agendamento


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = (
            "data_horario",
            "nome_cliente",
            "email_cliente",
            "telefone_cliente",
        )

    def validate_data_horario(
        self, data_horario: timezone.datetime
    ) -> timezone.datetime:
        """Check if data_horario is in the past"""
        if data_horario < timezone.now():
            raise serializers.ValidationError(
                "Agendamento não pode ser feito no passado!"
            )

        if data_horario.hour < 9 or data_horario.hour >= 18:
            raise serializers.ValidationError(
                "Agendamento não pode ser feito fora do horário de funcionamento!"
            )

        if data_horario.weekday() == 6:
            raise serializers.ValidationError(
                "Não é possível agendar no domingo!"
            )

        filter = Agendamento.objects.filter(data_horario=data_horario).filter(
            cancelado=False
        )

        if filter.exists():
            raise serializers.ValidationError(
                "Agendamento já existente para este horário!"
            )

        return data_horario

    def validate_telefone_cliente(self, is_e164: str) -> str:
        """Check if telefone_cliente is E.164 format"""
        is_e164 = Agendamento.to_e164(is_e164)

        if not re.fullmatch(r"^[+][0-9]{13}", is_e164):
            raise serializers.ValidationError(
                "Telefone inválido, informe um telefone celular com DDD."
            )

        return is_e164
