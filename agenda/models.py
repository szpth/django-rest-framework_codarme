from uuid import uuid4

import phonenumbers
from django.db import models


class StandardModelMixin(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, verbose_name="ID"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="Created at"
    )
    updated_at = models.DateTimeField(
        auto_now=True, editable=False, verbose_name="Updated at"
    )

    class Meta:
        abstract = True


class Agendamento(StandardModelMixin):
    prestador = models.ForeignKey(
        "auth.User",
        related_name="agendamentos",
        on_delete=models.CASCADE,
        verbose_name="Prestador",
    )
    data_horario = models.DateTimeField(verbose_name="Horário do agendamento")
    nome_cliente = models.CharField(
        max_length=255, verbose_name="Nome do cliente"
    )
    email_cliente = models.EmailField(verbose_name="E-Mail")
    telefone_cliente = models.CharField(max_length=20, verbose_name="Telefone")
    cancelado = models.BooleanField(default=False, verbose_name="Cancelado")

    @classmethod
    def to_e164(cls, telefone_cliente):
        """phonenumbers Python Library \n
        Enconding phone to E.164 format \n
        Reference: https://github.com/daviddrysdale/python-phonenumbers"""
        telefone_cliente = phonenumbers.parse(telefone_cliente, "BR")
        format_telefone_cliente = phonenumbers.format_number(
            telefone_cliente, phonenumbers.PhoneNumberFormat.E164
        )
        return format_telefone_cliente
