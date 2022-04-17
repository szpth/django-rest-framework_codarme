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
    data_horario = models.DateTimeField()
    nome_cliente = models.CharField(max_length=255)
    email_cliente = models.EmailField()
    telefone_cliente = models.CharField(max_length=20)

    @classmethod
    def criar_agendamento(cls, telefone_cliente):
        telefone_cliente = phonenumbers.parse(telefone_cliente, "BR")
        format_telefone_cliente = phonenumbers.format_number(telefone_cliente, phonenumbers.PhoneNumberFormat.E164)
        agendamento = Agendamento(telefone_cliente=format_telefone_cliente)
        agendamento.save()
        return
