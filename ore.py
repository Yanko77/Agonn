import random


class CrystalStats:
    """
    Represents the crystal stats of an object.

    6 stats (50 points to split):
    - INTELLIGENCE
    - POWER
    - DEXTERITY
    - CONSTITUTION
    - AGILITY
    - PERCEPTION
    """

    def __init__(self, statsl: list[int, int, int, int, int, int] = None):

        if statsl is None:
            statsl = [0, 0, 0, 0, 0, 0]

        (self.intelligence,
         self.power,
         self.dexterity,
         self.constitution,
         self.agility,
         self.perception) = statsl

    @property
    def list(self):
        return [self.intelligence, self.power, self.dexterity, self.constitution, self.agility, self.perception]

    def diff(self, other: 'CrystalStats') -> tuple[int]:
        """
        Returns the list of gaps between all stats of self and other.

        :param other: CrystalStats
        :return: tuple[int], the list of gaps
        """
        l1 = self.list
        l2 = other.list

        return tuple(l1[i] - l2[i] for i in range(len(l1)))

    def diff_value(self, other: 'CrystalStats') -> float:
        """
        Returns the difference value between self and other.
        It's calculated with the list of gaps between all stats.

        :param other: CrystalStats
        :return: float, the diff value
        """
        gaps_list = self.diff(other)

        res = 0
        for gap in gaps_list:
            close_bonus = -5 / (abs(gap) ** 0.9 + 1)
            res += abs(gap) + close_bonus

        return res

    def __repr__(self):
        return f"INT: {self.intelligence}\nPOW: {self.power}\nDEX: {self.dexterity}\nCONST: {self.constitution}\nAGI: {self.agility}\nPER: {self.perception}"


def random_stats() -> CrystalStats:
    """
    Returns a randomly selected CrystalStats object.
    :return: CrystalStats
    """
    rlist = [0] * 6
    for _ in range(50):
        i = random.randint(0, 5)
        rlist[i] += 1

    return CrystalStats(rlist)


# 50 points: INT, POWER, DEX, CONST, AGI, PERCEP
KNIGHT = CrystalStats((4, 10, 13, 13, 6, 4))
SORCERER = CrystalStats((10, 15, 5, 5, 6, 9))
ARCHER = CrystalStats((6, 9, 9, 5, 15, 6))


if __name__ == '__main__':
    s1 = CrystalStats([20, 12, 34, 7, 1, 0])
    s2 = CrystalStats([26, 10, 28, 10, 5, 20])
    s3 = CrystalStats([22, 10, 32, 9, 20, 20])

    print(s1.diff(s2))
    s1.diff_value(s2)
    s1.diff_value(s3)

    r = random_stats()
    print(r)

    types = (KNIGHT, SORCERER, ARCHER)
    l = [r.diff_value(t) for t in types]

    mini = min(l)
    print(l.index(mini))
    print(l)

