import pandas as pd
from functools import cached_property
import math
import numpy as np
import abc


class Analyzer:
    def __init__(self, name='', unit='', time_stamp_column=0, value_column=1, rms_interval=30 * 60 * 1000,
                 file_names=None):
        self.name = name
        self.unit = unit
        self.time_stamp_column = time_stamp_column
        self.value_column = value_column
        self.rms_interval = rms_interval
        self.file_names = file_names

    @cached_property
    def val_array(self):
        return self._raw_matrix[:, 1]

    @cached_property
    def first_column(self):
        return self._raw_matrix[:, 0]

    @abc.abstractmethod
    def time_stamps(self):
        pass

    @cached_property
    def val_std_array(self):
        return np.array([np.std(self.val_array[m]) for m in self._interval_masks])

    @cached_property
    def ms_std_array(self):
        return self.first_column[[m[0] for m in self._interval_masks]]

    @cached_property
    def interval_time_stamps(self):
        #        return self.time_index[[int(np.median(m)) for m in self._interval_masks]]
        return self.time_stamps[[int(np.median(m)) for m in self._interval_masks]]

    @cached_property
    def _raw_matrix(self):
        return np.concatenate([self._get_ms_value_matrix_from_file(f) for f in self.file_names])

    @cached_property
    def _n_intervals(self):
        return math.ceil((self.first_column[-1] - self.first_column[0]) / self.rms_interval)

    @cached_property
    def _ms_interval_edges(self):
        return [self.first_column[0] + i * self.rms_interval for i in range(self._n_intervals + 1)]

    @cached_property
    def _interval_masks(self):
        masks = []
        for i in range(self._n_intervals):
            ms_0, ms_1 = [self._ms_interval_edges[i], self._ms_interval_edges[i + 1]]
            masks.append(np.where((self.first_column >= ms_0) * (self.first_column < ms_1))[0])
        return masks

    def _get_ms_value_matrix_from_file(self, file_name):
        return pd.read_csv(file_name, sep=' ', header=None, usecols=[self.time_stamp_column, self.value_column]).values


class TriggerAnalyzer_depr(Analyzer):

    @cached_property
    def time_stamps(self):
        # return pd.DatetimeIndex(self.first_column).tz_localize("UTC").tz_convert("CET")
        return pd.DatetimeIndex(self.first_column).shift(1, freq='H')

    @cached_property
    def cum_val_array(self):
        return np.cumsum(self.val_array)

    def _get_ms_value_matrix_from_file(self, file_name):
        return pd.read_csv(file_name, sep=',', usecols=[self.time_stamp_column, self.value_column]).values


class DAQAnalyzer_depr(Analyzer):
    def __init__(self, name='', unit='', time_stamp_column=0, value_column=1, category_column=2,
                 rms_interval=30 * 60 * 1000, file_names=None):
        self.excluded_categories = []
        self.category_column = category_column
        super().__init__(name=name, unit=unit, time_stamp_column=time_stamp_column, value_column=value_column,
                         rms_interval=rms_interval, file_names=file_names)

    def _get_ms_value_matrix_from_file(self, file_name):
        return pd.read_csv(file_name, sep=',',
                           usecols=[self.time_stamp_column, self.value_column, self.category_column]).values

    @cached_property
    def sorted_column_indices(self):
        l = [self.time_stamp_column, self.value_column, self.category_column]
        l.sort()
        return l

    @cached_property
    def category_array(self):
        return self._raw_matrix[:, self.sorted_column_indices.index(self.category_column)]

    @cached_property
    def value_array(self):
        return self._raw_matrix[:, self.sorted_column_indices.index(self.value_column)]

    @cached_property
    def ts_array(self):
        return self._raw_matrix[:, self.sorted_column_indices.index(self.time_stamp_column)]

    @cached_property
    def time_stamps(self):
        # return pd.DatetimeIndex(self.first_column).tz_localize("UTC").tz_convert("CET")
        return pd.DatetimeIndex(self.ts_array).shift(1, freq='H')

    @cached_property
    def data_frame(self):
        return pd.DataFrame({"category": self.category_array, "value": self.value_array}, index=self.time_stamps)

    @cached_property
    def cum_val_array(self):
        return np.cumsum(self.filtered_data_frame.value)

    @cached_property
    def filtered_time_stamps(self):
        return self.filtered_data_frame.index

    @cached_property
    def filtered_data_frame(self):
        filtered = self.data_frame.loc[self.data_frame.index < pd.to_datetime(self.upper_ts_limit, utc=True)]
        for excluded_cat in self.excluded_categories:
            filtered = filtered[self.data_frame.category != excluded_cat]
        return filtered


