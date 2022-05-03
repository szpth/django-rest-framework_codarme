import phonenumbers
from django.db import models

from agenda.models.base import StandardModelMixin


class Agendamento(StandardModelMixin):
    NAOCONFIRMADO = "NC"
    CONFIRMADO = "CO"
    EXECUTADO = "EX"
    CANCELADO = "CA"
    ESTADOS = [
        (NAOCONFIRMADO, "Não Confirmado"),
        (CONFIRMADO, "Confirmado"),
        (EXECUTADO, "Executado"),
        (CANCELADO, "Cancelado"),
    ]

    prestador = models.ForeignKey(
        "auth.User",
        related_name="agendamentos",
        on_delete=models.CASCADE,
        verbose_name="Prestador",
    )
    data_horario = models.DateTimeField(
        verbose_name="Horário do agendamento",
    )
    nome_cliente = models.CharField(
        max_length=255,
        verbose_name="Nome do cliente",
    )
    email_cliente = models.EmailField(
        verbose_name="E-Mail",
    )
    telefone_cliente = models.CharField(
        max_length=20,
        verbose_name="Telefone",
    )
    status = models.CharField(
        max_length=2,
        choices=ESTADOS,
        default=NAOCONFIRMADO,
        verbose_name="Status",
    )

    @classmethod
    def to_e164(cls, telefone_cliente):
        """phonenumbers Python Library \n
        Encoding phone to E.164 format \n
        Reference: https://github.com/daviddrysdale/python-phonenumbers"""
        telefone_cliente = phonenumbers.parse(telefone_cliente, "BR")
        format_telefone_cliente = phonenumbers.format_number(
            telefone_cliente,
            phonenumbers.PhoneNumberFormat.E164,
        )
        return format_telefone_cliente
