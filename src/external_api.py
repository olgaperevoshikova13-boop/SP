import os
from typing import Any
from typing import Dict

import requests  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction: Словарь с данными о транзакции

    Returns:
        Сумма в рублях (float)
    """
    # Получаем сумму и валюту из транзакции
    amount_value = transaction.get('operationAmount', {}).get('amount', 0)
    amount = float(amount_value) if amount_value else 0.0
    currency = transaction.get('operationAmount', {}).get('currency', {}).get('code', 'RUB')

    # Если валюта уже рубли — возвращаем сумму
    if currency == 'RUB':
        return amount

    # Получаем API-ключ из переменных окружения
    api_key = os.getenv('EXCHANGE_API_KEY')
    api_url = os.getenv('EXCHANGE_API_URL', 'https://api.apilayer.com/exchangerates_data/convert')

    if not api_key:
        raise ValueError("API ключ не найден. Установите EXCHANGE_API_KEY в .env файле")

    # Делаем запрос к API для получения курса валюты
    headers = {'apikey': api_key}
    params = {
        'to': 'RUB',
        'from': currency,
        'amount': amount
    }

    try:
        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        rub_amount = data.get('result', 0)  # ← изменено

        if rub_amount:
            return float(round(rub_amount, 2))
        else:
            raise ValueError(f"Не удалось конвертировать {currency} в RUB")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ошибка при запросе к API: {e}")
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"Ошибка при обработке ответа API: {e}")
