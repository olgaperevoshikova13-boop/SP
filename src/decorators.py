import functools
import os
from typing import Any
from typing import Callable
from typing import Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функций.

    Args:
        filename: Опциональный путь к файлу для записи логов.
                 Если не указан, логи выводятся в консоль.

    Returns:
        Декоратор, оборачивающий функцию.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                _write_log(log_message, filename)
                return result
            except Exception as e:
                error_type = type(e).__name__
                log_message = f"{func.__name__} error: {error_type}. Inputs: {args}, {kwargs}"
                _write_log(log_message, filename)
                raise

        return wrapper

    return decorator


def _write_log(message: str, filename: Optional[str]) -> None:
    """
    Записывает сообщение в файл или выводит в консоль.

    Args:
        message: Сообщение для записи.
        filename: Путь к файлу. Если None, вывод в консоль.
    """
    if filename:
        os.makedirs(os.path.dirname(os.path.abspath(filename)) if os.path.dirname(filename) else '.', exist_ok=True)
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(message + '\n')
    else:
        print(message)
