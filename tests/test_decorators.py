from typing import Any

import pytest

from src.decorators import log


def test_log_success_to_console(capsys: Any) -> None:
    """Проверка логирования успешного выполнения функции в консоль"""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result = add(3, 5)

    assert result == 8
    captured = capsys.readouterr()
    assert captured.out.strip() == "add ok"


def test_log_error_to_console(capsys: Any) -> None:
    """Проверка логирования ошибки функции в консоль"""

    @log()
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "divide error: ZeroDivisionError" in captured.out
    assert "Inputs: (10, 0), {}" in captured.out


def test_log_with_kwargs_to_console(capsys: Any) -> None:
    """Проверка логирования функции с именованными аргументами"""

    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result = greet("Alice", greeting="Hi")

    assert result == "Hi, Alice!"
    captured = capsys.readouterr()
    assert captured.out.strip() == "greet ok"


def test_log_success_to_file(tmp_path: Any) -> None:
    """Проверка записи успешного выполнения в файл"""

    log_file = tmp_path / "test.log"

    @log(filename=str(log_file))
    def multiply(a: int, b: int) -> int:
        return a * b

    result = multiply(4, 7)

    assert result == 28
    assert log_file.exists()
    content = log_file.read_text().strip()
    assert content == "multiply ok"


def test_log_error_to_file(tmp_path: Any) -> None:
    """Проверка записи ошибки в файл"""

    log_file = tmp_path / "error.log"

    @log(filename=str(log_file))
    def divide(a: int, b: int) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    assert log_file.exists()
    content = log_file.read_text().strip()
    assert "divide error: ZeroDivisionError" in content
    assert "Inputs: (10, 0), {}" in content


def test_log_append_to_file(tmp_path: Any) -> None:
    """Проверка, что логи добавляются в конец файла, а не перезаписываются"""

    log_file = tmp_path / "append.log"

    @log(filename=str(log_file))
    def first_func() -> int:
        return 1

    @log(filename=str(log_file))
    def second_func() -> int:
        return 2

    first_func()
    second_func()

    content = log_file.read_text().strip().split('\n')
    assert len(content) == 2
    assert content[0] == "first_func ok"
    assert content[1] == "second_func ok"


def test_log_with_arguments_to_file(tmp_path: Any) -> None:
    """Проверка логирования функции с разными типами аргументов"""

    log_file = tmp_path / "args.log"

    @log(filename=str(log_file))
    def process(data: int, multiplier: int = 2, **kwargs: Any) -> int:
        return data * multiplier

    result = process(5, multiplier=3, extra="ignored")

    assert result == 15
    content = log_file.read_text().strip()
    assert content == "process ok"


def test_log_creates_directory_if_not_exists(tmp_path: Any) -> None:
    """Проверка, что декоратор создаёт папку для файла, если её нет"""

    log_file = tmp_path / "subdir" / "nested" / "test.log"

    @log(filename=str(log_file))
    def test_func() -> int:
        return 42

    test_func()

    assert log_file.exists()
    content = log_file.read_text().strip()
    assert content == "test_func ok"


def test_log_preserves_function_name() -> None:
    """Проверка, что декоратор сохраняет имя исходной функции"""

    @log()
    def my_special_function() -> None:
        pass

    assert my_special_function.__name__ == "my_special_function"


def test_log_preserves_docstring() -> None:
    """Проверка, что декоратор сохраняет документацию исходной функции"""

    @log()
    def documented_function(a: int, b: int) -> int:
        """Эта функция складывает два числа."""
        return a + b

    assert documented_function.__doc__ == "Эта функция складывает два числа."
