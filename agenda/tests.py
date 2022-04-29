import json
from datetime import datetime

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
        assert data[0]["data_horario"] == "2022-04-26T11:30:00Z"
        assert data[0]["nome_cliente"] == "Teste"
        assert data[0]["email_cliente"] == "teste@teste.com"
        assert data[0]["telefone_cliente"] == "(11) 99999-9999"
        assert data[0]["prestador"] == "bob"
        assert response.status_code == 200

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
        user = User.objects.create(
            email="bob@email.com", username="bob", password="123"
        )
        self.client.force_authenticate(user)
        agendamento_request_data = {
            "data_horario": "2022-06-15T11:00:00Z",
            "nome_cliente": "Teste",
            "email_cliente": "teste@teste.com",
            "telefone_cliente": "(11) 99999-9999",
            "prestador": "bob",
        }
        response = self.client.post(
            path="/api/agendamentos/",
            data=agendamento_request_data,
            format="json",
        )
        created = Agendamento.objects.get()
        assert response.status_code == 201
        assert created.data_horario == datetime(
            2022, 6, 15, 11, 0, tzinfo=timezone.utc
        )

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
        user_list = self.client.get(path="/api/agendamentos/?username=bob")
        user_data = json.loads(user_list.content)
        uuid = user_data[0]["uuid"]
        response = self.client.get(path=f"/api/agendamentos/{uuid}/")
        uuid = response.data["uuid"]

        qs = Agendamento.objects.get(uuid__exact=uuid)

        obj = Loyalty.objects.filter(
            email_cliente=qs.email_cliente, prestador=qs.prestador
        )

        if obj.exists():
            obj.pontos += 1
            obj.save()
        else:
            Loyalty.objects.create(
                email_cliente=qs.email_cliente, prestador=qs.prestador
            )

        obj2 = Loyalty.objects.get(
            email_cliente=qs.email_cliente, prestador=qs.prestador
        )

        obj.pontos += 1
        obj.save()

        assert obj2.pontos == 2


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
        data = json.loads(response.content)
        assert response.status_code == 403
        assert data == {
            "detail": "Authentication credentials were not provided."
        }

    def test_listagem_prestadores_nao_autorizado(self):
        user = User.objects.create(
            email="bob@email.com", username="bob", password="123"
        )
        self.client.force_authenticate(user)
        response = self.client.get(path="/api/prestadores/")
        data = json.loads(response.content)
        assert response.status_code == 403
        assert data == {
            "detail": "You do not have permission to perform this action."
        }
