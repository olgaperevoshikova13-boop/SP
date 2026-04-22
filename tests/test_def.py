
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
def stn_int_get_mask_account():
    """Ввод номера счета стандартное кол-во цифр (20) числом"""
    return 12345678912345678912


@pytest.fixture
def stn_str_get_mask_account():
    """Ввод номера счета стандартное кол-во цифр (20) строкой"""
    return '12345678912345678912'


@pytest.fixture
def short_str_get_mask_account():
    """Ввод номера счета - короткий номер, строкой"""
    return '1234'


def test_stn_int_get_mask_account(stn_int_get_mask_account):
    """Проверка на ввод номера счета стандартной длины, числом"""
    assert get_mask_account(stn_int_get_mask_account) == '**8912'


def test_stn_str_get_mask_account(stn_str_get_mask_account):
    """Проверка на ввод номера счета стандартной длины, строкой"""
    assert get_mask_account(stn_str_get_mask_account) == '**8912'


def test_short_str_get_mask_account(short_str_get_mask_account):
    """Проверка на ввод номера счета короткой длины, строкой"""
    assert get_mask_account(short_str_get_mask_account) == "Неверный номер счета"


@pytest.fixture
def check_stn_mask_account_card():
    """Стандартный номер счета"""
    return "Счет 73654108430135874305"


@pytest.fixture
def card_stn_mask_account_card():
    """Стандартный номер карты"""
    return "Visa 4108430135874305"


@pytest.fixture
def no_num_stn_mask_account_card():
    """Отсутствие номера"""
    return "Visa "


def test_check_stn_mask_account_card(check_stn_mask_account_card):
    """Проверка со стандартным номером счета"""
    assert mask_account_card(check_stn_mask_account_card) == "Счет **4305"


def test_card_stn_mask_account_card(card_stn_mask_account_card):
    """Проверка со стандартным номером карты"""
    assert mask_account_card(card_stn_mask_account_card) == "Visa 4108 43** **** 4305"


def test_no_num_stn_mask_account_card(no_num_stn_mask_account_card):
    """Проверка без номера"""
    assert mask_account_card(no_num_stn_mask_account_card) == "Неверный номер карты или счета"


@pytest.fixture
def fix_get_date():
    """Тестовые данные даты"""
    return "2024-03-11T02:26:18.671407"


@pytest.fixture
def valid_date_without_ms():
    """Дата без миллисекунд"""
    return "2024-03-11T02:26:18"


@pytest.fixture
def short_date():
    """Короткая строка с датой (без времени)"""
    return "2024-03-11"


def test_get_date(fix_get_date):
    """Тестирование правильности преобразования даты"""
    assert "11.03.2024"


def test_get_date_without_ms(valid_date_without_ms):
    """Проверка на дату без миллисекунд"""
    assert get_date(valid_date_without_ms) == "11.03.2024"


def test_get_date_short(short_date):
    """Проверка на короткую строку с датой (без времени)"""
    assert get_date(short_date) == "11.03.2024"


@pytest.fixture
def sample_transactions():
    """Стандартный список словарей для тестов"""
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]


@pytest.fixture
def empty_list():
    """Пустой список"""
    return []


@pytest.fixture
def no_matching_state():
    """Список без словарей с указанным статусом"""
    return [
        {'id': 1, 'state': 'CANCELED', 'date': '2020-01-01T00:00:00.000000'},
        {'id': 2, 'state': 'CANCELED', 'date': '2020-01-02T00:00:00.000000'},
    ]


def test_filter_by_state_default(sample_transactions):
    """Фильтрация со статусом по умолчанию ('EXECUTED')
    Должны остаться только словари с state='EXECUTED'"""
    result = filter_by_state(sample_transactions)
    expected = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    ]
    assert result == expected


def test_filter_by_state_canceled(sample_transactions):
    """Фильтрация со статусом 'CANCELED'
    Должны остаться только словари с state='CANCELED'"""
    result = filter_by_state(sample_transactions, state='CANCELED')
    expected = [
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]
    assert result == expected


def test_filter_by_state_no_matching(no_matching_state):
    """Отсутствие словарей с указанным статусом
    Должен вернуться пустой список"""
    result = filter_by_state(no_matching_state, state='EXECUTED')
    assert result == []


def test_filter_by_state_empty_list(empty_list):
    """Пустой список на входе
    Должен вернуться пустой список"""
    result = filter_by_state(empty_list, state='EXECUTED')
    assert result == []


