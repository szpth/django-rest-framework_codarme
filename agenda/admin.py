from django.contrib import admin

from agenda.models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "created_at",
        "updated_at",
        "prestador_id",
        "data_horario",
        "nome_cliente",
        "email_cliente",
        "telefone_cliente",
        "cancelado",
        "confirmado",
    ]

    search_fields = [
        "nome_cliente",
        "email_cliente",
        "telefone_cliente",
        "prestador_id",
    ]

    list_filter = [
        "data_horario",
        "cancelado",
        "confirmado",
    ]
