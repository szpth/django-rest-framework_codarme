import json

from rest_framework.test import APITestCase

# class TestListagemHorarios(APITestCase):
#     @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)
#     def test_listagem_horarios_disponiveis_em_feriados(self, _):
#         response = self.client.get(path="/api/horarios/?data=2022-12-25")
#         data = json.loads(response.content)
#         assert data == []


class TestListagemHorarios(APITestCase):
    def test_listagem_horarios_disponiveis_em_feriados(self):
        response = self.client.get(path="/api/horarios/?data=2022-12-25")
        data = json.loads(response.content)
        assert data == []
