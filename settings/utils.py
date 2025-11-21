import os
from datetime import datetime, timedelta
from urllib.parse import urljoin
import random
import string
import uuid
import requests

from settings.assertions.custom_assertions import assert_equal


def check_response_status(response: requests.Response, expected_status: int):
    """
    Проверяет, что статус-код HTTP-ответа соответствует ожидаемому, и в случае ошибки выводит подробную информацию.

    :param response: Объект HTTP-ответа.
    :param expected_status: Ожидаемый HTTP статус-код.
    :raises AssertionError: Если фактический статус не совпадает с ожидаемым.
    """
    actual_status = response.status_code
    request_url = response.request.url if response.request else "unknown"

    error_message = (
        f"Ошибка статуса ответа:\n"
        f"Ожидался статус: {expected_status}, фактически получен: {actual_status}\n"
        f"URL запроса: {request_url}\n"
        f"Тело ответа: {response.text}"
    )

    assert_equal(actual_status, expected_status, error_message)


def get_controller_url(config, name: str) -> str:
    """
    Формирует URL-адрес сервиса на основе базового URL из конфигурации и имени сервиса.

    :param config: Объект конфигурации тестов, содержащий base_url.
    :param name: Название сервиса.
    :return: Полный URL-адрес сервиса.
    """
    base_url = config.base_url
    if not base_url.endswith('/'):
        base_url += '/'
    return urljoin(base_url, name)


def verify_data(
    actual_data,
    expected_data,
    verified_fields: list = None,
    unverified_fields: list = None,
    msg_option: str = ""
):
    """
    Проверяет, что фактические данные соответствуют ожидаемым. Поддерживаются словари и списки.

    :param actual_data: Фактические данные (dict или list).
    :param expected_data: Ожидаемые данные (dict или list).
    :param verified_fields: Список ключей, которые необходимо проверить в словаре (по умолчанию None).
    :param unverified_fields: Список ключей, которые нужно исключить из проверки в словаре (по умолчанию None).
    :param msg_option: Дополнительное сообщение для контекста ошибки (по умолчанию пустая строка).
    :raises AssertionError: Если данные не совпадают.
    :raises TypeError: Если типы данных не поддерживаются или не совпадают.
    """
    if isinstance(expected_data, dict) and isinstance(actual_data, dict):
        verified_keys = expected_data.keys()
        if verified_fields is not None:
            verified_keys = verified_fields
        elif unverified_fields is not None:
            verified_keys = set(expected_data.keys()) - set(unverified_fields)

        for key in verified_keys:
            actual_value = actual_data.get(key)
            expected_value = expected_data.get(key)
            assert_equal(
                actual_value,
                expected_value,
                f"Ошибка! Несовпадение в поле '{key}' {msg_option}.\n"
                f"Фактическое значение = '{actual_value}', Ожидаемое значение = '{expected_value}'."
            )

    elif isinstance(expected_data, list) and isinstance(actual_data, list):
        assert_equal(
            len(actual_data),
            len(expected_data),
            f"Ошибка! Несовпадение длины списка {msg_option}.\n"
            f"Фактическая длина = {len(actual_data)}, Ожидаемая длина = {len(expected_data)}."
        )

        for index, (actual_item, expected_item) in enumerate(zip(actual_data, expected_data)):
            assert_equal(
                actual_item,
                expected_item,
                f"Ошибка! Несовпадение элемента списка по индексу {index} {msg_option}.\n"
                f"Фактический элемент = {actual_item}, Ожидаемый элемент = {expected_item}."
            )

    else:
        raise TypeError(
            f"Неподдерживаемые типы данных для проверки {msg_option}.\n"
            f"Фактический тип = {type(actual_data)}, Ожидаемый тип = {type(expected_data)}."
        )


def get_current_test_name() -> str | None:
    """
    Получает имя текущего выполняемого теста (если тест уже запущен).

    :return: Имя теста в виде строки или None, если тест ещё не запущен.
    """
    if os.environ.get('PYTEST_CURRENT_TEST') is not None:
        return os.environ.get('PYTEST_CURRENT_TEST').split(':')[-1].split(' ')[0]
    return None


def str2bool(val: str | None) -> bool:
    """
    Преобразует строку в булево значение. Поддерживаются 'true', '1', 'yes' (без учёта регистра).

    :param val: Строка, которую нужно преобразовать.
    :return: True, если значение соответствует одному из допустимых истинных значений, иначе False.
    """
    if isinstance(val, bool):
        return val
    return str(val).strip().lower() in ("true", "1", "yes", "y", "on")


class Randomizer:
    """
    Утилитный класс для генерации случайных чисел, строк и UUID.
    """

    @staticmethod
    def int_between(low: int = 0, high: int = 1_000_000) -> int:
        """
        Генерирует случайное целое число в заданном диапазоне.

        :param low: Минимальное возможное значение (включительно).
        :param high: Максимальное возможное значение (включительно).
        :return: Случайное целое число.
        """
        return random.randint(low, high)

    @staticmethod
    def float_between(
        low: float | int = 0.0,
        high: float | int = 1_000_000.0,
        precision: int | None = None
    ) -> float:
        """
        Генерирует случайное число с плавающей точкой в указанном диапазоне.

        :param low: Нижняя граница.
        :param high: Верхняя граница.
        :param precision: Количество знаков после запятой (если требуется округление).
        :return: Случайное число float.
        """
        result = random.uniform(low, high)
        return round(result, precision) if precision is not None else result

    @staticmethod
    def pick_random(one_of: list | str | tuple) -> any:
        """
        Возвращает случайный элемент из заданной последовательности.

        :param one_of: Список, строка или кортеж, из которого нужно выбрать элемент.
        :return: Один случайный элемент.
        """
        if not one_of:
            raise ValueError("Последовательность пуста - нечего выбирать.")
        return random.choice(one_of)

    @staticmethod
    def random_string(size: int) -> str:
        """
        Формирует случайную строку из букв латиницы и цифр.

        :param size: Длина результирующей строки.
        :return: Случайная строка.
        """
        alphabet = string.ascii_letters + string.digits
        return ''.join(Randomizer.pick_random(alphabet) for _ in range(size))

    @staticmethod
    def uuid() -> str:
        """
        Возвращает новый уникальный идентификатор в формате UUID4.

        :return: Строка с UUID.
        """
        return str(uuid.uuid4())

    @staticmethod
    def random_birthday(start_year: int = 1990, end_year: int = 2005) -> str:
        """
        Генерирует случайную дату рождения в формате 'YYYY-MM-DD' с ведущими нулями.

        :param start_year: Минимальный год (включительно).
        :param end_year: Максимальный год (включительно).
        :return: Случайная дата в формате 'YYYY-MM-DD'.
        """
        # Начальная и конечная даты
        start_date = datetime(start_year, 1, 1)
        end_date = datetime(end_year, 12, 31)

        # Разница в днях между датами
        delta_days = (end_date - start_date).days

        # Случайная дата
        random_days = random.randint(0, delta_days)
        random_date = start_date + timedelta(days=random_days)

        # Возвращаем дату в формате с ведущими нулями
        return random_date.strftime("%Y-%m-%d")
