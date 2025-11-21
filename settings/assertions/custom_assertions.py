def assert_equal(actual, expected, message=None):
    """
    Проверяет, что фактическое значение равно ожидаемому.

    :param actual: Фактическое значение.
    :param expected: Ожидаемое значение.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если значения не равны.
    """
    if actual != expected:
        raise AssertionError(message or f"{actual} != {expected}")


def assert_not_equal(actual, expected, message=None):
    """
    Проверяет, что фактическое значение не равно ожидаемому.

    :param actual: Фактическое значение.
    :param expected: Значение, которое не должно совпадать.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если значения совпадают.
    """
    if actual == expected:
        raise AssertionError(message or f"{actual} == {expected}")


def assert_true(value, message=None):
    """
    Проверяет, что значение является True.

    :param value: Проверяемое значение.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если значение не True.
    """
    if not value:
        raise AssertionError(message or f"Expected True, but got {value}")


def assert_false(value, message=None):
    """
    Проверяет, что значение является False.

    :param value: Проверяемое значение.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если значение не False.
    """
    if value:
        raise AssertionError(message or f"Expected False, but got {value}")


def assert_is_none(value, message=None):
    """
    Проверяет, что значение является None.

    :param value: Проверяемое значение.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если значение не None.
    """
    if value is not None:
        raise AssertionError(message or f"Expected None, but got {value}")


def assert_is_not_none(value, message=None):
    """
    Проверяет, что значение не является None.

    :param value: Проверяемое значение.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если значение является None.
    """
    if value is None:
        raise AssertionError(message or "Expected value to be not None")


def assert_greater(actual, expected, message=None):
    """
    Проверяет, что фактическое значение больше ожидаемого.

    :param actual: Фактическое значение.
    :param expected: Ожидаемое значение для сравнения.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если фактическое значение не больше ожидаемого.
    """
    if not actual > expected:
        raise AssertionError(message or f"{actual} > {expected} is not True")


def assert_greater_equal(actual, expected, message=None):
    """
    Проверяет, что фактическое значение больше или равно ожидаемому.

    :param actual: Фактическое значение.
    :param expected: Ожидаемое значение для сравнения.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если фактическое значение меньше ожидаемого.
    """
    if not actual >= expected:
        raise AssertionError(message or f"{actual} >= {expected} is not True")


def assert_less(actual, expected, message=None):
    """
    Проверяет, что фактическое значение меньше ожидаемого.

    :param actual: Фактическое значение.
    :param expected: Ожидаемое значение для сравнения.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если фактическое значение не меньше ожидаемого.
    """
    if not actual < expected:
        raise AssertionError(message or f"{actual} < {expected} is not True")


def assert_less_equal(actual, expected, message=None):
    """
    Проверяет, что фактическое значение меньше или равно ожидаемому.

    :param actual: Фактическое значение.
    :param expected: Ожидаемое значение для сравнения.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если фактическое значение больше ожидаемого.
    """
    if not actual <= expected:
        raise AssertionError(message or f"{actual} <= {expected} is not True")


def assert_in(item, container, message=None):
    """
    Проверяет, что элемент содержится в коллекции.

    :param item: Элемент, наличие которого нужно проверить.
    :param container: Коллекция, в которой выполняется поиск.
    :param message: Необязательное пользовательское сообщение об ошибке.
    :raises AssertionError: Если элемент не найден в коллекции.
    """
    if item not in container:
        raise AssertionError(message or f"{item} not found in {container}")
