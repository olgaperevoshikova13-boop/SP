import logging
from typing import Any
from typing import Dict
from typing import List

import pandas as pd

logger = logging.getLogger("file_processing")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler("logs/file_processing.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Считывает транзакции из CSV-файла и возвращает список словарей."""
    logger.debug(f"Попытка чтения CSV: {file_path}")
    try:
        df = pd.read_csv(file_path, sep=';')
        result = df.to_dict(orient="records")
        logger.info(f"Успешно загружено {len(result)} транзакций из CSV")
        return result  # type: ignore
    except FileNotFoundError:
        logger.error(f"CSV файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV: {e}")
        return []


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Считывает транзакции из Excel-файла и возвращает список словарей."""
    logger.debug(f"Попытка чтения Excel: {file_path}")
    try:
        df = pd.read_excel(file_path)
        result = df.to_dict(orient="records")
        logger.info(f"Успешно загружено {len(result)} транзакций из Excel")
        return result  # type: ignore
    except FileNotFoundError:
        logger.error(f"Excel файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel: {e}")
        return []
