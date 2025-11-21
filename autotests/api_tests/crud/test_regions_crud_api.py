import pytest

from autotests.api.api_data.regions_data_api import RegionsDataApi
from autotests.api.api_helpers.regions_helper_api import RegionsHelperApi
from autotests.api.api_methods.regions_methods_api import RegionsApi
from settings.report import autotest
from settings.utils import verify_data


@pytest.mark.api
@pytest.mark.crud
class TestRegionsCrudApi:

    @pytest.fixture(autouse=True)
    def setup(self, config, session_token):
        self.helper = RegionsHelperApi(config=config)
        self.regions_api = RegionsApi(config=config)
        self.token = session_token

    @autotest.num("1")
    @autotest.name("CRUD Create (RegionsApi). Создание избранного места.")
    @autotest.external_id("123e4567-e89b-12d3-a456-426614174020")
    def test_123e4567_create_favorite_region(self):
        # Arrange
        favorite_region_data = RegionsDataApi().data

        # Act
        with autotest.step("Создаем избранное место"):
            response_data = self.helper.create_favorite_region(
                region_data=favorite_region_data,
                token=self.token
            )

        # Assert
        with autotest.step("Проверяем корректность данных созданного избранного места."):
            verify_data(
                actual_data=response_data,
                expected_data=favorite_region_data,
            )
