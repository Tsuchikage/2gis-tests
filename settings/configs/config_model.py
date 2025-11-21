from pydantic import BaseModel, Field


class ConfigModel(BaseModel):
    """
    Главная модель конфигурации окружения для автотестов.
    """
    base_url: str | None = Field(
        default=None,
        alias="base_url",
        description="Базовый URL для обращения к тестируемому API."
    )

    token: str | None = Field(
        default=None,
        alias="token",
        description="Токен."
    )
