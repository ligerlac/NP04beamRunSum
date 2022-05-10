__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import pandas as pd


def format_fn(tick_val, tick_pos):
    # tick_val = contamination
    et = (1. / tick_val) * (0.1 * 3.)
    return "{0:0.1f}".format(et)


def minorFormat_fn(tick_val, tick_pos):
    # tick_val = contamination
    et = (1. / tick_val) * (0.1 * 3.)
    if tick_val in [0.05, 0.1, 0.5, 1., 5, ] and et > 0.1:
        return "{0:0.1f}".format(et)
    elif tick_val in [0.05, 0.1, 0.5, 1., 5, ] and et < 0.1:
        return "{0:0.2f}".format(et)
    else:
        return ''


def get_time_stamp_kevin(date_time):
    # this is necessary to reproduce kevin's results
    if date_time == pd.to_datetime("2018-10-17 11:59:58"):
        return int(date_time.timestamp() - 7200)
    summer_begin = pd.to_datetime(f"2018-03-25 02:00:00")
    summer_end = pd.to_datetime(f"2018-10-28 03:00:00")
    if summer_begin < date_time < summer_end:
        return int(date_time.timestamp() - 3600)
    else:
        return int(date_time.timestamp())
