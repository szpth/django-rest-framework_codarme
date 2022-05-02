import json
from datetime import datetime
from unittest import mock

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.test import APITestCase

from agenda.models import Agendamento, Loyalty


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


class TestEditaAgendamento(APITestCase):
    def test_edita_agendamento_autenticado(self):
        pass

    def test_edita_agendamento_nao_autenticado(self):
        pass


class TestCancelaAgendamento(APITestCase):
    def test_cancela_agendamento_autenticado(self):
        pass

    def test_cancela_agendamento_nao_autenticado(self):
        pass


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

    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)
    def test_cria_agendamento_no_feriado(self, _):
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


class TestDetalhaAgendamento(APITestCase):
    def test_detalhamento_de_agendamento_autenticado(self):
        user = User.objects.create(
            email="bob@email.com", username="bob", password="123"
        )
        self.client.force_authenticate(user)
        data = {
            "data_horario": "2022-06-15T11:30:00Z",
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
        user_list = self.client.get(path="/api/agendamentos/?username=bob")
        user_data = json.loads(user_list.content)
        uuid = user_data[0]["uuid"]
        response = self.client.get(path=f"/api/agendamentos/{uuid}/")
        assert response.status_code == 200

    def test_detalhamento_de_agendamento_nao_autenticado(self):
        User.objects.create_user(
            email="bob@email.com", username="bob", password="123"
        )
        self.client.login(username="bob", password="123")
        data = {
            "data_horario": "2022-06-15T11:30:00Z",
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
        user_list = self.client.get(
            path=f"/api/agendamentos/?username={data['prestador']}"
        )
        user_data = json.loads(user_list.content)
        uuid = user_data[0]["uuid"]
        self.client.logout()
        response = self.client.get(path=f"/api/agendamentos/{uuid}/")
        assert response.status_code == 403

    def test_detalhamento_de_agendamento_finalizar(self):
        user = User.objects.create(
            email="bob@email.com", username="bob", password="123"
        )
        self.client.force_authenticate(user)
        data = {
            "data_horario": "2022-06-15T11:30:00Z",
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

        _obj = Loyalty.objects.filter(
            email_cliente=data["email_cliente"], prestador=user
        )

        if _obj.exists():
            _obj = _obj[0]
            _obj.pontos += 1
            _obj.save()
        else:
            Loyalty.objects.create(
                email_cliente=data["email_cliente"],
                prestador=user,
            )

        assert _obj[0].pontos == 1


class TestListagemPrestadores(APITestCase):
    def test_listagem_prestadores_autenticado(self):
        user = User.objects.create_superuser(
            email="bob@email.com", username="bob", password="123"
        )
        self.client.force_authenticate(user)
        data = {
            "data_horario": "2022-06-15T11:30:00Z",
            "nome_cliente": "Teste",
            "email_cliente": "teste@teste.com",
            "telefone_cliente": "(11) 99999-9999",
            "prestador": "bob",
        }
        request = self.client.post(
            path="/api/agendamentos/",
            data=data,
            format="json",
        )
        response = self.client.get(path="/api/prestadores/")
        assert request.status_code == 201
        assert response.status_code == 200

    def test_listagem_prestadores_nao_autenticado(self):
        response = self.client.get(path="/api/prestadores/")
        json_in = {
            "detail": "Authentication credentials were not provided.",
        }
        data = json.loads(response.content)
        assert response.status_code == 403
        assert data == json_in

    def test_listagem_prestadores_nao_autorizado(self):
        user = User.objects.create(
            email="bob@email.com", username="bob", password="123"
        )
        self.client.force_authenticate(user)
        response = self.client.get(path="/api/prestadores/")
        json_in = {
            "detail": "You do not have permission to perform this action."
        }
        data = json.loads(response.content)
        assert response.status_code, 403
        assert data == json_in


class TestListagemHorarios(APITestCase):
    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)
    def test_listagem_horarios_disponiveis_em_feriados(self, _):
        response = self.client.get(path="/api/horarios/?data=2022-12-25")
        data = json.loads(response.content)
        assert data == []
