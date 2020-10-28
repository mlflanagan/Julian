#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions for astronomical calculations
Python 3.8
"""

import math
from typing import Tuple

# CONSTANTS
DEGREES_PER_HOUR = 360 / 24
DEGREES_PER_MINUTE = 360 / 1440
DEGREES_PER_SECOND = 360 / 86400


def time_to_angle(hours: int, minutes: int, seconds: float) -> float:
    """
    Convert hours, minutes, seconds to degrees
    """
    return round(hours * DEGREES_PER_HOUR
                 + minutes * DEGREES_PER_MINUTE
                 + seconds * DEGREES_PER_SECOND, 6)


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


def sidereal_time(year: int, month: int, day: int, hours: int, minutes: int, seconds: float, longitude: float) -> float:
    """
    Return sidereal time for given year, month, day, hours, minutes, seconds and longitude.
    Accepts partial days (e.g., 1.5 for noon on the 1st of a month).
    TODO: Accept a datetime struct
    Reference: www.dept.aoe.vt.edu/~cdhall/courses/aoe4134/13LocalSiderealTime.pdf
    """

    # get julian date
    jd = julian_day(year, month, day)  # 2452248.5

    # calculate the Greenwich sidereal time at the beginning of the day of interest
    t_ut1 = round((jd - 2451545.0) / 36525, 8)  # 0.01926078

    # Calculate Greenwich Sidereal Time with:
    #   GST = 100.4606184 + 36000.77005361 * t_ut1 + 0.00038793 * t_ut1**2 + 2.6e-8 * t_ut1**3
    # - drop the last term since it is negligible
    # - modulus to get it in the range 0-360
    # - round to some reasonable precision
    # 100.46 degrees = the value needed to make the expression yield the correct value for GMST at
    # 0h UT on 1 January 2000.
    gst = (100.4606184 + 36000.77005361 * t_ut1 + 0.00038793 * t_ut1**2) % 360
    gst = round(gst, 7)  # 73.8635304

    # account for time of day
    # a sidereal day is 23 hours, 56 minutes, 4.09053 seconds, or 1436.0681755 minutes
    # 360 / 1436.0681755 = 0.250684477340122 degrees / day (this guy's precision is a little better than mine)
    degrees_per_minute = 0.25068447733746215
    gst += round(degrees_per_minute * (hours * 60 + minutes + seconds / 60), 7)

    # calculate LST by adding the longitude
    lst = round(gst + longitude, 7)

    return lst


print(sidereal_time(2001, 12, 5, 18, 45, 30, -80.408333))  # 275.600766 deg
