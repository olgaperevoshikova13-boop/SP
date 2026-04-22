
import pytest

from src.masks import *
from src.widget import *
from src.processing import *


@pytest.fixture
def stn_get_mask_card_number():
    """Стандартный номер карты (16 цифр)"""
    return '1234567890123453'


@pytest.fixture
def short_get_mask_card_number():
    """Короткий номер карты"""
    return '1234'


@pytest.fixture
def long_get_mask_card_number():
    """Длинный номер карты"""
    return '1234567890123453123123123123'


@pytest.fixture
def empty_get_mask_card_number():
    """Пустой ввод"""
    return ''


def test_get_mask_card_number_stn(stn_get_mask_card_number):
    """Проверка на номер стандартной длины"""
    assert get_mask_card_number(stn_get_mask_card_number) == "1234 56** **** 3453"


def test_get_mask_card_number_short(short_get_mask_card_number):
    """Проверка на номер короткой длины"""
    assert get_mask_card_number(short_get_mask_card_number) == "Неверный номер карты"


def test_get_mask_card_number_long(long_get_mask_card_number):
    """Проверка на номер длинной длины"""
    assert get_mask_card_number(long_get_mask_card_number) == "Неверный номер карты"


def test_get_mask_card_number_empty(empty_get_mask_card_number):
    """Проверка на пустой ввод"""
    assert get_mask_card_number(empty_get_mask_card_number) == "Неверный номер карты"

@pytest.fixture
def fix_get_mask_account():
    return '12345678912345678912'


def test_get_mask_account(fix_get_mask_account):
    assert get_mask_account(fix_get_mask_account) == '**8912'


@pytest.fixture
def fix_mask_account_card():
    return "Счет 73654108430135874305"


def test_mask_account_card(fix_mask_account_card):
    assert mask_account_card(fix_mask_account_card) == "Счет **4305"


@pytest.fixture
def fix_get_date():
    return "2024-03-11T02:26:18.671407"


def test_get_date(fix_get_date):
    assert "11.03.2024"


@pytest.fixture
def fix_filter_by_state():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]


def test_filter_by_state(fix_filter_by_state):
    assert filter_by_state(fix_filter_by_state) == [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
        ]


@pytest.fixture
def fix_sort_by_date():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]


def test_sort_by_date(fix_sort_by_date):
    assert sort_by_date(fix_sort_by_date) == [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'}
    ]
