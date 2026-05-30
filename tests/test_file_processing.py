from unittest.mock import Mock
from unittest.mock import patch

from src.file_processing import read_csv_transactions
from src.file_processing import read_excel_transactions


@patch("pandas.read_csv")
def test_read_csv_transactions_success(mock_read_csv):
    """Тест успешного чтения CSV"""
    mock_df = Mock()
    mock_df.to_dict.return_value = [{"id": 1, "amount": 100}]
    mock_read_csv.return_value = mock_df

    result = read_csv_transactions("fake.csv")
    assert result == [{"id": 1, "amount": 100}]
    mock_read_csv.assert_called_once_with("fake.csv")


@patch("pandas.read_csv")
def test_read_csv_transactions_file_not_found(mock_read_csv):
    """Тест: CSV файл не найден"""
    mock_read_csv.side_effect = FileNotFoundError
    result = read_csv_transactions("missing.csv")
    assert result == []


@patch("pandas.read_csv")
def test_read_csv_transactions_error(mock_read_csv):
    """Тест: ошибка при чтении CSV"""
    mock_read_csv.side_effect = Exception("Read error")
    result = read_csv_transactions("bad.csv")
    assert result == []


@patch("pandas.read_excel")
def test_read_excel_transactions_success(mock_read_excel):
    """Тест успешного чтения Excel"""
    mock_df = Mock()
    mock_df.to_dict.return_value = [{"id": 1, "amount": 200}]
    mock_read_excel.return_value = mock_df

    result = read_excel_transactions("fake.xlsx")
    assert result == [{"id": 1, "amount": 200}]
    mock_read_excel.assert_called_once_with("fake.xlsx")


@patch("pandas.read_excel")
def test_read_excel_transactions_file_not_found(mock_read_excel):
    """Тест: Excel файл не найден"""
    mock_read_excel.side_effect = FileNotFoundError
    result = read_excel_transactions("missing.xlsx")
    assert result == []


@patch("pandas.read_excel")
def test_read_excel_transactions_error(mock_read_excel):
    """Тест: ошибка при чтении Excel"""
    mock_read_excel.side_effect = Exception("Read error")
    result = read_excel_transactions("bad.xlsx")
    assert result == []
