import os
from typing import Any
from typing import Dict
from unittest.mock import Mock
from unittest.mock import patch

import pytest
from requests.exceptions import RequestException

from src.external_api import convert_to_rubles


def test_convert_to_rubles_rub() -> None:
    """Тест: конвертация рублей в рубли (без API)"""
    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "100.50",
            "currency": {"code": "RUB"}
        }
    }
    result = convert_to_rubles(transaction)
    assert result == 100.50


@patch('src.external_api.requests.get')
@patch.dict(os.environ, {'EXCHANGE_API_KEY': 'test_key_123'})
def test_convert_to_rubles_usd(mock_get: Any) -> None:
    """Тест: конвертация USD в RUB через API (мок)"""
    mock_response = Mock()
    mock_response.status_code = 200
    # Исправленный мок-ответ для /convert
    mock_response.json.return_value = {
        "result": 912.3
    }
    mock_get.return_value = mock_response

    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "10.00",
            "currency": {"code": "USD"}
        }
    }

    result = convert_to_rubles(transaction)
    assert isinstance(result, float)
    assert result == 912.3


@patch('src.external_api.requests.get')
@patch.dict(os.environ, {'EXCHANGE_API_KEY': 'test_key_123'})
def test_convert_to_rubles_api_error(mock_get: Any) -> None:
    """Тест: ошибка при запросе к API"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.raise_for_status.side_effect = RequestException("API Error")
    mock_get.return_value = mock_response

    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "10.00",
            "currency": {"code": "USD"}
        }
    }

    with pytest.raises(RuntimeError):
        convert_to_rubles(transaction)


def test_convert_to_rubles_missing_amount() -> None:
    """Тест: отсутствует сумма в транзакции"""
    transaction: Dict[str, Any] = {}
    result = convert_to_rubles(transaction)
    assert result == 0.0


def test_convert_to_rubles_missing_currency() -> None:
    """Тест: отсутствует валюта в транзакции (по умолчанию RUB)"""
    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "50.00"
        }
    }
    result = convert_to_rubles(transaction)
    assert result == 50.0


@patch.dict(os.environ, {}, clear=True)
def test_convert_to_rubles_no_api_key() -> None:
    """Тест: отсутствует API ключ"""
    transaction: Dict[str, Any] = {
        "operationAmount": {
            "amount": "10.00",
            "currency": {"code": "USD"}
        }
    }

    with pytest.raises(ValueError, match="API ключ не найден"):
        convert_to_rubles(transaction)
