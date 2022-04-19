from django.contrib import admin

from agenda.models import Agendamento


@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = [
        "uuid",
        "created_at",
        "updated_at",
        "data_horario",
        "nome_cliente",
        "email_cliente",
        "telefone_cliente",
        "cancelado",
    ]

    # define search columns list, then a search box will be added at the top of Department list page.
    search_fields = ["nome_cliente", "email_cliente", "telefone_cliente"]

    # define filter columns list, then a filter widget will be shown at right side of Department list page.
    list_filter = ["data_horario", "cancelado"]
