import logging

from src.category_counter import count_categories
from src.external_api import convert_to_rubles
from src.file_processing import read_csv_transactions
from src.file_processing import read_excel_transactions
from src.filters import filter_by_description
from src.processing import filter_by_state
from src.processing import sort_by_date
from src.utils import load_transactions

logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/main.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

VALID_STATUSES = {"EXECUTED", "CANCELED", "PENDING"}
SOURCE_FILE_MAP = {
    "1": ("JSON", lambda: load_transactions("data/operations.json")),
    "2": ("CSV", lambda: read_csv_transactions("data/transactions.csv")),
    "3": ("XLSX", lambda: read_excel_transactions("data/transactions_excel.xlsx")),
}


def get_valid_status() -> str:
    while True:
        print("Введите статус (EXECUTED, CANCELED, PENDING):")
        status = input().strip().upper()
        if status in VALID_STATUSES:
            print(f"Операции отфильтрованы по статусу \"{status}\"")
            return status
        print(f"Статус операции \"{status}\" недоступен.")


def ask_yes_no(question: str) -> bool:
    while True:
        ans = input(f"{question} (да/нет): ").strip().lower()
        if ans == "да":
            return True
        if ans == "нет":
            return False
        print("Пожалуйста, ответьте 'да' или 'нет'.")


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input().strip()
    if choice not in SOURCE_FILE_MAP:
        print("Неверный выбор. Завершение программы.")
        return

    source_name, loader_func = SOURCE_FILE_MAP[choice]
    print(f"Для обработки выбран {source_name}-файл.")
    transactions = loader_func()

    if not transactions:
        print("Не удалось загрузить транзакции. Завершение программы.")
        return

    status = get_valid_status()
    filtered = filter_by_state(transactions, state=status)

    if ask_yes_no("Отсортировать операции по дате?"):
        order = input("Отсортировать по возрастанию или по убыванию? ").strip().lower()
        descending = order != "по возрастанию"
        filtered = sort_by_date(filtered, descending=descending)

    if ask_yes_no("Выводить только рублевые транзакции?"):
        filtered = [t for t in filtered if convert_to_rubles(t) is not None]

    if ask_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        word = input("Введите слово для поиска: ").strip()
        filtered = filter_by_description(filtered, word)
        categories = ["Перевод", "Оплата", "Открытие"]
        cat_counts = count_categories(filtered, categories)
        print("Статистика по категориям:")
        for cat, cnt in cat_counts.items():
            print(f"{cat}: {cnt}")

    print("Распечатываю итоговый список транзакций...")
    if not filtered:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"Всего банковских операций в выборке: {len(filtered)}")
    for t in filtered:
        amount = convert_to_rubles(t)
        cur = t.get("operationAmount", {}).get("currency", {}).get("code", "")
        print(f"{t.get('date', '')[:10]} {t.get('description', '')}")
        print(f"Сумма: {amount} {cur if cur != 'RUB' else 'руб.'}")


if __name__ == "__main__":
    main()
