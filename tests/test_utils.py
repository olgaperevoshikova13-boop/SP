import json
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List

import pytest

from src.utils import load_transactions


@pytest.fixture
def temp_json_file(tmp_path: Path) -> Any:
    """Создаёт временный JSON-файл с данными"""

    def _create_file(data: Any, filename: str = "test.json") -> str:
        file_path = tmp_path / filename
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return str(file_path)

    return _create_file


def test_load_transactions_success(temp_json_file: Any) -> None:
    """Тест: файл существует и содержит список транзакций"""
    test_data: List[Dict[str, int]] = [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    file_path = temp_json_file(test_data)

    result = load_transactions(file_path)
    assert result == test_data
    assert isinstance(result, list)


def test_load_transactions_file_not_found() -> None:
    """Тест: файл не существует"""
    result = load_transactions("non_existent_file.json")
    assert result == []


def test_load_transactions_empty_file(tmp_path: Path) -> None:
    """Тест: пустой файл"""
    file_path = tmp_path / "empty.json"
    file_path.touch()

    result = load_transactions(str(file_path))
    assert result == []


def test_load_transactions_not_list(temp_json_file: Any) -> None:
    """Тест: файл содержит не список (словарь)"""
    test_data: Dict[str, str] = {"key": "value"}
    file_path = temp_json_file(test_data)

    result = load_transactions(str(file_path))
    assert result == []


def test_load_transactions_invalid_json(tmp_path: Path) -> None:
    """Тест: невалидный JSON"""
    file_path = tmp_path / "invalid.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('{invalid json}')

    result = load_transactions(str(file_path))
    assert result == []
