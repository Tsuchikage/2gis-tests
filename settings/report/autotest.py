"""Методы для формирования отчёта при выполнении автотестов."""
import os
from typing import Callable

import allure


def attach_file(path: str):
    """
    Прикрепляет файл к результату теста.

    :param path: Путь к файлу.
    """
    file_path, file_extension = os.path.splitext(path)
    file_name = os.path.basename(file_path)
    allure.attach.file(source=path, name=file_name, extension=file_extension)


def name(name: str) -> Callable:
    """
    Устанавливает отображаемое имя теста в отчёте.

    :param name: Название теста.
    """
    return allure.title(name)


def step(step_name: str):
    """
    Добавляет шаг теста в отчёт.

    :param step_name: наименование шага автотеста.
    """
    return allure.step(step_name)


def add_link(url: str, title: str = None) -> Callable:
    """
    Добавляет ссылку к результату теста.

    :param url: Ссылка.
    :param type_: Тип ссылки.
    :param title: Название ссылки.
    """
    return allure.link(url=url, name=title, link_type="link")


def external_id(id_: str) -> Callable:
    """
    Устанавливает внешний идентификатор теста.

    :param id_: GUID теста.
    """
    return allure.label("Autotest id", id_)


def num(*test_work_items_id: int or str) -> Callable:
    """
    Устанавливает связь автотеста и тест-кейса.

    :param test_work_items_id: список идентификаторов тест-кейсов.
    """
    return allure.label("Test cases", *test_work_items_id)


def description(text: str):
    """
    Добавляет описание теста.

    :param text: Описание.
    """
    allure.description(text)
    return
