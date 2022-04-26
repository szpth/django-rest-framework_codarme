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


class AgendamentoList(APIView):
    permission_classes = [IsOwnerOrCreateOnly]

    def get(self, request):
        username = self.request.query_params.get("username", None)
        queryset = Agendamento.objects.filter(prestador__username=username)
        serializer = AgendamentoSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data = request.data
        serializer = AgendamentoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=201)
        return JsonResponse(serializer.errors, status=400)


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsPrestador]
    queryset = Agendamento.objects.filter(cancelado=False)
    serializer_class = AgendamentoSerializer
    lookup_field = "uuid"

    def perform_destroy(self, instance):
        instance.cancelado = True
        instance.save()


class HorarioList(APIView):
    permission_classes = [IsReadOnlyAccess]

    def get(self, request):
        data = request.query_params.get("data")
        if not data:
            data = datetime.now().date()
        else:
            data = datetime.fromisoformat(data).date()
        hr_disp = sorted(list(get_hr_disp(data)))
        return JsonResponse(hr_disp, safe=False)


class PrestadorList(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = User.objects.all()
        serializer = PrestadorSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)
