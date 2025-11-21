import os
import shutil
import subprocess
from datetime import datetime

import pytest
from pyAesCrypt import decryptFile

from autotests.api.api_methods.auth_methods_api import AuthApi
from settings.configs.config_model import ConfigModel
from settings.configs.env_config_loader import EnvConfigLoader
from settings.constants.constants_settings import Paths


def pytest_addoption(parser):
    """
    Добавляет пользовательские опции командной строки для pytest.

    --envFile: путь к .env-файлу, используемому для генерации конфигурации окружения.
    --htmlReport: флаг для генерации HTML-отчёта после выполнения тестов.
    """
    parser.addoption(
        "--envFile",
        action="store",
        help="Путь к .env-файлу для генерации конфигурации окружения."
    )

    parser.addoption(
        "--htmlReport",
        action="store_true",
        default=False,
        help="Сгенерировать HTML-отчёт pytest в директорию logs/reports/html/report_<...>.html"
    )

    parser.addoption(
        "--allureReport",
        action="store_true",
        default=False,
        help="Сгенерировать Allure-отчёт в директорию logs/reports/allure-report"
    )


@pytest.fixture(scope="session")
def config(pytestconfig) -> ConfigModel:
    """
    Сессионная фикстура, загружающая и возвращающая объект конфигурации из .env-файла или .aes-файла.
    """
    env_path = pytestconfig.getoption("envFile")

    # Приводим к абсолютному пути относительно корня проекта
    if not os.path.isabs(env_path):
        project_root = os.path.abspath(os.path.dirname(__file__))
        env_path = os.path.join(project_root, env_path)

    if not os.path.exists(env_path):
        raise FileNotFoundError(f".env file not found: {env_path}")

    # Если это зашифрованный файл
    if env_path.endswith(".aes"):

        decrypted_path = env_path.removesuffix(".aes")
        password = os.getenv("TEST_CONFIG_PASSWORD")
        if not password:
            raise EnvironmentError("Не задан TEST_CONFIG_PASSWORD для расшифровки .aes-файла")

        try:
            decryptFile(env_path, decrypted_path, password, bufferSize=64 * 1024)
        except Exception as e:
            raise RuntimeError(f"Ошибка при расшифровке файла {env_path}: {e}") from e

        env_path = decrypted_path

    config = EnvConfigLoader().load(env_path=env_path)
    return config

@pytest.fixture(scope="session")
def session_token(config: ConfigModel) -> str:
    """
    Фикстура, получения токена.
    """
    auth_api = AuthApi(config)
    response = auth_api.post_auth_token()
    return response.cookies.get("token")


@pytest.hookimpl()
def pytest_sessionfinish(session, exitstatus):
    if session.config.getoption("--allureReport"):
        results_dir = Paths.ALLURE_RESULTS
        report_dir = Paths.ALLURE_REPORT

        if results_dir.exists() and any(results_dir.iterdir()):
            allure_cli = shutil.which("allure")
            if allure_cli:
                try:
                    subprocess.run(
                        [allure_cli, "generate", "--clean", str(results_dir), "-o", str(report_dir)],
                        check=False
                    )
                    print(f"Allure report сгенерирован в: {report_dir}")
                except Exception as e:
                    print(f"Не удалось сгенерировать Allure report: {e}")
            else:
                print(
                    "Allure CLI не найден (команда `allure`). "
                    f"Результаты лежат в {results_dir}. "
                    "Установи Allure CLI, чтобы сгенерировать HTML: "
                    "https://docs.qameta.io/allure/#_get_started"
                )
        else:
            print(f"Папка с результатами Allure пуста: {results_dir} - отчёт не создан.")


def pytest_configure(config):
    """
    Хук инициализации Pytest.
    - при --htmlReport настраивает pytest-html
    - при ALLURE_UI_REPORT_ENABLED=true гарантирует папку для allure-results
    """
    if config.getoption("--htmlReport"):
        os.makedirs("logs/reports/html", exist_ok=True)
        mark_expr = config.option.markexpr or "all"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"report_{mark_expr}_{timestamp}.html"
        config.option.htmlpath = os.path.join("logs", "reports", "html", filename)

    if config.getoption("--allureReport"):
        os.makedirs(Paths.ALLURE_RESULTS, exist_ok=True)
        config.option.allure_report_dir = str(Paths.ALLURE_RESULTS)