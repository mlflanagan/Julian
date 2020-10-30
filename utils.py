#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions for astronomical calculations
Python 3.8
"""

import math
from typing import Tuple
import datetime

# CONSTANTS
DEGREES_PER_HOUR = 360 / 24
DEGREES_PER_MINUTE = 360 / 1440
DEGREES_PER_SECOND = 360 / 86400


def time_to_angle(hours: int, minutes: int, seconds: float) -> float:
    """
    Convert hours, minutes, seconds to degrees
    """
    return hours * DEGREES_PER_HOUR + minutes * DEGREES_PER_MINUTE + seconds * DEGREES_PER_SECOND


def angle_to_time(degrees: float) -> Tuple[int, int, float]:
    """
    Convert degrees to hours, minutes, seconds time tuple
    """
    hours: float = degrees / DEGREES_PER_HOUR
    minutes: float = (hours - math.floor(hours)) * 60
    seconds: float = (minutes - math.floor(minutes)) * 60
    seconds = round(seconds, 6)
    return int(hours), int(minutes), seconds


def is_leap(year: int) -> bool:
    """
    Return a boolean indicating whether the given year is a leap year.

    For the Julian calendar, the year must be divisible by four.
    For the Gregorian calendar, century years (end in '00') must _also_ be divisible by 400.
    """
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def day_fraction(hours: int, minutes: int, seconds: int, milliseconds: int) -> float:
    """
    Convert hours, minutes, seconds, and milliseconds into a fraction of a day.
    E.g., 12 hours, 0 minutes, 0 seconds, 0 millis = 0.5 day.
    TODO: Accept a time struct
    """
    return hours / 24.0 + minutes / 1440.0 + (seconds + milliseconds / 1000.0) / 86400.0


def is_julian(year: int, month: int, day: int) -> bool:
    """
    Return a boolean indicating whether the given date is on the Julian calendar (i.e., before
    1582 October 15).

    Note: The day following 1582 October 4 (Julian calendar) is 1582 October 15 (Gregorian
    calendar).  The dates 5 October 1582 through 14 October 1582 never occurred.
    """

    # NOTE: the python 'and' operator takes precedence over the 'or' operator
    return year < 1582 or year == 1582 and (month < 10 or month == 10 and day < 15)


def julian_day(year: int, month: int, day: float) -> float:
    """
    Return Julian day for the given year, month, day.
    Accepts partial days (e.g., 1.5 for noon on the first day of the month).
    Reference: Meeus, Jean: Astronomical Algorithms Second Edition (1998).
    """

    # if the date is in Jan or Feb, it is considered to be
    # the 13th or 14th month of the preceding year
    if month == 1 or month == 2:
        year -= 1
        month += 12

    if is_julian(year, month, int(day)):
        b = 0
    else:  # Gregorian
        a = math.trunc(year / 100)
        b = 2 - a + math.trunc(a / 4)

    jd = math.trunc(365.25 * (year + 4716)) + math.trunc(30.6001 * (month + 1)) + day + b - 1524.5

    return jd


def mean_sidereal_time(year: int, month: int, day: int,
                       hours: int, minutes: int, seconds: float) -> float:
    """
    Return Mean Sidereal Time _at Greenwich at 0hUT_
    Reference: Meeus, page 87
    """
    # calculate JD
    # millisecond = one 1000th (0.001) of a second
    milliseconds = int((seconds - math.floor(seconds)) * 1000)
    jd = julian_day(year, month, day + day_fraction(hours, minutes, int(seconds), milliseconds))
    # then find T with
    t = (jd - 2451545.0) / 36525
    # Mean Sidereal Time at Greenwich _at 0hUT_ is then given by the following expression adopted
    # by the International Astronomical Union in 1982:
    #   MST = 6h41m50.54841s + 8640184.812866 * T + 0.093104 * T**2 - 0.0000062 * T**3
    #
    # This formula can be expressed in degrees and decimals as:
    #   MST = 100.46061837 + 36000.770053608 * T + 0.000387933 * T**2 - T**3 / 38710000
    #
    # Multiply a time of day  by 1.00273790935 and add the result to MST at 0h UT to get sidereal
    # time at _a given instant_ of the day.
    #
    # The MST at Greenwich _for any instant_ can also be found directly with:
    #   280.46061837 + 360.98564736629 * (JD - 2451545.0) + 0.000387933 * T**2 - T**3 / 38710000
    mst = (280.46061837 + 360.98564736629 * (
            jd - 2451545.0) + 0.000387933 * t ** 2 - t ** 3 / 38710000) % 360
    return mst


def local_mean_time(utc_dt: datetime) -> datetime:
    """
    Return Local Mean Time given UTC.

    Basically just convert UTC to local time. Note that Local Mean Time is the time at the
    timezone meridian, i.e., the _average_ time in the local timezone.

    On average, timezones are 15 degrees wide, so the actual time in a timezone can vary by
    up to one hour. If you need the actual time at a specific longitude, use the
    local_standard_time function.
    """
    return utc_dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)


def local_standard_time(utc_dt: datetime, longitude: float) -> datetime:
    """
    Return datetime based on longitude offset from UTC.
    The earth takes four minutes to rotate one degree (24 * 60 / 360 = 4).
    So the time offset from UTC = longitude * 4 minutes per degree, given to timedelta in seconds.
    """
    return utc_dt + datetime.timedelta(seconds=longitude * 4 * 60)
