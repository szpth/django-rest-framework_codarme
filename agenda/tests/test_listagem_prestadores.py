import json

from django.contrib.auth.models import User
from rest_framework.test import APITestCase


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
