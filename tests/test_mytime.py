######################################################################
# Copyright 2025 (c) Yanko Lemoine
#
# This program and the accompanying materials are made
# available under the terms of the Eclipse Public License 2.0
# which is available at https://www.eclipse.org/legal/epl-2.0/
#
# SPDX-License-Identifier: EPL-2.0
######################################################################


import unittest

from src.mytime import Hour, Date, round_to_quarter, random_hour

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
        self.assertFalse(h.is_between(Hour(10, 00), Hour(10, 29)))

        h2 = Hour(0, 30)
        self.assertTrue(h2.is_between(Hour(00, 00), Hour(1, 00)))
        self.assertTrue(h2.is_between(Hour(23, 00), Hour(1, 00)))
        self.assertFalse(h2.is_between(Hour(1, 00), Hour(00, 00)))
    
    def test_incr_hours(self):
        h = Hour(22, 30)

        
        self.assertEqual(h.incr_hours(0), h)
        self.assertEqual(h.incr_hours(1), Hour(23, 30))
        self.assertEqual(h.incr_hours(2), Hour(0, 30))
        self.assertEqual(h.incr_hours(2 + 24), Hour(0, 30))

        self.assertRaises(ValueError, lambda: h.incr_hours(-1))
    
    def test_incr_minutes(self):
        h = Hour(22, 30)

        self.assertEqual(h.incr_minutes(10), Hour(22, 40))
        self.assertEqual(h.incr_minutes(30), Hour(23, 00))
        self.assertEqual(h.incr_minutes(90), Hour(0, 0))
        self.assertEqual(h.incr_minutes(60*24), Hour(22, 30))

        self.assertRaises(ValueError, lambda: h.incr_minutes(-1))
    
    def test_add(self):
        h = Hour(10, 30)
        h2 = Hour(5, 20)

        self.assertEqual(h + h2, Hour(15, 50))
        self.assertEqual(h + h2, h2 + h)

        h3 = Hour(5, 50)

        self.assertEqual(h + h3, Hour(16, 20))
        self.assertEqual(h + h3, h3 + h)

        h4 = Hour(20, 0)

        self.assertEqual(h + h4, Hour(6, 30))
        self.assertEqual(h + h4, h4 + h)

        h5 = Hour(20, 50)

        self.assertEqual(h + h5, Hour(7, 20))
        self.assertEqual(h + h5, h5 + h)


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

class testFuncTools(unittest.TestCase):
    def test_round_to_quarter(self):
        h = Hour(10, 12)

        self.assertEqual(round_to_quarter(h), Hour(10, 15))

        h2 = Hour(23, 50)

        self.assertEqual(round_to_quarter(h2), Hour(23, 45))

        h3 = Hour(23, 59)

        self.assertEqual(round_to_quarter(h3), Hour(0, 0))
    
    def test_random_hour(self):
        h1 = Hour(10, 0)
        h2 = Hour(0, 10)

        for _ in range(10000):
            assert random_hour(h1, h2).is_between(h1, h2)