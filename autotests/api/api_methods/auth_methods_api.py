import requests

from settings.configs.config_model import ConfigModel
from settings.api_client.api_client import ApiClient
from settings.report import autotest


class AuthApi:
    """
    Методы для работы с сессионным токеном сервиса 2GIS Regions.
    """

    def __init__(self, config: ConfigModel):
        """
        Инициализирует API-клиент для работы с Tokens.
        """
        self.api_client = ApiClient(config=config, controller_path="")

    def post_auth_token(self) -> requests.Response:
        """
        Выполняет запрос получения сессионного токена (POST /v1/auth/tokens).

        :return: Возвращает токен.
        """
        with autotest.step("Получаем сессионный токен (POST /v1/auth/tokens)"):
            response = self.api_client.post("/v1/auth/tokens")
        return response
