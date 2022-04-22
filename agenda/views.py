from datetime import datetime, timedelta

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer


@api_view(http_method_names=["GET", "PATCH", "DELETE"])
def agendamento_detail(request, uuid):
    obj = get_object_or_404(Agendamento, uuid=uuid)
    if request.method == "GET":
        serializer = AgendamentoSerializer(obj)
        return JsonResponse(serializer.data)

    if request.method == "PATCH":
        serializer = AgendamentoSerializer(
            obj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return JsonResponse(serializer.errors, status=400)

    if request.method == "DELETE":
        obj.cancelado = True
        obj.save()
        return Response(status=204)


@api_view(http_method_names=["GET", "POST"])
def agendamento_list(request):
    if request.method == "GET":
        qs = Agendamento.objects.filter(cancelado=False)
        serializer = AgendamentoSerializer(qs, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        data = request.data
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(http_method_names=["GET"])
def horario_list(request):
    if request.method == "GET":
        data = request.query_params.get("data")
        data = datetime.fromisoformat(data).date()
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
        return JsonResponse(horarios, safe=False)
