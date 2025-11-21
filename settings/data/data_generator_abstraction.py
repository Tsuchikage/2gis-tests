from settings.utils import get_current_test_name


class DataAbstractionGenerator:
    """
    Абстрактный генератор тестовых данных
    """

    @staticmethod
    def generate_entity_name(id_: str, name: str) -> str:
        """
        Формирует уникальное имя сущности для текущего теста, включая внешний ID и часть идентификатора сущности.

        :param id_: Уникальный идентификатор сущности (например, UUID или int64).
        :param name: Краткое название сущности (например, "user", "dataset").
        :return: Строка в формате `<test_id>_<label>_00000000_<entity_id[:10]>`.
        """
        test_name = get_current_test_name()
        prefix = test_name[5:13] if test_name else "unknown"

        return f"{prefix}_{name}_00000000_{id_[:10]}"

