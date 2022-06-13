import csv
from io import StringIO

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from agenda.serializers import PrestadorSerializer
from tamarcado.celery import app


@app.task
def gera_relatorio_prestadores():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "uuid",
            "data_horario",
            "nome_cliente",
            "email_cliente",
            "telefone_cliente",
            "prestador",
            "status",
        ]
    )

    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)

    for prestador in serializer.data:
        agendamentos = prestador["agendamentos"]
        for agendamento in agendamentos:
            writer.writerow(
                [
                    agendamento["uuid"],
                    agendamento["data_horario"],
                    agendamento["nome_cliente"],
                    agendamento["email_cliente"],
                    agendamento["telefone_cliente"],
                    agendamento["prestador"],
                    agendamento["status"],
                ]
            )

    email = EmailMessage(
        "tamarcado - Relatório de prestadores",
        "Em anexo o relatório solicitado.",
        "from@example.com",
        ["to@example.com"],
    )
    email.attach(
        "relatorio.csv",
        output.getvalue(),
        "text/csv",
    )
    email.send()
