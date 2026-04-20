

def filter_by_state(list_of_dicts: list, state: str = 'EXECUTED') -> list[dict]:
    """Фильтрует список словарей по ключу 'state'"""
    new_list_of_dicts = []
    for item in list_of_dicts:
        if item["state"] == state:
            new_list_of_dicts.append(item)
    return new_list_of_dicts


if __name__ == "__main__":
    result = filter_by_state([
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ])
    print(result)


def sort_by_date(list_of_dicts: list, descending: bool = True) -> list[dict]:
    """Сортирует список словарей по дате"""
    return sorted(list_of_dicts, key=lambda item: item['date'], reverse=descending)


if __name__ == "__main__":
    result = sort_by_date([
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ])
    print(result)
