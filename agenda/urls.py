from django.urls import include, path

from agenda.views import (
    AgendamentoDetail,
    AgendamentoList,
    ConfirmaAgendamentoDetail,
    EnderecoDetail,
    FinalizaAgendamentoDetail,
    HorarioList,
    PrestadorList,
)

urlpatterns = [
    path("agendamentos/", AgendamentoList.as_view()),
    path("agendamentos/<uuid:uuid>/", AgendamentoDetail.as_view()),
    path(
        "agendamentos/<uuid:uuid>/confirmar/",
        ConfirmaAgendamentoDetail.as_view(),
    ),
    path(
        "agendamentos/<uuid:uuid>/finalizar/",
        FinalizaAgendamentoDetail.as_view(),
    ),
    path("horarios/", HorarioList.as_view()),
    path("prestadores/", PrestadorList.as_view()),
    path("prestadores/endereco/", EnderecoDetail.as_view()),
]
