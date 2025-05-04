import json


class Stat:

    def __init__(self,
                 manager: 'Stats',
                 name: str):
        self.manager = manager
        self.owner = manager.owner

        self.name = name

        self.formula = _parse_formula(self.manager.raw_data.get(self.name))
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

    def add(self, value: int):
        """
        Adds a bonus flat value.
        """
        assert type(value) is int, 'Stat object can only be added with int value'

        self.flat_bonus += value


class Stats:
    """
    To read a stat value:
        Use ``__getitem__`` method

        Example:
            ```
            stats = Stats(..., ...)
            stats['knowledge']
            ```

    To access a stat:
        Use ``get`` method

        Example:
            ```
            stats = Stats(..., ...)
            stats.get('knowledge')
            ```

    To increments a stat:
        Use ``add`` method of Stat objects

        Example:
            ```
            stats = Stats(..., ...)
            knowledge = stats.get('knowledge')
            knowledge.add(10)  # Increments knowledge stat by 10 (flat value)
            ```
    """

    def __init__(self,
                 owner: 'Entity'):
        self.owner = owner

        self.raw_data = get_data(self.owner.class_name)

        stats_name_list = self.raw_data.keys()
        for stat_name in stats_name_list:
            setattr(self, stat_name, Stat(self, stat_name))

    def get(self, stat_name: str) -> Stat:
        """
        Returns the stat obj of self whose name is ``stat_name``.

        :param stat_name: str
        :return: Stat object
        """
        return self.__getattribute__(stat_name)

    def __getitem__(self, stat_name: str) -> int:
        """
        Returns the value of ``stat_name`` in self.
        """
        return self.get(stat_name).value

    def locals(self):
        """
        Returns locals variables of the class.
        """
        return locals()

    @property
    def list(self) -> tuple:
        return tuple(attr for attr in self.__dict__.values() if isinstance(attr, Stat))


def _parse_formula(formula: str = ''):
    _ALLOWED_C = '+-*/% ().'
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


def get_data(entity_class_name: str) -> dict[str, str]:
    """
    Returns all the stats data of the entity whose class name is ``entity_class_name``.
    :param entity_class_name: str
    :return: dict[str, str]
    """
    with open('stats.json', 'r') as file:
        res = json.load(file).get(entity_class_name)

        assert res is not None, f'Unknown entity: {entity_class_name}'

        return res