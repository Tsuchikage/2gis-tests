import requests

from settings.configs.config_model import ConfigModel
from settings.api_client.api_client import ApiClient
from settings.report import autotest


class RegionsApi:
    """
    Методы для работы с местами (Regions).
    """

    def __init__(self, config: ConfigModel):
        """
        Инициализирует API-клиент для работы с местами.
        """
        self.api_client = ApiClient(config=config, controller_path="")

    def post_favorite_region(self, data: dict, token: str) -> requests.Response:
        """
        Создаёт избранное место (POST /v1/favorites).

        :param data: словарь с данными избранного места.
        :param token: Сессионный токен, полученный из AuthApi (cookie token).
        :return: Ответ сервера (`requests.Response`) в формате JSON.
        """
        with autotest.step("Создаём избранное место (POST /v1/favorites)"):
            return self.api_client.post(
                "/v1/favorites",
                data=data,
                cookies={"token": token}
            )
