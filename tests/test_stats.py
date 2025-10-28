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
    
    def test_addStatWithRel(self):
        manager = StatsManager()

        s1 = Stat("charisma", formula="10")
        manager.addStat(s1)

        s2 = Stat("dexterity", formula="`charisma` * 1.5")
        manager.addStat(s2)

        self.assertEqual(manager.rel_register.getRelList(s2.name), {"charisma"}) 

        s3 = Stat("wisdom", formula="`charisma` * 2 + `dexterity` + 5")
        manager.addStat(s3)

        self.assertEqual(manager.rel_register.getRelList(s3.name), {"charisma", "dexterity"})
    
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

    def test_getValueWithoutRel(self):
        manager = StatsManager()

        # Without any buff
        s = Stat("charisma", formula="10")
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

    def test_getValueWithRel(self):
        manager = StatsManager()

        s0 = Stat("wisdom", "7 + `charisma` + `dexterity`")
        s1 = Stat("charisma", "10 + `dexterity`")
        s2 = Stat("dexterity", formula="5")

        manager.addStat(s2)
        manager.addStat(s1)
        manager.addStat(s0)

        # Without any buff
        self.assertEqual(manager.getValue("dexterity"), 5)
        self.assertEqual(manager.getValue("charisma"), 10 + 5)
        self.assertEqual(manager.getValue("wisdom"), 7 + 10 + 5 + 5)

        # With buffs
        b1 = StatBuff(StatBuffTypes.FLAT_BONUS, 3)
        manager.addBuff(b1, "dexterity")

        self.assertEqual(manager.getValue("dexterity"), 8)
        self.assertEqual(manager.getValue("charisma"), 10 + 8)
        self.assertEqual(manager.getValue("wisdom"), 7 + 10 + 8 + 8)

        b2 = StatBuff(StatBuffTypes.MULTIPLIER, 2)
        manager.addBuff(b2, "charisma")

        self.assertEqual(manager.getValue("dexterity"), 8)
        self.assertEqual(manager.getValue("charisma"), (10 + 8) * 2)
        self.assertEqual(manager.getValue("wisdom"), 7 + (10 + 8) * 2 + 8)
