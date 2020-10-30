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
from datetime import datetime, timezone, timedelta

import utils


class TestTimeAndAngle(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_time_to_angle(self):
        self.assertEqual(utils.time_to_angle(0, 0, 0.0), 0.0)
        self.assertEqual(utils.time_to_angle(12, 0, 0.0), 180.0)
        self.assertEqual(utils.time_to_angle(24, 0, 0.0), 360.0)
        self.assertEqual(utils.time_to_angle(12, 12, 12.0), 183.05)
        # random time
        self.assertEqual(round(utils.time_to_angle(6, 42, 51.5354), 7), 100.7147308)
        # mean sidereal time at Greenwich at 0h UT
        self.assertEqual(round(utils.time_to_angle(6, 41, 50.54841), 7), 100.4606184)  # 100.46061837
        self.assertEqual(round(utils.time_to_angle(0, 0, 8640184.812866), 7), 36000.7700536)  # 36000.770053648
        self.assertEqual(round(utils.time_to_angle(0, 0, 0.093104), 7), 0.0003879)  # 0.000387933

    def test_angle_to_time(self):
        self.assertEqual(utils.angle_to_time(0.0), (0, 0, 0.0))
        self.assertEqual(utils.angle_to_time(180.0), (12, 0, 0.0))
        self.assertEqual(utils.angle_to_time(258.741859), (17, 14, 58.04616))

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


class TestMeanSiderealTime(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_mean_sidereal_time(self):
        # example in Meeus, page 89
        # TODO: This result differs slightly from Meeus, who gets 128.7378734;
        #  look for a rounding error
        self.assertEqual(utils.mean_sidereal_time(1987, 4, 10, 19, 21, 0), 128.73787324433215)

    def tearDown(self) -> None:
        pass


class TestLocalMeanTime(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_UTC(self):
        actual_result = utils.local_mean_time(datetime(2020, 10, 30, 0, 0, 0, 0, tzinfo=timezone.utc))
        time_delta = timedelta(hours=0)
        tz_obj = timezone(time_delta, name="UTC")
        expected_result = datetime(2020, 10, 30, 0, 0, 0, 0, tzinfo=tz_obj)
        self.assertEqual(actual_result, expected_result)

    def test_America_New_York(self):
        actual_result = utils.local_mean_time(datetime(2020, 10, 30, 0, 0, 0, 0, tzinfo=timezone.utc))
        time_delta = timedelta(hours=-4)  # TODO: may need to automate dst
        tz_obj = timezone(time_delta, name="EST")
        expected_result = datetime(2020, 10, 29, 20, 0, 0, 0, tzinfo=tz_obj)
        self.assertEqual(actual_result, expected_result)

    def tearDown(self) -> None:
        pass


class TestLocalStandardTime(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_America_New_York(self):
        actual_result = utils.local_standard_time(datetime(2020, 10, 30, 0, 0, 0, 0, tzinfo=timezone.utc), -74.346322)
        # only the hh:mm:ss matter, set tzinfo to avoid test failure
        expected_result = datetime(2020, 10, 29, 19, 2, 36, 882720, tzinfo=timezone.utc)
        self.assertEqual(actual_result, expected_result)

    def tearDown(self) -> None:
        pass


if __name__ == '__main__':
    # prevent unittest from sorting class methods alphabetically
    unittest.TestLoader.sortTestMethodsUsing = None
    unittest.main()

    # To run only the tests in the specified classes:
    # suites_list = []
    # for test_class in [TestLocalMeanTime]:  # e.g., run only the TestLocalMeanTime tests
    #     suites_list.append(unittest.TestLoader().loadTestsFromTestCase(test_class))
    # results = unittest.TextTestRunner(verbosity=3).run(unittest.TestSuite(suites_list))
