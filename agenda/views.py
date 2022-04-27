from datetime import datetime

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer, PrestadorSerializer
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
    permission_classes = [IsOwnerOrCreateOnly]
    serializer_class = AgendamentoSerializer

    def get_queryset(self):
        confirmado = self.request.query_params.get("confirmado", None)
        if confirmado == "True" or confirmado == "true":
            prestador = self.request.query_params.get("username", None)
            qs_user = Agendamento.objects.filter(
                prestador__username=prestador,
                cancelado=False,
                confirmado=True,
            ).order_by("data_horario")
        elif confirmado == "False" or confirmado == "false":
            prestador = self.request.query_params.get("username", None)
            qs_user = Agendamento.objects.filter(
                prestador__username=prestador,
                cancelado=False,
                confirmado=False,
            ).order_by("data_horario")
        else:
            prestador = self.request.query_params.get("username", None)
            qs_user = Agendamento.objects.filter(
                prestador__username=prestador, cancelado=False
            ).order_by("data_horario")
        return qs_user


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPrestador]
    serializer_class = AgendamentoSerializer
    lookup_field = "uuid"
    queryset = Agendamento.objects.filter(cancelado=False)

    def perform_destroy(self, instance):
        instance.cancelado = True
        instance.confirmado = False
        instance.save()
        return Response(status=204)


class ConfirmaAgendamentoDetail(generics.RetrieveUpdateAPIView):
    permission_classes = [IsPrestador]
    serializer_class = AgendamentoSerializer
    lookup_field = "uuid"
    queryset = Agendamento.objects.filter(confirmado=False)

    def post(self, request, **kwargs):
        username = request.user.username
        Agendamento.objects.filter(
            prestador__username=username, confirmado=False
        ).update(
            cancelado=False,
            confirmado=True,
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
