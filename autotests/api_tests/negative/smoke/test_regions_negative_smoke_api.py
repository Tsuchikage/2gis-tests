import pytest

from autotests.api.api_helpers.regions_helper_api import RegionsHelperApi
from autotests.api.api_data.regions_data_api import RegionsDataApi
from autotests.api.api_methods.regions_methods_api import RegionsApi
from settings.report import autotest
from settings.utils import check_response_status


@pytest.mark.api
@pytest.mark.smoke
@pytest.mark.negative
class TestNegativeRegionsSmokeApi:

    @pytest.fixture(autouse=True)
    def setup(self, config, session_token):
        self.helper = RegionsHelperApi(config=config)
        self.regions_api = RegionsApi(config=config)
        self.token = session_token

    @autotest.num("101")
    @autotest.external_id("609ec550-90b8-49f3-881b-619d358ed06b")
    @autotest.name("Negative Smoke. Создание избранного места с некорректным title.")
    @pytest.mark.parametrize("title_value", ["", "A" * 1000])
    def test_609ec550_negative_create_region_with_invalid_title(self, title_value):
        """
        Баг: При отправке невалидных граничных значений (title > 1000)
        сервер отвечает 200, хотя должен быть 400.
        """
        # Arrange
        with autotest.step(f"Подготавливаем данные с некорректным title - {title_value}"):
            data = RegionsDataApi(title=title_value).data

        # Act
        with autotest.step("Отправляем запрос на создание избранного места с некорректным title"):
            response = self.regions_api.post_favorite_region(data=data, token=self.token)

        # Assert
        with autotest.step("Проверяем, что сервер возвращает статус-код 400"):
            check_response_status(response, 400)

    @autotest.num("103")
    @autotest.external_id("4615d5b3-ccd8-44c0-aa67-e3b5ea8f61a0")
    @autotest.name("Negative Smoke. Создание избранного места с недопустимым color.")
    def test_4615d5b3_negative_create_region_with_invalid_color(self):
        # Arrange
        with autotest.step("Подготавливаем данные с color='PURPLE'"):
            data = RegionsDataApi(color="PURPLE").data

        # Act
        with autotest.step("Отправляем запрос с неверным цветом"):
            response = self.regions_api.post_favorite_region(data=data, token=self.token)

        # Assert
        with autotest.step("Проверяем, что сервер возвращает статус-код 400"):
            check_response_status(response, 400)

    @autotest.num("104")
    @autotest.external_id("aa12d425-58e5-4f87-8f7b-ae0a0499c8ae")
    @autotest.name("Negative Smoke. Создание избранного места без token.")
    def test_aa12d425_negative_create_region_without_token(self):
        # Arrange
        with autotest.step("Подготавливаем корректные данные без передачи token"):
            data = RegionsDataApi().data

        # Act
        with autotest.step("Отправляем запрос без token"):
            response = self.regions_api.post_favorite_region(data=data, token="")

        # Assert
        with autotest.step("Проверяем, что сервер возвращает статус-код 401"):
            check_response_status(response, 401)

    @autotest.num("105")
    @autotest.external_id("5de578b9-91ff-4c0d-a025-c386285c7e8f")
    @autotest.name("Negative Smoke. Создание избранного места с некорректными значения latitude.")
    @pytest.mark.parametrize("invalid_lat", [999.999, "abc"])
    def test_5de578b9_negative_create_region_with_invalid_lat(self, invalid_lat):
        # Arrange
        with autotest.step(f"Подготавливаем данные с lat={invalid_lat!r}"):
            data = RegionsDataApi(lat=invalid_lat).data

        # Act
        with autotest.step("Отправляем запрос с некорректным значением lat"):
            response = self.regions_api.post_favorite_region(data=data, token=self.token)

        # Assert
        with autotest.step("Проверяем, что сервер возвращает статус-код 400"):
            check_response_status(response, 400)

    @autotest.num("106")
    @autotest.external_id("86a9f492-054c-48dd-95ba-717466109ee4")
    @autotest.name("Negative Smoke. Создание избранного места с валидными граничными данными latitude и longitude.")
    def test_86a9f492_negative_create_region_with_invalid_lat_lon(self):
        """
        Баг: При отправке валидных граничных значений (lat=0, lon=0)
        сервер отвечает 500 Internal Server Error, хотя должен быть 200.
        """
        # Arrange
        with autotest.step("Подготавливаем данные: lat=0, lon=0"):
            data = RegionsDataApi(lat=0, lon=0).data

        # Act
        with autotest.step("Отправляем запрос с валидными граничными данными latitude и longitude."):
            response = self.regions_api.post_favorite_region(data=data, token=self.token)

        # Assert
        with autotest.step("Проверяем, что сервер возвращает статус-код 200 при корректных данных"):
            check_response_status(response, 200)
