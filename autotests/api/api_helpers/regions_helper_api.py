from autotests.api.api_data.regions_data_api import RegionsDataApi
from autotests.api.api_methods.regions_methods_api import RegionsApi
from settings.report import autotest
from settings.utils import check_response_status


class RegionsHelperApi:
    """
    Хелпер для работы с API избранных мест.
    """

    def __init__(self, config):
        """
        :param config: Конфигурационный объект (`ConfigModel`).
        """
        self.regions_api = RegionsApi(config)
        # self.entities_registry = EntitiesRegistry(config=config) # Удаление после теста


    def create_favorite_region(self, token: str, region_data: dict = None) -> dict:
        """
        Создает избранное место и возвращает данные.

        :param token: Сессионный токен.
        :param region_data: Данные избранного места. Если не переданы - генерируются.
        :return: Словарь данных созданного избранного места.
        """
        if region_data is None:
            region_data = RegionsDataApi().data

        with autotest.step("Создаем избранное место"):
            response = self.regions_api.post_favorite_region(
                data=region_data,
                token=token
            )

        check_response_status(response, 200)

        # Удаление сущностей после теста
        # self.entities_registry.add_entities_ids_dict(
        #     ent_type=EntitiesTypes.favorite_region,
        #     ent_param=regions.get('id')
        # )

        return region_data
