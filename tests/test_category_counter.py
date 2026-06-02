from src.category_counter import count_categories


def test_count_categories():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод с карты"},
        {"description": "Оплата услуг"},
    ]
    categories = ["Перевод", "Оплата"]
    result = count_categories(transactions, categories)
    assert result == {"Перевод": 2, "Оплата": 1}


def test_count_categories_empty():
    assert count_categories([], ["Перевод"]) == {}
