__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import pandas as pd


def get_streamer_intervals(df):
    streamer_intervals = []
    df = df.loc[df['nvolt'] * df['ncurr'] != 0]
    streamer_on = False
    for row in df.itertuples(index=True, name='Pandas'):
        if streamer_on:
            if row.stable:
                streamer_on = False
                b = row.Index + pd.Timedelta(2, "s")
                if len(streamer_intervals) != 0 and streamer_intervals[-1][1] > a:
                    streamer_intervals[-1][1] = b
                else:
                    streamer_intervals.append([a, b])
        else:
            if not row.stable:
                streamer_on = True
                a = row.Index - pd.Timedelta(2, "s")
    return streamer_intervals
