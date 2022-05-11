import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from agenda.models.loyalty import Loyalty


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
