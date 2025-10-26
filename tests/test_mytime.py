import unittest

from Agonn.src.mytime import *

class TestHour(unittest.TestCase):
    def test_init_w_str(self):
        # Test on 10h50 (string)
        h1 = Hour("10:50")

        self.assertEqual(h1.hours, 10)
        self.assertEqual(h1.minutes, 50)

        # Test on incorrect string -> Raises ValueError
        bad_strings = [
            "24:30",
            "10:60",
            "10",
            "a:a",
            "a:10",
            "10:a",
            ""
        ]
        for string in bad_strings:
            self.assertRaises(ValueError, lambda: Hour(string))
    
    def test_init_w_int(self):
        # Test on 10h50 (integers)
        h2 = Hour(10, 50)

        self.assertEqual(h2.hours, 10)
        self.assertEqual(h2.minutes, 50)

        # Test on bad values
        bad_values = [
            (10, 60),
            (24, 10),
            (10, -1),
            (-1, 10),
        ]
        for h_val, min_val in bad_values:
            self.assertRaises(ValueError, lambda: Hour(h_val, min_val))

    def test_is_between(self):
        h = Hour(10, 30)

        self.assertTrue(h.is_between(Hour(10, 00), Hour(11, 00)))
        self.assertTrue(h.is_between(Hour(10, 30), Hour(11, 00)))
        self.assertTrue(h.is_between(Hour(10, 30), Hour(10, 30)))
        self.assertFalse(h.is_between(Hour(10, 00), Hour(10, 30)))

        h2 = Hour(0, 30)
        self.assertTrue(h2.is_between(Hour(00, 00), Hour(1, 00)))
        self.assertTrue(h2.is_between(Hour(23, 00), Hour(1, 00)))
        self.assertFalse(h2.is_between(Hour(1, 00), Hour(00, 00)))

class testDate(unittest.TestCase):
    def test_init(self):
        d = Date(1, Hour(10, 30))

        self.assertEqual(d.days, 1)
        self.assertEqual(d.hour, Hour(10, 30))

        self.assertRaises(ValueError, lambda: Date(-1, Hour(10, 20)))

    def test_is_between(self):
        d = Date(3, Hour(10, 30))

        self.assertTrue(d.is_between(
            Date(2, Hour(10, 30)),
            Date(4, Hour(10, 30))
        ))
        self.assertFalse(d.is_between(
            Date(4, Hour(10, 30)),
            Date(2, Hour(10, 30))
        ))
