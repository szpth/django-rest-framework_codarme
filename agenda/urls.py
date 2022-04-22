from django.urls import path

from agenda.views import agendamento_detail, agendamento_list, horario_list

urlpatterns = [
    path("agendamentos/", agendamento_list),
    path("agendamentos/<uuid:uuid>/", agendamento_detail),
    path("horarios/", horario_list),
]
