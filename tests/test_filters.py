from src.filters import filter_by_description


def test_filter_by_description_found():
    data = [{"description": "Перевод организации"}, {"description": "Перевод с карты"}]
    result = filter_by_description(data, "Перевод")
    assert len(result) == 2


def test_filter_by_description_not_found():
    data = [{"description": "Перевод организации"}]
    result = filter_by_description(data, "Оплата")
    assert result == []


def test_filter_by_description_case_insensitive():
    data = [{"description": "перевод организации"}]
    result = filter_by_description(data, "Перевод")
    assert len(result) == 1


def test_filter_by_description_empty_list():
    assert filter_by_description([], "test") == []
