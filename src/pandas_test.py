import pandas as pd
import numpy as np

fn = 'data/heinzCurr_2018-09-14.csv'
df = pd.read_csv(fn, sep=' ', index_col=0, usecols=[0, 1], names=['timestamp', 'curr'])
df['date'] = pd.to_datetime(df.index * 1000000)

df = df.loc[df['date']>pd.to_datetime('2018-09-14 00:06:02')]

fn = 'data/np04_hv_cut_periods.csv'
df_int = pd.read_csv(fn, sep=',', usecols=[0, 1], names=['begin', 'end'], parse_dates=[0, 1])
[df_int['begin_ts'], df_int['end_ts']] = [ding.values.astype(np.int64)/10e5 for ding in [df_int['begin'], df_int['end']]]
[df_int['begin_ts2'], df_int['end_ts2']] = [ding.values.astype('int64')/10e5 for ding in [df_int['begin'], df_int['end']]]
print(f'df=\n{df}')
print(f'df_int=\n{df_int}')

bin_tuples = []
for row in df_int.itertuples(index=True, name='Pandas'):
    bin_tuples.append((row.begin_ts, row.end_ts))
binning = pd.IntervalIndex.from_tuples(bin_tuples)

df["bin"] = pd.cut(df['date'], binning)
df["bin_ts"] = pd.cut(df.index, binning)


print(pd.to_datetime('2018-09-14 00:06:02') < pd.to_datetime('2018-09-14 00:06:01'))


print(df)