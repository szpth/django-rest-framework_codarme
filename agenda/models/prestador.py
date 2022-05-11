from django.db import models

from agenda.models.base import StandardModelMixin


class Endereco(StandardModelMixin):
    prestador = models.ForeignKey(
        "auth.User",
        related_name="endereco",
        on_delete=models.CASCADE,
        verbose_name="Prestador",
    )
    cep = models.CharField("CEP", max_length=12)
    estado = models.CharField("Estado", max_length=2)
    cidade = models.CharField("Cidade", max_length=50)
    bairro = models.CharField("Bairro", max_length=50)
    rua = models.CharField("Rua", max_length=50)
    complemento = models.CharField(
        "Complemento", max_length=50, blank=True, null=True
    )
