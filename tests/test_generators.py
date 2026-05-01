
from typing import Any
from typing import Dict
from typing import Iterator
from typing import List

import pytest

from src.generators import card_number_generator
from src.generators import filter_by_currency
from src.generators import transaction_descriptions


@pytest.fixture
def first_filter_by_currency() -> List[Dict[str, Any]]:
    """Список словарей """
    return [{
          "id": 939719570,
          "state": "EXECUTED",
          "date": "2018-06-30T02:08:58.425572",
          "operationAmount": {
              "amount": "9824.07",
              "currency": {
                  "name": "USD",
                  "code": "USD"
              }
          },
          "description": "Перевод организации",
          "from": "Счет 75106830613657916952",
          "to": "Счет 11776614605963066702"
      },
      {
              "id": 142264268,
              "state": "EXECUTED",
              "date": "2019-04-04T23:20:05.206878",
              "operationAmount": {
                  "amount": "79114.93",
                  "currency": {
                      "name": "USD",
                      "code": "USD"
                  }
              },
              "description": "Перевод со счета на счет",
              "from": "Счет 19708645243227258542",
              "to": "Счет 75651667383060284188"
       }]


def test_first_filter_by_currency(first_filter_by_currency: List[Dict[str, Any]]) -> None:
    """Первый тест с фикстурами"""
    usd_transactions = (filter_by_currency(first_filter_by_currency, "USD"))
    first_transaction = next(usd_transactions)
    assert first_transaction["id"] == 939719570
    assert first_transaction["operationAmount"]["currency"]["code"] == "USD"

    second_transaction = next(usd_transactions)
    assert second_transaction["id"] == 142264268
    assert second_transaction["operationAmount"]["currency"]["code"] == "USD"


@pytest.fixture
def first_transaction_descriptions() -> List[Dict[str, Any]]:
    """Первые данные для transaction_descriptions"""
    return [{
          "id": 939719570,
          "state": "EXECUTED",
          "date": "2018-06-30T02:08:58.425572",
          "operationAmount": {
              "amount": "9824.07",
              "currency": {
                  "name": "USD",
                  "code": "USD"
              }
          },
          "description": "Перевод организации",
          "from": "Счет 75106830613657916952",
          "to": "Счет 11776614605963066702"
      },
      {
              "id": 142264268,
              "state": "EXECUTED",
              "date": "2019-04-04T23:20:05.206878",
              "operationAmount": {
                  "amount": "79114.93",
                  "currency": {
                      "name": "USD",
                      "code": "USD"
                  }
              },
              "description": "Перевод со счета на счет",
              "from": "Счет 19708645243227258542",
              "to": "Счет 75651667383060284188"
       }]


def test_first_transaction_descriptions(first_transaction_descriptions: List[Dict[str, Any]]) -> None:
    """Первый тест для transaction_descriptions"""
    tran_des = transaction_descriptions(first_transaction_descriptions)
    first_tran_des = next(tran_des)
    assert first_tran_des == "Перевод организации"


@pytest.fixture
def first_card_number_generator() -> Iterator[str]:
    """Данные для первой проверки"""
    return card_number_generator(4, 6)


def test_first_card_number_generator(first_card_number_generator: Iterator[str]) -> None:
    """Тест card_number_generator"""
    assert next(first_card_number_generator) == "0000 0000 0000 0004"
    assert next(first_card_number_generator) == "0000 0000 0000 0005"
