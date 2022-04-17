from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer


# Create your views here.
@api_view(http_method_names=["GET"])
def agendamento_detail(request, uuid):
    obj = get_object_or_404(Agendamento, uuid=uuid)
    serializer = AgendamentoSerializer(obj)

    return JsonResponse(serializer.data)


@api_view(http_method_names=["GET", "POST"])
def agendamento_list(request):
    if request.method == "GET":
        qs = Agendamento.objects.all()
        serializer = AgendamentoSerializer(qs, many=True)

        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        data = request.data
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            if 11 == len(validated_data["telefone_cliente"]):
                telefone_cliente = Agendamento.format_phone(validated_data["telefone_cliente"])
                Agendamento.objects.create(
                    data_horario=validated_data["data_horario"],
                    nome_cliente=validated_data["nome_cliente"],
                    email_cliente=validated_data["email_cliente"],
                    telefone_cliente=telefone_cliente,
                )
                return JsonResponse(serializer.data, status=201)
            else:
                return JsonResponse(
                    {"detail": "Telefone inválido, deve ter DDD e Telefone  (Ex. 11987654321)."}, status=400
                )
        return JsonResponse(serializer.errors, status=400)
