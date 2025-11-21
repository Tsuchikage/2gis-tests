import os
from dotenv import dotenv_values

from settings.configs.config_model import ConfigModel


class EnvConfigLoader:
    """
    Загружает переменные из .env-файла и формирует объект ConfigModel.
    Также экспортирует переменные в окружение.
    """

    def load(self, env_path: str) -> ConfigModel:
        """
        Загружает переменные из указанного .env-файла и возвращает объект ConfigModel.

        :param env_path: Путь к .env-файлу с настройками.
        :return: Объект ConfigModel, содержащий параметры запуска автотестов.
        """
        # Загрузка .env переменных
        values = dotenv_values(env_path)
        for key, value in values.items():
            os.environ[key] = value  # Экспорт в переменные окружения

        # Итоговый объект конфигурации
        return ConfigModel(
            base_url=values.get("BASE_URL")
        )
