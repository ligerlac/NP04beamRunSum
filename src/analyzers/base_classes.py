import pandas as pd
from functools import cached_property
import numpy as np
import abc
from utils.intervalhandler import IntervalHandler

class GeneralAnalyzer:
    def __init__(self, file_names=None):
        self.file_names = file_names

    @abc.abstractmethod
    def _get_data_frame_from_file(self, fn):
        return pd.Dataframe()

    @abc.abstractmethod
    def _modify_data_frame(self, df):
        pass

    def _get_shift_data_frame(self, data_frame):
        data_frame['timestamp'] = pd.to_datetime(data_frame.index)#.shift(1, freq='H')
        return data_frame.set_index('timestamp')

    @cached_property
    def data_frame(self):
        df = pd.concat([self._get_data_frame_from_file(fn) for fn in self.file_names], axis=0)
        self._modify_data_frame(df)
        return self._get_shift_data_frame(df)


class IntervalAnalyzer(GeneralAnalyzer):
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
        return IntervalHandler(self.interval, self.data_frame.index[0], self.data_frame.index[-1])