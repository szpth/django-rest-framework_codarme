from django.contrib import admin

from agenda.models.agenda import Agendamento
from agenda.models.loyalty import Loyalty


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "created_at",
        "updated_at",
        "prestador",
        "data_horario",
        "nome_cliente",
        "email_cliente",
        "telefone_cliente",
        "status",
    ]

    search_fields = [
        "nome_cliente",
        "email_cliente",
        "telefone_cliente",
        "prestador",
    ]

    list_filter = [
        "data_horario",
        "status",
    ]


@admin.register(Loyalty)
class LoyaltyAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "created_at",
        "updated_at",
        "email_cliente",
        "prestador",
        "pontos",
    ]

    search_fields = [
        "nome_cliente",
    ]

    list_filter = [
        "prestador",
    ]
