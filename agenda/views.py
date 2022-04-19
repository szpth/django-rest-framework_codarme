from django.http import JsonResponse
from django.shortcuts import get_object_or_404
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
            try:
                serializer.save()
                return Response(status=201)
            except AssertionError:
                return JsonResponse(
                    {"detail": "Informe um telefone celular válido com DDD."},
                    status=400,
                )

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
            try:
                serializer.save()
                return Response(status=201)
            except AssertionError:
                return JsonResponse(
                    {"detail": "Informe um telefone celular válido com DDD."},
                    status=400,
                )
        return JsonResponse(serializer.errors, status=400)
