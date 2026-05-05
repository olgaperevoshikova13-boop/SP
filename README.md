# Банковский виджет

Проект для обработки банковских операций. Принимает номер счета и карты, маскирует их, сортирует даты и фильтрует операции по статусу.

## Установка и запуск

```bash
# Клонировать репозиторий
git clone https://github.com/olgaperevoshikova13-boop/SP.git

# Перейти в папку проекта
cd SP

# Установить зависимости (если используется poetry)
poetry install

--------------------------------------------------------------------------------------

## Модуль src.masks

from src.masks import get_mask_card_number
get_mask_card_number(card_number: Union[str, int]) -> str
"""Возвращает замаскированный номер карты"""
## Пример:
print(get_mask_card_number("1234567890123456")) # 1234 56** **** 3456

from src.masks import get_mask_account
get_mask_account(account: Union[str, int]) -> str
"""Возвращает замаскированный номер счета"""
## Пример:
print(get_mask_account("12345678912345678912")) # **8912

____________________________________

## Модуль src.widget

from src.widget import mask_account_card
mask_account_card(account_card: str) -> str
""" Принимает строку с типом карты/счёта и номером. 

    Определяет по длине номера (16 цифр — карта, 20 — счёт),
    маскирует номер с помощью соответствующих функций.
    Параметры:
        account_card (str): строка вида "Visa Platinum 1234567890123456"
                            или "Счет 73654108430135874305"
    Возвращает:
        str: замаскированный номер с типом карты/счёта,
             или сообщение об ошибке"""
## Пример:
print(mask_account_card("Счет 73654108430135874305") # Счет **4305

from src.widget import get_date
get_date(date: str) -> str
"""Принимает один формат даты и возвращает более удобный формат"""
## Пример:
print(get_date("2024-03-11T02:26:18.671407")) # 11.03.2024

____________________________________

## Модуль src.processing

from src.processing import filter_by_state
filter_by_state(list_of_dicts: list, state: str = 'EXECUTED') -> list[dict]
"""Фильтрует список словарей по ключу 'state'"""
# Пример
print(filter_by_state([
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},  # [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},  #  {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]))                                                                              

from src.processing import sort_by_date
processing(list_of_dicts: list, descending: bool = True) -> list[dict]
"""Сортирует список словарей по дате"""
# Пример
print(sort_by_date([
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},     # [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},    #  {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},    #  {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}     #  {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}]
    ])   
        
____________________________________
        
## Модуль `src.generators`

Модуль содержит функции-генераторы для работы с транзакциями и номерами карт.

### `filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]`

Возвращает итератор, который поочередно выдает транзакции с указанной валютой.

**Пример использования:**

```python
from src.generators import filter_by_currency

transactions = [
    {
        "id": 1,
        "operationAmount": {"currency": {"code": "USD"}}
    },
    {
        "id": 2,
        "operationAmount": {"currency": {"code": "RUB"}}
    },
]

usd_transactions = filter_by_currency(transactions, "USD")
print(next(usd_transactions)["id"])  # 1

from src.generators import transaction_descriptions

### `transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]`

Возвращает итератор с описаниями транзакций.

**Пример:**
```python
from src.generators import transaction_descriptions

transactions = [
    {"description": "Перевод организации"},
    {"description": "Перевод со счета на счет"},
]

descriptions = transaction_descriptions(transactions)
print(next(descriptions))  # "Перевод организации"
print(next(descriptions))  # "Перевод со счета на счет"

from src.generators import card_number_generator

for card in card_number_generator(1, 5):
    print(card)

# 0000 0000 0000 0001
# 0000 0000 0000 0002
# 0000 0000 0000 0003
# 0000 0000 0000 0004
# 0000 0000 0000 0005

--------------------------------------------------------------------------------------

```markdown
## Тестирование

Проект покрыт тестами `pytest`. Для запуска тестов выполните:

```bash
poetry run pytest

Для проверки покрытия кода:
poetry run pytest --cov=src --cov-report=html

```markdown
## Технологии

- Python 3.14
- Poetry
- pytest (тестирование)
- flake8, mypy (линтеры)

## Автор

Olga
