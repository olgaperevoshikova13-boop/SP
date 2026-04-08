
from typing import Union

def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Возвращает замаскированный номер карты"""
    card_number_str = str(card_number).replace(" ", "")

    if len(card_number_str) != 16:
        return "Неверный номер карты"

    return f"{card_number_str[:4]} {card_number_str[4:6]}** **** {card_number_str[-4:]}"


def get_mask_account(account: Union[str, int]) -> str:
    """Возвращает замаскированный номер счета"""

    account_str = str(account).replace(" ", "")

    if len(account_str) != 20:
        return "Неверный номер счета"

    return f"**{account_str[-4:]}"