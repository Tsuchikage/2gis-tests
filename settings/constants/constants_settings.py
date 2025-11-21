from pathlib import Path


class Paths:
    """
    Централизованный класс для управления путями к файловым артефактам тестов.
    Все директории располагаются в корневой папке ./logs/
    """

    ROOT_DIR = Path(__file__).resolve().parent.parent.parent
    LOGS_ROOT = ROOT_DIR / "logs"
    REPORTS = LOGS_ROOT / "reports"  # Папка для отчётов (общая)
    REPORTS_HTML = REPORTS / "html"  # Папка для pytest-html отчётов

    # Allure
    ALLURE_RESULTS = REPORTS / "allure-results"  # Сырые результаты allure (json/attachments)
    ALLURE_REPORT = REPORTS / "allure-report"  # Сгенерированный HTML-репорт allure