class IntervalHandler:
    def __init__(self, interval, first_ts, last_ts):
        self.interval = interval
        self.first_ts = first_ts
        self.last_ts = last_ts

    @cached_property
    def n(self):
        return math.ceil((self.last_ts - self.first_ts) / self.interval)

    @cached_property
    def edges(self):
        return [self.first_ts + i * self.interval for i in range(self.n + 1)]

    @cached_property
    def mean_time_stamps(self):
        return [self.edges[i] + self.interval / 2 for i in range(self.n)]


class GeneralAnalyzer:
    def __init__(self, interval=pd.Timedelta(30, "m"), file_names=None):
        self.interval = interval
        self.file_names = file_names

    @abc.abstractmethod
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=1, usecols=[1, 3, 4], names=['cat', 'timestamp', 'trig_count'])

    def _modify_data_frame(self, df):
        return df

    def _shift_data_frame(self, data_frame):
        data_frame['timestamp'] = pd.to_datetime(data_frame.index).shift(1, freq='H')
        return data_frame.set_index('timestamp')

    @cached_property
    def interval_handler(self):
        return IntervalHandler(self.interval, self.data_frame.index[0], self.data_frame.index[-1])

    @cached_property
    def data_frame(self):
        df = pd.concat([self._get_data_frame_from_file(fn) for fn in self.file_names], axis=0)
        df = self._modify_data_frame(df)
        return self._shift_data_frame(df)

    @cached_property
    def interval_data_frames(self):
        n, edges = [self.interval_handler.n, self.interval_handler.edges]
        return [self.data_frame.loc[edges[i]:edges[i + 1]] for i in range(n)]

    @cached_property
    def val_std_array(self):
        return np.array([np.std(df) for df in self.interval_data_frames])


class HeinzAnalyzer(GeneralAnalyzer):
    def _get_data_frame_from_file(self, fn):
        df = pd.read_csv(fn, sep=' ', index_col=0, usecols=[0, 1], names=['timestamp', 'curr'])
        return df

    def _modify_data_frame(self, df):
        df.index = 1000000 * df.index
        return df


class TriggerAnalyzer(GeneralAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=0, usecols=[0, 2], names=['timestamp', 'trig_count'], header=0)

    def _modify_data_frame(self, df):
        df['trig_count_sum'] = np.cumsum(df['trig_count'])
        return df


class DAQAnalyzer(GeneralAnalyzer):
    def __init__(self, interval=pd.Timedelta(30, "m"), file_names=None, excl_cats=None, upper_ts=pd.to_datetime("2018-11-12 10:00:00", utc=True)):
        super().__init__(interval, file_names)
        self.excl_cats = excl_cats
        self.upper_ts = upper_ts

    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=1, usecols=[1, 3, 4], names=['cat', 'timestamp', 'trig_count'],
                           parse_dates=True)

    def _modify_data_frame(self, df):
        df = df[~df['cat'].isin(self.excl_cats)]
        df = df.loc[df.index < self.upper_ts]
        df['trig_count_sum'] = np.cumsum(df['trig_count'])
        return df


class LifeTimeAnalyzer(GeneralAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=0, usecols=[0, 1], names=['timestamp', 'lifetime'], header=0)

    def _modify_data_frame(self, df):
        df['contamination'] = 0.3/df['lifetime']
        return df