@pytest.mark.parametrize("test_state, expected_count", [
    ('EXECUTED', 2),
    ('CANCELED', 2),
    ('UNKNOWN', 0),
])
def test_filter_by_state_parametrized(sample_transactions, test_state, expected_count):
    """Параметризация для различных значений статуса
    Проверяет количество отфильтрованных элементов"""
    result = filter_by_state(sample_transactions, state=test_state)
    assert len(result) == expected_count


@pytest.mark.parametrize("test_state, expected_ids", [
    ('EXECUTED', [41428829, 939719570]),
    ('CANCELED', [594226727, 615064591]),
])
def test_filter_by_state_parametrized_ids(sample_transactions, test_state, expected_ids):
    """Параметризация с проверкой конкретных id"""
    result = filter_by_state(sample_transactions, state=test_state)
    result_ids = [item['id'] for item in result]
    assert result_ids == expected_ids


@pytest.fixture
def sample_transactions():
    """Стандартный список словарей для тестов"""
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
    ]


@pytest.fixture
def same_dates_transactions():
    """Список с одинаковыми датами"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': '2020-01-01T10:00:00.000000'},
        {'id': 2, 'state': 'CANCELED', 'date': '2020-01-01T12:00:00.000000'},
        {'id': 3, 'state': 'PENDING', 'date': '2020-01-01T08:00:00.000000'},
    ]


@pytest.fixture
def invalid_dates_transactions():
    """Список с некорректными форматами дат"""
    return [
        {'id': 1, 'state': 'EXECUTED', 'date': 'некорректная_дата'},
        {'id': 2, 'state': 'CANCELED', 'date': '2020-01-01'},
        {'id': 3, 'state': 'PENDING', 'date': ''},
    ]


@pytest.fixture
def empty_list():
    """Пустой список"""
    return []


def test_sort_by_date_descending(sample_transactions):
    """Сортировка по убыванию (по умолчанию)
    Ожидаемый порядок: от новых к старым"""
    result = sort_by_date(sample_transactions)
    expected = [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
    ]
    assert result == expected


def test_sort_by_date_ascending(sample_transactions):
    """Сортировка по возрастанию (descending=False)
    Ожидаемый порядок: от старых к новым"""
    result = sort_by_date(sample_transactions, descending=False)
    expected = [
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'},
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    ]
    assert result == expected


def test_sort_by_date_same_dates(same_dates_transactions):
    """Сортировка при одинаковых датах
    Порядок элементов с одинаковой датой может сохраняться как есть"""
    result = sort_by_date(same_dates_transactions, descending=True)
    for item in result:
        assert item['date'].startswith('2020-01-01')
    assert len(result) == 3


def test_sort_by_date_empty_list(empty_list):
    """Пустой список на входе
    Должен вернуться пустой список"""
    result = sort_by_date(empty_list)
    assert result == []


def test_sort_by_date_invalid_formats(invalid_dates_transactions):
    """Некорректные форматы дат
    Функция должна сортировать как строки (лексикографически)"""
    result = sort_by_date(invalid_dates_transactions, descending=True)
    assert len(result) == 3


def test_sort_by_date_single_element():
    """Тестирование список с одним элементом"""
    single = [{'id': 1, 'state': 'EXECUTED', 'date': '2020-01-01T00:00:00'}]
    result = sort_by_date(single)
    assert result == single


@pytest.mark.parametrize("descending, expected_first_id", [
    (True, 41428829),   # убывание: сначала 2019-07-03 → id 41428829
    (False, 939719570), # возрастание: сначала 2018-06-30 → id 939719570
])
def test_sort_by_date_parametrized(sample_transactions, descending, expected_first_id):
    """Параметризация для проверки первого элемента при разных порядках"""
    result = sort_by_date(sample_transactions, descending=descending)
    assert result[0]['id'] == expected_first_id


@pytest.mark.parametrize("descending, expected_last_id", [
    (True, 939719570),   # убывание: последний — самая старая дата → id 939719570
    (False, 41428829),   # возрастание: последний — самая новая дата → id 41428829
])
def test_sort_by_date_parametrized_last(sample_transactions, descending, expected_last_id):
    """Параметризация для проверки последнего элемента при разных порядках"""
    result = sort_by_date(sample_transactions, descending=descending)
    assert result[-1]['id'] == expected_last_id
