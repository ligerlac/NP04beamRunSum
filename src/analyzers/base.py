__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import pandas as pd
from functools import cached_property
import numpy as np
import abc
from utils import intervalhandler


class GeneralAnalyzer:
    """Wrapper class for pandas data frame"""
    def __init__(self, file_names=None):
        self.file_names = file_names

    @abc.abstractmethod
    def _get_data_frame_from_file(self, fn):
        return pd.Dataframe()

    @abc.abstractmethod
    def _get_modified_data_frame(self, df):
        return df

    def _get_shifted_data_frame(self, data_frame):
        data_frame['timestamp'] = pd.to_datetime(data_frame.index)#.shift(1, freq='H')
        return data_frame.set_index('timestamp')

    def _decorate_cols_in_sec(self, df, col_names):
        for col_name in col_names:
            df[f'{col_name}_s'] = df[col_name].astype('int64') / 10e8
        return df

    @cached_property
    def data_frame(self):
        df = pd.concat([self._get_data_frame_from_file(fn) for fn in self.file_names], axis=0)
        return self._get_modified_data_frame(df)

    def get_copy(self):
        return self.from_data_frame(self.data_frame)

    @classmethod
    def from_data_frame(cls, df):
        new_instance = cls()
        new_instance.data_frame = df
        return new_instance


class TimeStampedAnalyzer(GeneralAnalyzer):
    @cached_property
    def data_frame(self):
        df = pd.concat([self._get_data_frame_from_file(fn) for fn in self.file_names], axis=0)
        df = self._get_modified_data_frame(df)
        df['timestamp'] = pd.to_datetime(df.index)
        return df.set_index('timestamp')


class IntervalAnalyzer(TimeStampedAnalyzer):
    def __init__(self, file_names=None, interval=pd.Timedelta(30, "m")):
        super().__init__(file_names=file_names)
        self.interval = interval

    @cached_property
    def val_std_array(self):
        return np.array([np.std(df) for df in self.interval_data_frames])

    @cached_property
    def interval_data_frames(self):
        n, edges = [self.interval_handler.n, self.interval_handler.edges]
        return [self.data_frame.loc[edges[i]:edges[i + 1]] for i in range(n)]

    @cached_property
    def interval_handler(self):
        return intervalhandler.IntervalHandler(self.interval, self.data_frame.index[0],
                                               self.data_frame.index[-1])


class HeinzAnalyzer(IntervalAnalyzer):
    def __init__(self, interval=pd.Timedelta(30, "m"), file_names=None, val_name=None):
        super().__init__(interval=interval, file_names=file_names)
        self.val_name = val_name

    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=' ', index_col=0, usecols=[0, 1],
                           names=['timestamp', self.val_name])

    def _get_modified_data_frame(self, df):
        df.index = 1000000 * df.index
        return df


class CombinedAnalyzer:
    def __init__(self, analyzer_list=None):
        self.analyzer_list = analyzer_list
        self.resample_rate = 'S'

    def _get_data_frames(self):
        dfs = []
        for ana in self.analyzer_list:
            dfs.append(self._resample_value(ana))
            dfs.append(self._resample_count(ana))
        return dfs

    @abc.abstractmethod
    def _get_modified_data_frame(self, df):
        return df

    def _resample_value(self, ana):
        res = ana.data_frame.resample(self.resample_rate)[ana.val_name].sum()
        return pd.Series.to_frame(res).rename(columns={ana.val_name: 'sum'+ana.val_name})

    def _resample_count(self, ana):
        res = ana.data_frame.resample(self.resample_rate)[ana.val_name].count()
        return pd.Series.to_frame(res).rename(columns={ana.val_name: 'n'+ana.val_name})

    @cached_property
    def data_frame(self):
        df = pd.concat(self._get_data_frames(), axis=1)
        df = self._get_modified_data_frame(df)
        return df