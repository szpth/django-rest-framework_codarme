import json
from datetime import datetime

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from agenda.models.agenda import Agendamento


class TestListagemAgendamentos(APITestCase):
    def test_listagem_agendamentos_vazia(self):
        user = User.objects.create(
            email="bob@email.com", username="bob", password="123"
        )
        self.client.force_authenticate(user)
        response = self.client.get(path="/api/agendamentos/?username=bob")
        data = json.loads(response.content)
        assert data == []

    def test_listagem_agendamentos_criados(self):
        user = User.objects.create(
            email="bob@email.com", username="bob", password="123"
        )
        self.client.force_authenticate(user)
        Agendamento.objects.create(
            data_horario=datetime(2022, 4, 26, 11, 30, tzinfo=timezone.utc),
            nome_cliente="Teste",
            email_cliente="teste@teste.com",
            telefone_cliente="(11) 99999-9999",
            prestador=user,
        )
        response = self.client.get(path="/api/agendamentos/?username=bob")
        data = json.loads(response.content)
        assert response.status_code == 200
        assert data[0]["prestador"] == "bob"

    def test_listagem_agendamentos_nao_autenticado(self):
        pass
