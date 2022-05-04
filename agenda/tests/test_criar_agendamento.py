import json
from datetime import datetime
from unittest import mock

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from agenda.models.agenda import Agendamento


class TestCriaAgendamentos(APITestCase):
    def test_cria_agendamento(self):
        User.objects.create(
            email="bob@email.com", username="bob", password="123"
        )
        data = {
            "data_horario": "2022-12-01T11:00:00Z",
            "nome_cliente": "Teste",
            "email_cliente": "teste@teste.com",
            "telefone_cliente": "(11) 99999-9999",
            "prestador": "bob",
        }
        self.client.post(
            path="/api/agendamentos/",
            data=data,
            format="json",
        )
        response = Agendamento.objects.get()
        assert response.data_horario == datetime(
            2022, 12, 1, 11, 0, tzinfo=timezone.utc
        )

    def test_cria_agendamento_no_feriado(self):
        User.objects.create(
            email="bob@email.com", username="bob", password="123"
        )
        data = {
            "data_horario": "2023-12-25T11:00:00Z",
            "nome_cliente": "Teste",
            "email_cliente": "teste@teste.com",
            "telefone_cliente": "(11) 99999-9999",
            "prestador": "bob",
        }
        response = self.client.post(
            path="/api/agendamentos/",
            data=data,
            format="json",
        )
        data = json.loads(response.content)
        json_in = {
            "data_horario": {
                "detail": "Não há horários disponíveis!",
            }
        }
        assert response.status_code == 400
        assert data == json_in

    def test_cria_agendamento_passado(self):
        pass

    def test_cria_agendamento_fora_do_horario(self):
        pass

    def test_cria_agendamento_domingo(self):
        pass
