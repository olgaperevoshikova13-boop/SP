import logging
from collections import Counter
from typing import Any
from typing import Dict
from typing import List

logger = logging.getLogger("category_counter")
logger.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("logs/category_counter.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


def count_categories(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций в каждой категории на основе поля description.
    """
    logger.debug(f"Подсчёт категорий: {categories}")
    counter: Counter[str] = Counter()
    for t in transactions:
        desc = t.get("description", "")
        for cat in categories:
            if cat.lower() in desc.lower():
                counter[cat] += 1
                break
    logger.info(f"Результат подсчёта: {dict(counter)}")
    return dict(counter)
