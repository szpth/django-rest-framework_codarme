from uuid import uuid4

import phonenumbers
from django.db import models


# Create your models here.
class StandardModelMixin(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False, verbose_name="ID")
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, editable=False, verbose_name="Updated at")

    class Meta:
        abstract = True


class Agendamento(StandardModelMixin):
    data_horario = models.DateTimeField(verbose_name="Horário do agendamento")
    nome_cliente = models.CharField(max_length=255, verbose_name="Nome do cliente")
    email_cliente = models.EmailField(verbose_name="E-Mail")
    telefone_cliente = models.CharField(max_length=20, verbose_name="Telefone")

    @classmethod
    def format_phone(cls, telefone_cliente):
        telefone_cliente = phonenumbers.parse(telefone_cliente, "BR")
        format_telefone_cliente = phonenumbers.format_number(telefone_cliente, phonenumbers.PhoneNumberFormat.E164)
        return format_telefone_cliente
