
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str = 'USD') -> Iterator[Dict[str, Any]]:
    """
        Фильтрует транзакции по валюте и возвращает итератор.

        Параметры:
            transactions: список словарей с транзакциями
            currency: код валюты для фильтрации (например, 'USD')

        Возвращает:
            Итератор, выдающий транзакции с указанной валютой по одной
        """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
        Принимает список словарей с транзакциями и возвращает описание каждой операции по очереди

        Параметр:
            transactions: список словарей с транзакциями

        Возвращает:
            Описание операции
    """
    for transaction in transactions:
        yield transaction.get("description", "Описание отсутствует")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
        Генератор должен принимать начальное и конечное
        значения для генерации диапазона номеров
        Параметры:
            start: начало
            end: конец
        Возвращает:
            Номера банковских карт в формате XXXX XXXX XXXX XXXX
    """
    for number in range(start, end + 1):
        formatted = f"{number:016d}"
        card_number = " ".join([formatted[i:i+4] for i in range(0, 16, 4)])
        yield card_number
