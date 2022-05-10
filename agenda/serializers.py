import logging
import re

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers

from agenda.libs.brasil_api import get_cep
from agenda.models.agenda import Agendamento
from agenda.models.prestador import Endereco

# from agenda.models.prestador import Endereco
from agenda.utils import get_hr_disp


class AgendamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agendamento
        fields = (
            "uuid",
            "data_horario",
            "nome_cliente",
            "email_cliente",
            "telefone_cliente",
            "prestador",
            "status",
        )

    prestador = serializers.CharField()

    def validate_prestador(self, prestador):
        try:
            logging.info(f'Try to find "{prestador}" if exists..')
            prestador_obj = User.objects.get(username=prestador)
        except User.DoesNotExist:
            logging.error(f'Provider not found: "{prestador}')
            raise serializers.ValidationError(
                {
                    "detail": "Provider not found! Check the provider's name.",
                }
            )
        return prestador_obj

    def validate_data_horario(self, value):
        if value.weekday() == 6:
            raise serializers.ValidationError(
                {
                    "detail": "It is not possible to schedule on Sunday!",
                }
            )

        if get_hr_disp(value) == []:
            raise serializers.ValidationError(
                {
                    "detail": "No times available!",
                }
            )

        if value < timezone.now():
            raise serializers.ValidationError(
                {
                    "detail": "Scheduling cannot be done in the past!",
                }
            )

        if value.weekday() == 5:
            if value.hour < 9 or value.hour >= 13:
                raise serializers.ValidationError(
                    {
                        "detail": "Scheduling outside opening hours!",
                    }
                )
        else:
            if value.hour < 9 or value.hour >= 18:
                raise serializers.ValidationError(
                    {
                        "detail": "Scheduling outside opening hours!",
                    }
                )

        return value

    def validate_telefone_cliente(self, is_e164: str) -> str:
        """Check if telefone_cliente is E.164 format

        Raises:
            serializers.ValidationError: Return message if is not valid.

        Returns:
            {boolean}: Return a {boolean} if is valid or not.
        """
        is_e164 = Agendamento.to_e164(is_e164)

        if not re.fullmatch(r"^[+][0-9]{13}", is_e164):
            raise serializers.ValidationError(
                "Invalid phone! Inform a cell phone with area code."
            )

        return is_e164


class PrestadorSerializer(serializers.ModelSerializer):
    agendamentos = AgendamentoSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "agendamentos",
        ]


class EnderecoSerializer(serializers.ModelSerializer):
    prestador = serializers.CharField()
    cep = serializers.CharField()
    estado = serializers.CharField(default="")
    cidade = serializers.CharField(default="")
    bairro = serializers.CharField(default="")
    rua = serializers.CharField(default="")
    complemento = serializers.CharField(default="")

    class Meta:
        model = Endereco
        fields = [
            "prestador",
            "cep",
            "estado",
            "cidade",
            "bairro",
            "rua",
            "complemento",
        ]

    def validate_prestador(self, prestador):
        try:
            logging.info(f'Try to find if "{prestador}" exists..')
            prestador_obj = User.objects.get(username=prestador)
            logging.info(f'Provider "{prestador}" exists!')
        except User.DoesNotExist:
            logging.error(f'Provider not found: "{prestador}')
            raise serializers.ValidationError(
                {
                    "detail": "Provider not found! Check the provider's name.",
                }
            )

        try:
            logging.info(
                f'Try to find if "{prestador}" have already adress registered..'
            )
            Endereco.objects.get(prestador__username=prestador)
            logging.error(
                f'Provider "{prestador}" have already adress registered...'
            )
            raise serializers.ValidationError(
                {
                    "detail": "Provider already have adress, try to update existing information!",
                }
            )
        except Endereco.DoesNotExist:
            logging.info(f'Provider "{prestador}" validated!')
            return prestador_obj

    def validate_cep(self, cep_obj):
        if cep_obj == "":
            raise serializers.ValidationError(
                "The zip code needs to be informed!"
            )

        logging.info(f'Verify zip code: "{cep_obj}"')
        if len(cep_obj) > 8:
            cep_obj = cep_obj.replace("-", "")
            cep_obj = cep_obj.replace(".", "")
            cep_obj = cep_obj.replace(" ", "")

        logging.info(f'"Verify if "{cep_obj}" have more than 8 digits!')
        if re.fullmatch(r"^[0-9]{8}", cep_obj):
            logging.info(cep_obj + " Validated!")
            zip_code = get_cep(cep_obj)
            if not zip_code:
                raise serializers.ValidationError(
                    {
                        "detail": "Invalid zip code! Please enter a valid zip code! eg. 01234567",
                    }
                )
            return cep_obj
        else:
            logging.error(f'Invalid zip code: "{cep_obj}"')
            raise serializers.ValidationError(
                {
                    "detail": "Invalid zip code! Please enter a valid zip code! eg. 01234567",
                }
            )

    def validate_estado(self, estado):
        return estado

    def validate_cidade(self, cidade):
        return cidade

    def validate_bairro(self, bairro):
        return bairro

    def validate_rua(self, rua):
        return rua

    def validate_complemento(self, complemento):
        return complemento

    def validate(self, attrs):
        cep = attrs.get("cep", None)
        state = attrs.get("estado", None)
        city = attrs.get("cidade", None)
        district = attrs.get("bairro", None)
        street = attrs.get("rua", None)

        validation = get_cep(cep)
        validation_state = validation["state"]
        validation_city = validation["city"]
        validation_neighborhood = validation["neighborhood"]
        validation_street = validation["street"]

        if state == "" and city == "" and district == "" and street == "":
            attrs["estado"] = validation_state
            attrs["cidade"] = validation_city
            attrs["bairro"] = validation_neighborhood
            attrs["rua"] = validation_street

        return attrs

    def create(self, validated_data):
        return Endereco.objects.create(**validated_data)

    # logging.info(f'Try to find if "{prestador}" exists..')
    # print(get_cep(cep_obj))

    # {
    #     "cep": "09070250",
    #     "state": "SP",
    #     "city": "Santo André",
    #     "neighborhood": "Campestre",
    #     "street": "Rua João Ribeiro",
    #     "service": "correios",
    # }
