
import masks
import re

def mask_account_card(type_num):
    """Обрабатывает информацию о картах и счетах"""
    type = " ".join(re.findall(r"\b[a-zA-Zа-яА-Я]+\b", type_num))
    nums = re.findall(r"\d+", type_num)
    num = nums[0]
    len_num = len(num)
    if len_num == 16:
        der_nums = masks.get_mask_card_number(num)
        return f"{type} {der_nums}"
    elif len_num == 20:
        mask_account = masks.get_mask_account(num)
        return f"{type} {mask_account}"

result = mask_account_card("Счет 73654108430135874305")
print(result)

def get_date(date):
    """Принимает один формат даты и возвращает более удобный формат"""
    return f"{date[8:10]}.{date[5:7]}.{date[0:4]}"

result_two = get_date("2024-03-11T02:26:18.671407")
print(result_two)