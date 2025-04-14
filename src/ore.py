import random


class CrystalStats:
    """
    Represents the crystal stats of an object.

    7 stats (100 points to split):
    - INTELLIGENCE
    - STRENGTH
    - POWER
    - DEXTERITY
    - CONSTITUTION
    - AGILITY
    - PERCEPTION
    """

    PTS = 100

    def __init__(self, statsl: list[int] = None):
        assert len(statsl) == 7, "Needs 7 values to unpack"
        assert sum(statsl) == self.PTS, f"Sum of the 7 values has to be equal to {self.PTS} : {sum(statsl)}"

        if statsl is None:
            statsl = [0, 0, 0, 0, 0, 0, 0]

        (self.intelligence,
         self.strength,
         self.power,
         self.dexterity,
         self.constitution,
         self.agility,
         self.perception) = statsl

    @property
    def list(self):
        return [self.intelligence, self.strength, self.power, self.dexterity, self.constitution, self.agility, self.perception]

    def diff(self, other: 'CrystalStats') -> tuple[float]:
        """
        Returns the list of similarity percentage between all stats of self and other.

        :param other: CrystalStats
        :return: tuple[int], the list of percentage
        """
        l1: list[int] = self.list
        l2: list[int] = other.list

        res = ()
        for i in range(len(l1)):
            gap = l1[i] - l2[i]
            if gap < 0:
                res += (l1[i] * 100 / l2[i],)
            else:
                res += (l2[i] / l1[i] * 100,)

        return res

    def diff_value(self, other: 'CrystalStats') -> float:
        """
        Returns the similarity percentage between self and other.

        :param other: CrystalStats
        :return: float, the similarity percentage
        """
        gaps_list = self.diff(other)

        res = 0
        for gap in gaps_list:
            res += gap

        return res / 7

    def __repr__(self):
        return f"CrystalStats({str(self.list)})"

def random_stats() -> CrystalStats:
    """
    Returns a randomly selected CrystalStats object.
    :return: CrystalStats
    """
    rlist = [0] * 7
    for _ in range(CrystalStats.PTS):
        i = random.randint(0, 6)
        rlist[i] += 1

    return CrystalStats(rlist)


# 50 points: INT, STRENGTH, POWER, DEX, CONST, AGI, PERCEP
KNIGHT = CrystalStats([8, 26, 8, 14, 26, 10, 8])
SORCERER = CrystalStats([16, 4, 32, 8, 14, 8, 18])
ARCHER = CrystalStats([12, 10, 8, 16, 8, 26, 20])


if __name__ == '__main__':
    '''s1 = CrystalStats([20, 12, 34, 7, 1, 0])
    s2 = CrystalStats([26, 10, 28, 10, 5, 20])
    s3 = CrystalStats([22, 10, 32, 9, 20, 20])

    print(s1.diff(s2))
    s1.diff_value(s2)
    s1.diff_value(s3)'''

    r = random_stats()
    print(r)

    types = (KNIGHT, SORCERER, ARCHER)
    l = [r.diff_value(t) for t in types]

    mini = max(l)
    print(l.index(mini))
    print(l)

