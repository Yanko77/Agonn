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

        self.assertRaises(ValueError, lambda: manager.addBuff(StatBuff(StatBuffTypes.FLAT_BONUS, 10, 0), "charisma"))

        manager.addStat(Stat("charisma"))

        b = StatBuff(StatBuffTypes.FLAT_BONUS, 10, 1)
        manager.addBuff(b, "charisma")

        self.assertEqual(manager.getBuffList("charisma"), [b])

        b2 = StatBuff(StatBuffTypes.FLAT_BONUS, 15, 2)
        manager.addBuff(b2, "charisma")

        self.assertEqual(manager.getBuffList("charisma"), [b2, b])

        b3 = StatBuff(StatBuffTypes.FLAT_BONUS, 20, 1)
        manager.addBuff(b3, "charisma")

        self.assertEqual(manager.getBuffList("charisma"), [b2, b, b3])

    def test_getValue(self):
        manager = StatsManager()

        # Without any buff
        s = Stat("charisma", value=10)
        manager.addStat(s)

        self.assertEqual(manager.getValue("charisma"), 10)

        # Add a buff
        b = StatBuff(StatBuffTypes.FLAT_BONUS, 5, prio=0)
        manager.addBuff(b, "charisma")

        self.assertEqual(manager.getValue("charisma"), 15)

        # Add a second buff
        b2 = StatBuff(StatBuffTypes.FLAT_BONUS, 5, prio=0)
        manager.addBuff(b2, "charisma")

        self.assertEqual(manager.getValue("charisma"), 20)

        # Add a third buff with specific prio value
        b3 = StatBuff(StatBuffTypes.MULTIPLIER, 2, prio=10)
        manager.addBuff(b3, "charisma")

        self.assertEqual(manager.getValue("charisma"), 30)

