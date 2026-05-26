import json
import logging
import os
from typing import Any
from typing import Dict
from typing import List

# Настройка логгера для utils
logger_utils = logging.getLogger("utils")
logger_utils.setLevel(logging.DEBUG)

file_handler_utils = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_handler_utils.setLevel(logging.DEBUG)

formatter_utils = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler_utils.setFormatter(formatter_utils)

logger_utils.addHandler(file_handler_utils)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    logger_utils.debug(f"Попытка загрузки файла: {file_path}")

    if not os.path.exists(file_path):
        logger_utils.error(f"Файл не найден: {file_path}")
        return []

    if os.path.getsize(file_path) == 0:
        logger_utils.error(f"Файл пуст: {file_path}")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            logger_utils.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
            return data
        else:
            logger_utils.error(f"Данные в файле не являются списком: {file_path}")
            return []
    except json.JSONDecodeError as e:
        logger_utils.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except Exception as e:
        logger_utils.error(f"Неизвестная ошибка при загрузке файла {file_path}: {e}")
        return []
