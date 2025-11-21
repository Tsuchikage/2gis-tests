import json

import requests

from settings.configs.config_model import ConfigModel
from settings.utils import get_controller_url


class ApiClient:
    """
    Универсальный REST API клиент.

    Предназначен для отправки HTTP-запросов к целевому сервису.
    """

    def __init__(self, config: ConfigModel, controller_path: str):
        """
        Инициализация клиента для заданного сервиса.

        :param config: Конфигурационная модель, содержащая параметры окружения.
        :param controller_path: Название контроллера (часть пути до сервиса).
        """
        self.__config = config

        self.controller_path = controller_path
        self.base_url = get_controller_url(name=controller_path, config=config)

    def _send_request(
        self,
        method: str,
        endpoint_path: str,
        params: dict = None,
        headers: dict = None,
        json_data: json = None,
        data: dict = None,
        cookies: dict = None,
        files: dict = None
    ) -> requests.Response:
        """
        Внутренний метод отправки HTTP-запроса и записи покрытия, если включено.

        :param method: HTTP-метод (GET, POST, PUT, DELETE, PATCH).
        :param endpoint_path: Относительный путь эндпоинта (добавляется к base_url).
        :param params: Query-параметры запроса.
        :param headers: Заголовки запроса.
        :param json_data: JSON-данные в теле запроса.
        :param data: Form-данные в теле запроса.
        :param cookies: Cookie-параметры запроса.
        :param files: Файлы, передаваемые в запросе (multipart/form-data).
        :return: Ответ от сервера в виде `requests.Response`.
        """

        if headers is None:
            headers = {
                'Accept': 'application/json'
            }

        with requests.sessions.Session() as session:
            response = session.request(
                method=method,
                url=f"{self.base_url}{endpoint_path}",
                headers=headers,
                params=params,
                json=json_data,
                data=data,
                files=files,
                cookies=cookies,
                timeout=20
            )

        return response

    def get(self, path: str, **kwargs) -> requests.Response:
        """
        Выполняет GET-запрос к указанному пути.

        :param path: Относительный путь до эндпоинта.
        :param kwargs: Дополнительные параметры запроса (params, headers и т.д.).
        :return: Ответ от сервера.
        """
        return self._send_request(method="GET", endpoint_path=path, **kwargs)

    def post(self, path: str, **kwargs) -> requests.Response:
        """
        Выполняет POST-запрос к указанному пути.

        :param path: Относительный путь до эндпоинта.
        :param kwargs: Дополнительные параметры запроса (headers, json_data и т.д.).
        :return: Ответ от сервера.
        """
        return self._send_request(method="POST", endpoint_path=path, **kwargs)

    def put(self, path: str, **kwargs) -> requests.Response:
        """
        Выполняет PUT-запрос к указанному пути.

        :param path: Относительный путь до эндпоинта.
        :param kwargs: Дополнительные параметры запроса.
        :return: Ответ от сервера.
        """
        return self._send_request(method="PUT", endpoint_path=path, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        """
        Выполняет DELETE-запрос к указанному пути.

        :param path: Относительный путь до эндпоинта.
        :param kwargs: Дополнительные параметры запроса.
        :return: Ответ от сервера.
        """
        return self._send_request(method="DELETE", endpoint_path=path, **kwargs)

    def patch(self, path: str, **kwargs) -> requests.Response:
        """
        Выполняет PATCH-запрос к указанному пути.

        :param path: Относительный путь до эндпоинта.
        :param kwargs: Дополнительные параметры запроса.
        :return: Ответ от сервера.
        """
        return self._send_request(method="PATCH", endpoint_path=path, **kwargs)
