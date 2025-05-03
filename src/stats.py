import json

from varname import varname

_ALLOWED_C = {'+', '-', '*', '/', '//', '%', ' ', '(', ')', '.'}


class Stat:

    def __init__(self,
                 manager: 'Stats'):
        self.manager = manager
        self.owner = manager.owner

        self.name = _get_name()  # stat name = name of the variable the stat object got affected to

        try:
            self.formula = _parse(get_formula(self.name, self.owner.name))
        except AssertionError:
            self.formula = ""
        self._old_formula_list = []

        self.flat_bonus = 0


    @property
    def value(self) -> int:
        """
        Returns stat value.
        """
        res_dict = {}
        code = f'res = round({self.formula} + {self.flat_bonus})'

        exec(code, self.manager.locals(), res_dict)
        return res_dict['res']

    def edit_formula(self, adding: str):
        """
        Edits the formula by adding ``adding`` at this end.
        The added part will always be calculated after the orignal formula

        :param adding: the part to add
        """
        self._old_formula_list.append(self.formula)

        self.formula = f"({self.formula}) {adding}"

    def back_to_previous_formula(self):
        """
        Edits the formula so it become again the previous formula.
        It is useful when we want to do time limited stats buffs.
        """
        assert len(self._old_formula_list) > 0, f"No previous formula for '{self.name}'"

        self.formula = self._old_formula_list.pop()


    def __add__(self, value: int):
        """
        Adds a bonus flat value.
        """
        assert type(value) is int, 'Stat object can only be added with int value'

        self.flat_bonus += value
        return self


def _parse(formula: str = ''):
    res = ''

    word = ""
    for c in formula:
        if c.isdigit() or c in _ALLOWED_C:
            if word:
                res += f"self['{word}']"
                word = ""

            res += c
        else:
            word += c

    if word:
        res += f"self['{word}']"

    return res


def _get_name() -> str:
    """
    Used in Stat class __init__ method to get its name.
    Returns the stat name.

    It uses varname with frame=2.

    :return: str
    """
    name = varname(2)

    if name.startswith('self.'):
        name = name[5:]

    return name


def get_formula(stat_name: str, owner_name: str):
    with open('stats.json', 'r') as file:
        res = json.load(file)[owner_name].get(stat_name)

        assert res is not None, f'Unknown stat : "{stat_name}"'

        return res

