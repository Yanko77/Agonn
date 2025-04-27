import json

_ALLOWED_C = {'+', '-', '*', '/', '//', '%', ' ', '(', ')'}


class Stat:

    def __init__(self,
                 owner,
                 name: str):
        self.owner = owner

        self.name = name
        self.formula = _parse(get_formula(self.name, self.owner.name))

        self.flat_bonus = 0

    @property
    def value(self):
        return exec(self.formula)


def _parse(formula: str = ''):
    res = ''

    word = ""
    for c in formula:
        if c.isdigit() or c in _ALLOWED_C:
            if word:
                res += f"self.{word}"
                word = ""

            res += c
        else:
            word += c

    return res


def get_formula(stat_name: str, owner_name: str):
    with open('stats.json', 'r') as file:
        return json.load(file)[owner_name][stat_name]

