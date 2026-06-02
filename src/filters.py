import logging
import re
from typing import Any
from typing import Dict
from typing import List

logger = logging.getLogger("filters")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/filters.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def filter_by_description(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Возвращает транзакции, в описании которых содержится искомая строка (регистронезависимо).
    """
    logger.debug(f"Поиск по описанию: '{search_string}'")
    try:
        pattern = re.compile(re.escape(search_string), re.IGNORECASE)
        result = [t for t in transactions if pattern.search(t.get("description", ""))]
        logger.info(f"Найдено {len(result)} транзакций по запросу '{search_string}'")
        return result
    except Exception as e:
        logger.error(f"Ошибка при поиске по описанию: {e}")
        return []
