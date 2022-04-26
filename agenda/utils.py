from datetime import datetime, timedelta, timezone

from django.http import JsonResponse

from agenda.models import Agendamento


def get_hr_disp(data) -> list:
    """
    Retorna uma lista de horários disponíveis para agendamento.
    """
    dt_tz = datetime(data.year, data.month, data.day, tzinfo=timezone.utc)
    filter = list(
        Agendamento.objects.filter(data_horario__date=dt_tz).filter(
            cancelado=False
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
