import pandas as pd
from functools import cached_property
import numpy as np
from analyzers.base_classes import GeneralAnalyzer, IntervalAnalyzer


class HeinzAnalyzer(IntervalAnalyzer):
    def __init__(self, interval=pd.Timedelta(30, "m"), file_names=None, val_name=None):
        super().__init__(interval=interval, file_names=file_names)
        self.val_name = val_name

    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=' ', index_col=0, usecols=[0, 1], names=['timestamp', self.val_name])

    def _modify_data_frame(self, df):
        df.index = 1000000 * df.index


class TriggerAnalyzer(GeneralAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=0, usecols=[0, 2], names=['timestamp', 'trig_count'], header=0)

    def _modify_data_frame(self, df):
        df['trig_count_sum'] = np.cumsum(df['trig_count'])


class DAQAnalyzer(GeneralAnalyzer):
    def __init__(self, file_names=None, excl_cats=None, upper_ts=pd.to_datetime("2018-11-12 10:00:00", utc=True)):
        super().__init__(file_names=file_names)
        self.excl_cats = excl_cats
        self.upper_ts = upper_ts

    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=1, usecols=[1, 3, 4], names=['cat', 'timestamp', 'trig_count'],
                           parse_dates=True)

    def _modify_data_frame(self, df):
        df = df[~df['cat'].isin(self.excl_cats)]
        df = df.loc[df.index < self.upper_ts]
        df['trig_count_sum'] = np.cumsum(df['trig_count'])


class LifeTimeAnalyzer(GeneralAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=0, usecols=[0, 1], names=['timestamp', 'lifetime'], header=0)

    def _modify_data_frame(self, df):
        df['contamination'] = 0.3/df['lifetime']


class EFieldAnalyzer(GeneralAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=' ', index_col=0, usecols=[0, 1], names=['timestamp', 'efield'], header=0)


class CombinedHeinzAnalyzer:
    def __init__(self, analyzer_list=None):
        self.analyzer_list = analyzer_list
        self.resample_rate = 'S'

    def _get_data_frames(self):
        dfs = []
        for ana in self.analyzer_list:
            dfs.append(self._resample_value(ana))
            dfs.append(self._resample_count(ana))
        return dfs

    def _resample_value(self, ana):
        res = ana.data_frame.resample(self.resample_rate)[ana.val_name].sum()
        return pd.Series.to_frame(res).rename(columns={ana.val_name: 'sum'+ana.val_name})

    def _resample_count(self, ana):
        res = ana.data_frame.resample(self.resample_rate)[ana.val_name].count()
        return pd.Series.to_frame(res).rename(columns={ana.val_name: 'count'+ana.val_name})

    @cached_property
    def data_frame(self):
        return pd.concat(self._get_data_frames(), axis=1)











