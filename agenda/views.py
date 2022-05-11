from datetime import datetime

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, permissions, serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from agenda.models.agenda import Agendamento
from agenda.models.loyalty import Loyalty
from agenda.serializers import (
    AgendamentoSerializer,
    EnderecoSerializer,
    PrestadorSerializer,
)
from agenda.utils import get_hr_disp


class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True
        username = request.query_params.get("username", None)
        if request.user.username == username:
            return True
        return False


class IsReadOnlyAccess(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            return True
        return False


class IsPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.prestador == request.user:
            return True
        return False


class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "GET":
            if request.user.is_staff:
                return True
        return False


class AgendamentoList(generics.ListCreateAPIView):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsOwnerOrCreateOnly]

    def get_queryset(self):
        confirmado = self.request.query_params.get("confirmado", None)
        prestador = self.request.query_params.get("username", None)
        if confirmado == "True" or confirmado == "true":
            qs_user = Agendamento.objects.filter(
                prestador__username=prestador,
                status="CO",
            ).order_by(
                "data_horario",
            )
        elif confirmado == "False" or confirmado == "false":
            qs_user = Agendamento.objects.filter(
                prestador__username=prestador,
                status="CA",
            ).order_by(
                "data_horario",
            )
        else:
            qs_user = (
                Agendamento.objects.filter(
                    prestador__username=prestador,
                )
                .exclude(
                    status="CA",
                )
                .order_by(
                    "data_horario",
                )
            )
        return qs_user


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsPrestador]
    lookup_field = "uuid"
    queryset = Agendamento.objects.all()

    def perform_destroy(self, instance):
        if instance.status == "CA":
            raise serializers.ValidationError(
                {
                    "detail": "Agendamento já foi cancelado!",
                }
            )
        elif instance.status == "EX":
            raise serializers.ValidationError(
                {
                    "detail": "Agendamento já foi finalizado!",
                }
            )
        else:
            instance.status = "CA"
            instance.save()
        return Response(status=204)


class ConfirmaAgendamentoDetail(generics.RetrieveAPIView):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsPrestador]
    lookup_field = "uuid"

    def post(self, request, uuid):
        _qs = Agendamento.objects.get(
            uuid=uuid,
        )

        _obj = Agendamento.objects.filter(
            data_horario=_qs.data_horario,
            prestador=_qs.prestador,
            status="CO",
        )

        if _obj.exists():
            raise serializers.ValidationError(
                "Agendamento confirmado já existente para este horário!"
            )
        elif _qs.status == "CA":
            raise serializers.ValidationError(
                "Este agendamento já está cancelado!"
            )
        elif _qs.status == "CO":
            raise serializers.ValidationError(
                "Este agendamento já está confirmado!"
            )
        else:
            _qs.status = "CO"
            _qs.save()

        return Response(status=202)


class FinalizaAgendamentoDetail(generics.UpdateAPIView):
    serializer_class = AgendamentoSerializer
    permission_classes = [IsPrestador]
    lookup_field = "uuid"

    def post(self, request, uuid):
        _qs = Agendamento.objects.get(
            uuid=uuid,
        )

        _obj = Loyalty.objects.filter(
            email_cliente=_qs.email_cliente,
            prestador=_qs.prestador,
        )

        if _qs.status == "EX":
            raise serializers.ValidationError(
                {
                    "detail": "Agendamento já foi finalizado!",
                }
            )
        elif _qs.status == "CA":
            raise serializers.ValidationError(
                {
                    "detail": "Agendamento está cancelado!",
                },
            )
        elif _qs.status == "NC":
            raise serializers.ValidationError(
                {
                    "detail": "Agendamento ainda não foi confirmado!",
                }
            )
        else:
            if _qs.status == "CO":
                _qs.status = "EX"
                _qs.save()
                if _obj.exists():
                    _obj = _obj[0]
                    _obj.pontos += 1
                    _obj.save()
                else:
                    Loyalty.objects.create(
                        email_cliente=_qs.email_cliente,
                        prestador=_qs.prestador,
                    )

        return Response(status=202)


class HorarioList(APIView):
    permission_classes = [IsReadOnlyAccess]

    def get(self, request):
        data = request.query_params.get("data")
        if not data:
            data = datetime.now().date()
        else:
            data = datetime.fromisoformat(data).date()
        hr_disp = sorted(list(get_hr_disp(data)))
        return JsonResponse(data=hr_disp, safe=False)


class PrestadorList(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = PrestadorSerializer

    def get_queryset(self):
        qs_prestador = User.objects.all()
        return qs_prestador


class EnderecoDetail(generics.CreateAPIView):
    serializer_class = EnderecoSerializer
    permission_classes = [IsPrestador]


@api_view(http_method_names=["GET"])
def healthcheck(request):
    return Response({"status": "OK"}, status=200)
