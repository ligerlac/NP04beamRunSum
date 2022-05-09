__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import pandas as pd


def _get_streamer_ts_list(df):
    df = df.loc[df['nvolt'] * df['ncurr'] != 0]
    df = df.loc[df['stable'] == False]
    streamer_ts_set = set()
    for row in df.itertuples(index=True, name='Pandas'):
        streamer_ts_temp = set([row.Index + i*pd.Timedelta(1, "s") for i in range(-2, 3)])
        streamer_ts_set = streamer_ts_set.union(streamer_ts_temp)
    streamer_ts_list = list(streamer_ts_set)
    streamer_ts_list.sort()
    return streamer_ts_list


def _get_streamer_intervals_from_ts_list(ts_list):
    streamer_intervals = []
    a = ts_list[0]
    for i in range(len(ts_list)-1):
        if ts_list[i+1] != ts_list[i] + pd.Timedelta(1, "s"):
            streamer_intervals.append([a, ts_list[i]])
            a = ts_list[i+1]
    streamer_intervals.append([a, ts_list[-1]])
    return streamer_intervals


def get_streamer_intervals(df):
    streamer_ts_list = _get_streamer_ts_list(df)
    return _get_streamer_intervals_from_ts_list(streamer_ts_list)

