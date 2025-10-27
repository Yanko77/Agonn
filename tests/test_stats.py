import unittest

from Agonn.src.stats import *

class TestStatManager(unittest.TestCase):

    def test_addStat(self):
        manager = StatsManager()

        s = Stat("charisma")
        manager.addStat(s)

        self.assertEqual(manager._dict.get("charisma"), s)
        self.assertEqual(manager._buffs_dict.get("charisma"), list())

        self.assertRaises(ValueError, lambda: manager.addStat(Stat("charisma")))
    
    def test_addBuff(self):
        manager = StatsManager()

        self.assertRaises(ValueError, lambda: manager.addBuff(StatBuff(StatBuffType.FLAT_BONUS, 10, 0), "charisma"))

        manager.addStat(Stat("charisma"))

        b = StatBuff(StatBuffType.FLAT_BONUS, 10, 1)
        manager.addBuff(b, "charisma")

        self.assertEqual(manager.getBuffList("charisma"), [b])

        b2 = StatBuff(StatBuffType.FLAT_BONUS, 15, 2)
        manager.addBuff(b2, "charisma")

        self.assertEqual(manager.getBuffList("charisma"), [b2, b])

        b3 = StatBuff(StatBuffType.FLAT_BONUS, 20, 1)
        manager.addBuff(b3, "charisma")

        self.assertEqual(manager.getBuffList("charisma"), [b2, b, b3])
