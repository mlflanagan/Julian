#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit tests

instruction statement format: [Label:] [subleq] a b [address] [; comment]
data statement format: label: <.byte byte | .string ascii string> [; comment]

Example instruction statements
    ; whole line is a comment
    loop: subleq Z b 6 ; trailing comment
    loop: subleq Z b
    loop: Z b 6
    loop: Z b
    subleq Z b 6
    subleq Z b
    Z b 6
    Z b
    Z

Example data statements
    b: .byte 0
    Z: .byte 0
    hello: .string "Hello, world!"
"""

import unittest

import utils


class TestHoursMinutesSecondsVsDegrees(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_hms_to_degrees(self):
        self.assertEqual(utils.hms_to_degrees(0, 0, 0), 0.0)
        self.assertEqual(utils.hms_to_degrees(12, 0, 0), 180.0)
        self.assertEqual(utils.hms_to_degrees(24, 0, 0), 360.0)
        self.assertEqual(utils.hms_to_degrees(12, 12, 12), 183.05)

    def test_degrees_to_hms(self):
        self.assertEqual(utils.degrees_to_hms(0.0), (0, 0, 0.0))
        self.assertEqual(utils.degrees_to_hms(180.0), (12, 0, 0.0))
        self.assertEqual(utils.degrees_to_hms(258.741859), (17, 14, 58.04616))

    def tearDown(self) -> None:
        pass


class TestLeapYears(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_common_false(self):
        # common false leap years
        self.assertFalse(utils.is_leap(1900))
        self.assertFalse(utils.is_leap(2018))

    def test_leap_years(self):
        # list of leap years from https://www.thelists.org/list-of-leap-years.html
        for year in [
            1804, 1808, 1812, 1816, 1820, 1824, 1824, 1832, 1836, 1840,
            1844, 1848, 1852, 1856, 1860, 1864, 1868, 1872, 1876, 1880,
            1884, 1888, 1892, 1896, 1904, 1908, 1912, 1916, 1920, 1924,
            1928, 1932, 1936, 1940, 1944, 1948, 1952, 1956, 1960, 1964,
            1968, 1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004,
            2008, 2012, 2016, 2020, 2024, 2028, 2032, 2036, 2040, 2044,
            2048, 2052, 2056, 2060, 2064, 2068, 2072, 2076, 2080, 2084,
            2088, 2092, 2096,
        ]:
            self.assertTrue(utils.is_leap(year))

    def tearDown(self) -> None:
        pass


class TestDayFraction(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_all_zeros(self):
        self.assertEqual(utils.day_fraction(0, 0, 0, 0), 0.0)

    def test_hours(self):
        self.assertEqual(utils.day_fraction(1, 0, 0, 0), 1 / 24)  # 0.041666666666667
        self.assertEqual(utils.day_fraction(12, 0, 0, 0), 0.5)
        self.assertEqual(utils.day_fraction(24, 0, 0, 0), 1)
        self.assertEqual(utils.day_fraction(25, 0, 0, 0), 1 + 1 / 24)  # 1.041666666666667

    def test_minutes(self):
        self.assertEqual(utils.day_fraction(0, 1, 0, 0), 1 / 1440)
        self.assertEqual(utils.day_fraction(0, 30, 0, 0), 30 / 1440)
        self.assertEqual(utils.day_fraction(0, 59, 0, 0), 59 / 1440)
        self.assertEqual(utils.day_fraction(0, 60, 0, 0), 60 / 1440)
        self.assertEqual(utils.day_fraction(0, 61, 0, 0), 61 / 1440)

    def test_seconds_and_millis(self):
        self.assertEqual(utils.day_fraction(0, 0, 1, 0), 1 / 86400)
        self.assertEqual(utils.day_fraction(0, 0, 1, 500), 1.5 / 86400)
        self.assertEqual(utils.day_fraction(0, 0, 1, 1000), 2 / 86400)

    def tearDown(self) -> None:
        pass


class TestIsJulian(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_around_Gregorian_calendar_change(self):
        # days immediately before and after the Gregorian calendar change
        self.assertTrue(utils.is_julian(1582, 10, 4))  # 1582 October 4
        self.assertFalse(utils.is_julian(1582, 10, 15))  # 1582 October 15

    def tearDown(self) -> None:
        pass


class TestJulianDay(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_julian_day(self):
        # very first Julian day in 4713 BC
        self.assertEqual(utils.julian_day(-4712, 1, 1.5), 0.00)

        # dates around 0 BC
        self.assertEqual(utils.julian_day(0, 12, 31.0), 1721422.5)
        self.assertEqual(utils.julian_day(1, 1, 0.5), 1721423.0)
        self.assertEqual(utils.julian_day(1, 1, 1.0), 1721423.5)
        self.assertEqual(utils.julian_day(1, 1, 1.5), 1721424.0)  # noon on Jan 1, 1 AD
        self.assertEqual(utils.julian_day(1, 1, 2.0), 1721424.5)

        # only one Julian day has passed even though the Gregorian calendar skipped Oct 4 - Oct 15
        self.assertEqual(utils.julian_day(1582, 10, 4), 2299159.50)  # 1582 October 4
        self.assertEqual(utils.julian_day(1582, 10, 15), 2299160.50)  # 1582 October 15

        # J2000.0 - start of epoch at noon on 2000 January 1 Terrestrial Time
        # (equivalent to January 1, 2000, 11:58:55.816 UTC)
        # Reference: https://en.m.wikipedia.org/wiki/Terrestrial_Time
        self.assertEqual(utils.julian_day(2000, 1, 1.5), 2451545.0)

        # Sputnik launch example from the Meeus book
        self.assertEqual(utils.julian_day(1957, 10, 4.81), 2436116.31)
        # right now, when I wrote this test
        self.assertEqual(utils.julian_day(
                         2020, 10, 26 + utils.day_fraction(17, 52, 21, 0)),
                         2459149.2446875)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    # prevent unittest from sorting class methods alphabetically
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()

    # To run only the tests in the specified classes:
    # suites_list = []
    # for test_class in [TestJulianDay]:  # run only the TestJulianDay tests
    #     suites_list.append(unittest.TestLoader().loadTestsFromTestCase(test_class))
    # results = unittest.TextTestRunner(verbosity=3).run(unittest.TestSuite(suites_list))
