import json
import logging
from datetime import date, datetime

import requests
from django.conf import settings


def is_feriado(date: date):
    logging.info(f"Querying on BrasilAPI: {date.isoformat()}")
    if settings.TESTING == "True":
        logging.info("Request is not being performed, DEBUG mode active.")
        if date.day == 25 and date.month == 12:
            return True
        return False

    r = requests.get(f"https://brasilapi.com.br/api/feriados/v1/{date.year}")
    if not r.status_code == 200:
        logging.error(
            "Request is not being performed, ERROR when consulting BrasilAPI!"
        )
        return False

    feriados = json.loads(r.text)
    logging.error("Checking if the data entered is a holiday..")
    for feriado in feriados:
        dt_as_str = feriado["date"]
        if datetime.strptime(dt_as_str, "%Y-%m-%d").date() == date:
            logging.error("The given date is a holiday!")
            return True
    logging.error("The given date is not a holiday!")
    return False
