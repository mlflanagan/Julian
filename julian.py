#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import math


def is_leap(year):
    """
    Return True if the year is a leap year.
    For the Julian calendar, the year must be divisible by four.
    For the Gregorian calendar, century years (end in '00') must _also_ be divisible by 400.
    """

    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def day_fraction(hours: int, minutes: int, seconds: int, milliseconds: int) -> float:
    """
    Return hours, minutes, seconds, and milliseconds as a decimal value
    """

    return hours / 24.0 + minutes / 1440.0 + (seconds + milliseconds / 1000.0) / 86400.0


def is_julian(year, month, day):
    """
    Return True if the given date is on the Julian calendar (i.e., before 1582 October 15).
    NOTE: The day following 1582 October 4 (Julian calendar) is 1582 October 15 (Gregorian calendar).
    The dates 5 October 1582 through 14 October 1582 never occurred.
    """

    # The python 'and' operator takes precedence over the 'or' operator
    return year < 1582 or year == 1582 and (month < 10 or month == 10 and day < 15)


def julian_day(year, month, day):
    """
    Reference: Meeus, Jean: Astronomical Algorithms Second Edition (1998).
    """

    # if the month is Jan or Feb, it is considered to be the 13th or 14th month
    # of the preceding year
    if month == 1 or month == 2:
        year -= 1
        month += 12

    if is_julian(year, month, day):
        b = 0
    else:  # Gregorian
        a = math.trunc(year / 100)
        b = 2 - a + math.trunc(a / 4)

    return math.trunc(365.25 * (year + 4716)) + math.trunc(30.6001 * (month + 1)) + day + b - 1524.5


def tests():
    # common false leap years
    assert is_leap(1900) is False
    assert is_leap(2018) is False

    # list of leap years from https://www.thelists.org/list-of-leap-years.html
    for year in [
        1804, 1808, 1812, 1816, 1820, 1824, 1824, 1832, 1836, 1840, 1844, 1848, 1852, 1856, 1860,
        1864, 1868, 1872, 1876, 1880, 1884, 1888, 1892, 1896, 1904, 1908, 1912, 1916, 1920, 1924,
        1928, 1932, 1936, 1940, 1944, 1948, 1952, 1956, 1960, 1964, 1968, 1972, 1976, 1980, 1984,
        1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 2024, 2028, 2032, 2036, 2040, 2044,
        2048, 2052, 2056, 2060, 2064, 2068, 2072, 2076, 2080, 2084, 2088, 2092, 2096,
    ]:
        assert is_leap(year) is True

    # all zeros
    assert day_fraction(0, 0, 0, 0) == 0.0

    # hours
    assert day_fraction(1, 0, 0, 0) == 1 / 24  # 0.041666666666667
    assert day_fraction(12, 0, 0, 0) == 0.5
    assert day_fraction(24, 0, 0, 0) == 1
    assert day_fraction(25, 0, 0, 0) == 1 + 1 / 24  # 1.041666666666667

    # minutes
    assert day_fraction(0, 1, 0, 0) == 1 / 1440
    assert day_fraction(0, 30, 0, 0) == 30 / 1440
    assert day_fraction(0, 59, 0, 0) == 59 / 1440
    assert day_fraction(0, 60, 0, 0) == 60 / 1440
    assert day_fraction(0, 61, 0, 0) == 61 / 1440

    # seconds + millis
    assert day_fraction(0, 0, 1, 0) == 1 / 86400
    assert day_fraction(0, 0, 1, 500) == 1.5 / 86400
    assert day_fraction(0, 0, 1, 1000) == 2 / 86400

    # days immediately before and after the Gregorian calendar change
    assert is_julian(1582, 10, 4) is True  # 1582 October 4
    assert is_julian(1582, 10, 15) is False  # 1582 October 15

    # very first Julian day in 4713 BC
    assert julian_day(-4712, 1, 1.5) == 0.00

    # dates around 0 BC
    assert julian_day(0, 12, 31.0) == 1721422.5
    assert julian_day(1, 1, 0.5) == 1721423.0
    assert julian_day(1, 1, 1.0) == 1721423.5
    assert julian_day(1, 1, 1.5) == 1721424.0  # noon on Jan 1, 1 AD
    assert julian_day(1, 1, 2.0) == 1721424.5

    # only one Julian day has passed even though the Gregorian calendar skipped Oct 4 - Oct 15
    assert julian_day(1582, 10, 4) == 2299159.50  # 1582 October 4
    assert julian_day(1582, 10, 15) == 2299160.50  # 1582 October 15

    # start of epoch at noon on 2000 January 1
    assert julian_day(2000, 1, 1.5) == 2451545.0

    # other notable dates
    assert julian_day(1957, 10, 4.81) == 2436116.31  # Sputnik launch example from the Meeus book
    assert julian_day(2020, 10, 26 + day_fraction(17, 52, 21, 0)) == 2459149.2446875  # today

    print("All tests passed")


# noinspection PyPep8Naming
def main():
    # get local date and time converted to utc
    dt_now = datetime.datetime.now(tz=datetime.timezone.utc)
    day = day_fraction(dt_now.hour, dt_now.minute, dt_now.second, dt_now.microsecond)
    print(julian_day(dt_now.year, dt_now.month, day))


if __name__ == '__main__':
    tests()
    main()
