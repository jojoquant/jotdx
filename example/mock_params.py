from enum import Enum


class Interval(Enum):
    """
    Interval of bar data.
    """
    MINUTE = "1m"
    #####################
    # fangyang add
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    MINUTE_30 = "30m"
    #####################
    HOUR = "1h"
    DAILY = "d"
    WEEKLY = "w"
    TICK = "tick"


Interval_to_frequency_dict = {
    Interval.MINUTE: 8,
    Interval.MINUTE_5: 0,
    Interval.MINUTE_15: 1,
    Interval.MINUTE_30: 2,
    Interval.HOUR: 3,
    Interval.DAILY: 4,
    Interval.WEEKLY: 5,
}