import logging
from typing import Any

import pandas as pd

from src.category_counter import count_categories
from src.external_api import convert_to_rubles
from src.file_processing import read_csv_transactions
from src.file_processing import read_excel_transactions
from src.filters import filter_by_description
from src.masks import get_mask_account
from src.masks import get_mask_card_number
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


def mask_card_or_account(card_or_account: Any) -> str:
    """Маскирует номер карты или счета в строке."""
    if card_or_account is None:
        return ""
    card_or_account_str = str(card_or_account)

    if not card_or_account_str:
        return ""

    import re

    if "Счет" in card_or_account_str or "счет" in card_or_account_str:
        numbers = re.findall(r"\d+", card_or_account_str)
        if numbers:
            account_number = numbers[-1]
            masked_account = get_mask_account(account_number)
            return card_or_account_str.replace(account_number, masked_account)
        return card_or_account_str
    else:
        numbers = re.findall(r"\d+", card_or_account_str)
        if numbers:
            card_number = numbers[-1]
            if len(card_number) == 16:
                masked_card = get_mask_card_number(card_number)
                return card_or_account_str.replace(card_number, masked_card)
        return card_or_account_str


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
        if not isinstance(t, dict) or not t:
            continue
        # Пропускаем пустые строки
        if t.get("id") is None or (hasattr(pd, 'isna') and pd.isna(t.get("id"))):
            continue

        # Форматируем дату
        date_raw = str(t.get("date", ""))
        if len(date_raw) >= 10:
            date_str = f"{date_raw[8:10]}.{date_raw[5:7]}.{date_raw[0:4]}"
        else:
            date_str = date_raw

        description = t.get("description", "")

        # Маскируем from и to
        from_str = mask_card_or_account(t.get("from", ""))
        to_str = mask_card_or_account(t.get("to", ""))

        # Получаем сумму и валюту (из CSV поле amount, из JSON — operationAmount.amount)
        if "operationAmount" in t:
            amount_data = t.get("operationAmount", {})
            amount = amount_data.get("amount", "0")
            currency = amount_data.get("currency", {}).get("code", "RUB")
        else:
            amount = t.get("amount", 0)
            currency = t.get("currency_code", "RUB")

        # Форматируем сумму
        try:
            amount_float = float(amount)
            amount_str = f"{amount_float:.2f}"
        except (ValueError, TypeError):
            amount_str = str(amount)

        # Выводим транзакцию
        print(f"{date_str} {description}")
        if from_str or to_str:
            print(f"{from_str} -> {to_str}")
        print(f"Сумма: {amount_str} {currency}\n")


if __name__ == "__main__":
    main()
