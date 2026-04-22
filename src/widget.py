
import re

from src.masks import get_mask_account
from src.masks import get_mask_card_number


def mask_account_card(account_card: str) -> str:

    """Обрабатывает информацию о картах и счетах"""
    type_card = " ".join(re.findall(r"\b[a-zA-Zа-яА-Я]+\b", account_card))
    nums_account = re.findall(r"\d+", account_card)
    nums_account_str = nums_account[0]
    len_nums_account_str = len(nums_account_str)
    if len_nums_account_str == 16:
        der_nums_account_str = get_mask_card_number(nums_account_str)
        return f"{type_card} {der_nums_account_str}"
    elif len_nums_account_str == 20:
        mask_account = get_mask_account(nums_account_str)
        return f"{type_card} {mask_account}"
    return "Неверный номер карты или счета"


def get_date(date: str) -> str:

    """Принимает один формат даты и возвращает более удобный формат"""
    return f"{date[8:10]}.{date[5:7]}.{date[0:4]}"


if __name__ == "__main__":
    result_two = get_date("2024-03-11T02:26:18.671407")
    print(result_two)

    result = mask_account_card("Счет 73654108430135874305")
    print(result)
