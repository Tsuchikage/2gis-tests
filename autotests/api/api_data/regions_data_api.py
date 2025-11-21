from settings.data.data_generator_abstraction import DataAbstractionGenerator
from settings.utils import Randomizer


class RegionsDataApi(DataAbstractionGenerator):
    """
    Вспомогательный класс для генерации данных при создании избранного места.
    """

    def __init__(
        self,
        title: str | None = None,
        lat: float | None = None,
        lon: float | None = None,
        color: str | None = None,
    ):
        """
        Инициализирует объект RegionsDataApi и формирует словарь с данными
        для создания избранного места.

        Если параметры не переданы, значения генерируются автоматически.

        :param title: Название места (если None - генерируется случайное).
        :param lat: Широта (если None - случайное значение в диапазоне [-90; 90]).
        :param lon: Долгота (если None - случайное значение в диапазоне [-180; 180]).
        :param color: Цвет иконки (BLUE, GREEN, RED, YELLOW). Если None - выбирается случайно.
        """
        allowed_colors = ["BLUE", "GREEN", "RED", "YELLOW"]

        if title is None:
            entity_id = Randomizer.uuid()
            self.title = self.generate_entity_name(
                id_=entity_id,
                name="favorite_place",
            )
        else:
            self.title = title

        self.lat = lat if lat is not None else Randomizer.float_between(-90, 90, precision=6)
        self.lon = lon if lon is not None else Randomizer.float_between(-180, 180, precision=6)
        self.color = color if color is not None else Randomizer.pick_random(allowed_colors)

        self.data = {
            "title": self.title,
            "lat": self.lat,
            "lon": self.lon,
            "color": self.color,
        }
