__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import pandas as pd
from datetime import datetime


def get_streamer_intervals(df, sideband=pd.Timedelta(2, "s")):
    # exactly reproducing kevin's results:
    # the sideband is actually (-2, +3) secs
    # also, intervals can overlap
    streamer_intervals = []
    df = df.loc[df['nvolt'] * df['ncurr'] != 0]
    streamer_on = False
    for row in df.itertuples(index=True, name='Pandas'):
        if streamer_on:
            if row.stable:
                streamer_on = False
                b = row.Index + sideband
#                if len(streamer_intervals) != 0 and streamer_intervals[-1][1] > a:
#                    streamer_intervals[-1][1] = b
#                else:
#                    streamer_intervals.append([a, b])
                streamer_intervals.append([a, b])
        else:
            if not row.stable:
                streamer_on = True
                a = row.Index - sideband
    if streamer_on:
        streamer_intervals.append([a, df.index[-1]])
    return streamer_intervals


def _get_streamer_ts_list(df):
    df_copy_dict = {}
    for i in range(-2, 3):
        df_copy_dict[i] = pd.DataFrame({str(i): df['stable'].copy()})
        df_copy_dict[i].index = pd.to_datetime(df_copy_dict[i].index).shift(i, freq='S')
    df_merge = pd.concat([_df for _df in df_copy_dict.values()], axis=1)
    print(f'df_merge =\n{df_merge}')
    df_merge['res'] = False
    print(f'df_merge =\n{df_merge}')
    df_merge['res'] = df.product(axis=1, skipna=True)

    print(f'df_merge =\n{df_merge}')
    print(f'returning {df_merge.loc[df_merge["res"]!=True].index}')
    print(f'with length {len(df_merge.loc[df_merge["res"]!=True].index)}')
    return df_merge.loc[df_merge['res']>1].index


def _get_streamer_intervals_from_ts_list(ts_list):
    streamer_intervals = []
    a = ts_list[0]
    for i in range(len(ts_list)-1):
        if ts_list[i+1] != ts_list[i] + pd.Timedelta(1, "s"):
            streamer_intervals.append([a, ts_list[i]])
            a = ts_list[i+1]
    streamer_intervals.append([a, ts_list[-1]])
    return streamer_intervals


def get_streamer_intervals_new(df):
    ### the vectorization of this method is tricky
    ### dataframe rows with no entries (NaN) can be
    ### streamer or stable, depending on previous
    ### values
    t_0 = datetime.now()
    streamer_ts_list = _get_streamer_ts_list(df)
    s_i = _get_streamer_intervals_from_ts_list(streamer_ts_list)
    print(f'get_streamer_intervals took {datetime.now()-t_0} sec')
    return s_i

