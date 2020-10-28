#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Utility functions for astronomical calculations
Python 3.8
"""

import datetime
import math
from typing import Tuple

# CONSTANTS
DEGREES_PER_HOUR = 360 / 24
DEGREES_PER_MINUTE = 360 / 1440
DEGREES_PER_SECOND = 360 / 86400


def hms_to_degrees(hours: int, minutes: int, seconds: int) -> float:
    """
    Convert hours, minutes, seconds to degrees
    """
    return hours * DEGREES_PER_HOUR + minutes * DEGREES_PER_MINUTE + seconds * DEGREES_PER_SECOND


def degrees_to_hms(degrees: float) -> Tuple[int, int, float]:
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


# noinspection PyPep8Naming
def main():
    # get local date and time converted to utc
    dt_now = datetime.datetime.now(tz=datetime.timezone.utc)
    day = day_fraction(dt_now.hour, dt_now.minute, dt_now.second, dt_now.microsecond)
    # print(julian_day(dt_now.year, dt_now.month, day))

    # Greenwich Mean Sidereal Time (GMST) = 280.46061837 + 360.98564736629 * d
    # where d = UT days since J2000.0, including parts of a day.
    #
    # To get the sidereal time at your longitude, known as Local Mean
    # Sidereal Time, add your longitude in degrees, taking East as positive:
    # LMST = 280.46061837 + 360.98564736629 * d + Long
    # You must subtract multiples of 360 to bring the answer into the range 0 to 360.
    #
    # Example: Calculate the GMST on 1994 June 16th at 18h UT.
    # d = -2024.75000
    # GMST = 281.46061837 + -730905.68950490
    #      = -730624.22888653
    #
    # d = -2024.75000
    #
    # GMST = 280.46061837 + 360.98564736629 * d
    # print(f"Step 1: GMST = {GMST}")
    #
    # GMST /= 360
    # print(f"Step 2: GMST / 360 = {GMST}")
    #
    # GMST += int(round(-GMST, 0))
    # print(f"Step 3: Get positive fraction of 360 = {GMST}")
    #
    # GMST *= 360
    # print(f"Step 4: Multiply by 360 = {GMST} degrees")
    #
    # GMST = 175.771113474402
    #
    # # A sidereal day = 23h 56m 4.09053s, a difference of 3h 55.90947s per day
    # hpd = 24
    # # hpd = 23 + (56 / 60) + (4.09053 / 3600)  # 23.93445
    # decimal_hours = GMST * (hpd / 360)  # 24 / 360 = hours per degree
    # hours = math.floor(decimal_hours)
    #
    # decimal_minutes = (decimal_hours - hours) * 60
    # minutes = math.floor(decimal_minutes)
    #
    # decimal_seconds = (decimal_minutes - minutes) * 60
    # seconds = int(round(decimal_seconds))
    #
    # print(f"Step 5: Convert degrees to HH:MM:SS = {hours:02}:{minutes:02}:{seconds:02}")


if __name__ == '__main__':
    main()
