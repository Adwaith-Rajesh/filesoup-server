"""contains all the extra funcs file manger might need"""

from typing import List


def filter_list(_list: List[str]) -> List[str]:
    new_list = [i for i in _list if i]
    return new_list