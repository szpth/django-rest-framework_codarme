from django.db import models

from agenda.models.base import StandardModelMixin


class Loyalty(StandardModelMixin):
    email_cliente = models.EmailField(verbose_name="E-Mail")
    prestador = models.ForeignKey(
        "auth.User",
        related_name="loyalty",
        on_delete=models.CASCADE,
        verbose_name="Prestador",
    )
    pontos = models.IntegerField(verbose_name="Fidelidade", default=1)
