import logging
from typing import Union

# Настройка логгера для masks
logger_masks = logging.getLogger("masks")
logger_masks.setLevel(logging.DEBUG)

file_handler_masks = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler_masks.setLevel(logging.DEBUG)

formatter_masks = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler_masks.setFormatter(formatter_masks)

logger_masks.addHandler(file_handler_masks)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    try:
        card_str = str(card_number)
        if len(card_str) != 16 or not card_str.isdigit():
            error_msg = "Неверный номер карты"
            logger_masks.error(f"{error_msg}: {card_str}")
            return error_msg

        masked = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[12:]}"
        logger_masks.info(f"Успешно замаскирован номер карты: {card_str} -> {masked}")
        return masked
    except Exception as e:
        logger_masks.error(f"Ошибка при маскировке номера карты: {e}")
        return "Неверный номер карты"


def get_mask_account(account_number: Union[str, int]) -> str:
    try:
        account_str = str(account_number)
        if len(account_str) != 20 or not account_str.isdigit():
            error_msg = "Неверный номер счета"
            logger_masks.error(f"{error_msg}: {account_str}")
            return error_msg

        masked = f"**{account_str[-4:]}"
        logger_masks.info(f"Успешно замаскирован номер счета: {account_str} -> {masked}")
        return masked
    except Exception as e:
        logger_masks.error(f"Ошибка при маскировке номера счета: {e}")
        return "Неверный номер счета"
