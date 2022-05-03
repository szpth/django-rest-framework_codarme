import json
from datetime import date, datetime

import requests
from django.conf import settings


def is_feriado(date: date):
    if settings.DEBUG is True:
        if date.day == 25 and date.month == 12:
            return True
        return False

    r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{date.year}")
    if not r.status_code == 200:
        return False

    feriados = json.loads(r.text)
    for feriado in feriados:
        dt_as_str = feriado["date"]
        if datetime.strptime(dt_as_str, "%Y-%m-%d").date() == date:
            return True
    return False
