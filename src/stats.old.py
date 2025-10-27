import json


class Stat:

    def __init__(self,
                 manager: 'Stats',
                 name: str):
        self.manager = manager
        self.owner = manager.owner
        self.game = self.owner.game

        self.name = name

        self.formula = _parse_formula(self.manager.raw_data.get(self.name))
        self._old_formula_list = []

        self.buffs = {0: {}}  # Buffs are ordered by priority values: the higher the value, the sooner it will be
                              # applied to the formula when it calculated the stat value

    @property
    def value(self) -> int:
        """
        Returns stat value.
        """
        res_dict = {}

        formula = self._apply_buffs()
        code = f'res = round({formula})'

        exec(code, self.manager.locals(), res_dict)
        return res_dict['res']

    def _apply_buffs(self):
        formula = self.formula
        max_prio = max(self.buffs.keys())

        for prio in range(max_prio, -1, -1):
            buffs = self.buffs.get(prio, {})

            for buff in buffs.values():
                formula = buff.apply(formula)

        return formula

    def add(self, value: int, name='Unknown'):
        """
        Adds a bonus flat value.
        """
        assert type(value) is int, 'Stat object can only be added with int value'

        self.add_buff(StatBuff(self.game, name=name, formula=f"formula + {value}"))

    def add_buff(self, buff):
        if self.buffs.get(buff.prio) is None:
            self.buffs[buff.prio] = {}

        self.buffs[buff.prio][buff.id] = buff


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


class StatBuff:

    """
    >>> from game import Game
    >>> g = Game()

    >>> buff = StatBuff(g, 'name', 'formula * 5')

    >>> formula = 'self["INT"] + 5'
    >>> buff.apply(formula)
    '(self["INT"] + 5) * 5'
    """

    def __init__(self,
                 game: 'Game',
                 name: str,
                 formula: str = "formula",
                 prio: int = 0):
        self.name = name
        self.formula = formula

        self.prio = prio

        self.id = game.get_unique_id()

    def apply(self, formula: str) -> str:
        """
        Applies the buff to the formula.
        Returns the edited formula.
        """
        return self.formula.replace('formula', f"({formula})")


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