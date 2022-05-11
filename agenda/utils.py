from datetime import date, datetime, timedelta, timezone
from typing import Iterable

from django.http import JsonResponse

from agenda.libs import brasil_api
from agenda.models.agenda import Agendamento


def get_hr_disp(data: date) -> Iterable[datetime]:
    """
    Returns a list of available times for scheduling.

    Raises:
        JsonResponse: Returns a message if it is pointed to a Sunday or Holiday.

    Returns:
        {list}: Return a {list} with avaliable schedule.
    """
    if brasil_api.is_feriado(data):
        return []

    dt_tz = datetime(data.year, data.month, data.day, tzinfo=timezone.utc)
    filter = list(
        Agendamento.objects.filter(data_horario__date=dt_tz,).exclude(
            status="CO",
        )
    )

    horarios = []

    if dt_tz.weekday() == 6:
        return JsonResponse(
            {"response": "Não é possível agendar no domingo!"}, status=400
        )
    dt_hr_ini = datetime(
        data.year, data.month, data.day, hour=9, tzinfo=timezone.utc
    )
    if dt_tz.weekday() == 5:
        dt_hr_fim = datetime(
            data.year, data.month, data.day, hour=13, tzinfo=timezone.utc
        )
    else:
        dt_hr_fim = datetime(
            data.year, data.month, data.day, hour=18, tzinfo=timezone.utc
        )
        int_ini = datetime(
            data.year, data.month, data.day, hour=12, tzinfo=timezone.utc
        )
        int_fim = datetime(
            data.year, data.month, data.day, hour=13, tzinfo=timezone.utc
        )
    delta = timedelta(minutes=30)
    agendados = [x.data_horario for x in filter]
    while dt_hr_ini < dt_hr_fim:
        if dt_tz.weekday() == 5:
            if dt_hr_ini not in agendados:
                horarios.append(dt_hr_ini.isoformat())
        else:
            if (dt_hr_ini not in agendados) and (
                dt_hr_ini < int_ini or dt_hr_ini >= int_fim
            ):
                horarios.append(dt_hr_ini.isoformat())
        dt_hr_ini += delta
    return horarios
