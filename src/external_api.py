from typing import Any
from typing import Dict

import requests  # type: ignore
from dotenv import load_dotenv  # type: ignore

load_dotenv()


def convert_to_rubles(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    """
    # Получаем сумму и валюту из транзакции
    amount_value = transaction.get('operationAmount', {}).get('amount', 0)
    amount = float(amount_value) if amount_value else 0.0
    currency = transaction.get('operationAmount', {}).get('currency', {}).get('code', 'RUB')

    # Если валюта уже рубли — возвращаем сумму
    if currency == 'RUB':
        return amount

    # Используем бесплатный API без ключа
    url = f"https://api.exchangerate-api.com/v4/latest/{currency}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        data = response.json()
        rate = data.get('rates', {}).get('RUB')

        if rate:
            rub_amount = amount * rate
            return round(rub_amount, 2)  # type: ignore
        else:
            raise ValueError(f"Курс для {currency} не найден")

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Ошибка при запросе к API: {e}")
    except (KeyError, ValueError) as e:
        raise RuntimeError(f"Ошибка при обработке ответа API: {e}")
