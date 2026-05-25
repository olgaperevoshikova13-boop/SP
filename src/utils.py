import json
import os
from typing import Any
from typing import Dict
from typing import List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу

    Returns:
        Список словарей с транзакциями или пустой список при ошибке
    """
    # Проверяем, существует ли файл
    if not os.path.exists(file_path):
        return []

    # Проверяем, что файл не пустой
    if os.path.getsize(file_path) == 0:
        return []

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

            # Проверяем, что данные — это список
            if isinstance(data, list):
                return data
            else:
                return []

    except (json.JSONDecodeError, FileNotFoundError, PermissionError):
        return []
