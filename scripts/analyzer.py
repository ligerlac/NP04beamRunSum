import pandas as pd
from functools import cached_property
import math
import numpy as np
import abc


class Analyzer:
    def __init__(self, name='', unit='', time_stamp_column=0, value_column=1, rms_interval=30*60*1000, file_names=None):
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
        return [self.first_column[0] + i*self.rms_interval for i in range(self._n_intervals+1)]

    @cached_property
    def _interval_masks(self):
        masks = []
        for i in range(self._n_intervals):
            ms_0, ms_1 = [self._ms_interval_edges[i], self._ms_interval_edges[i+1]]
            masks.append(np.where((self.first_column >= ms_0) * (self.first_column < ms_1))[0])
        return masks

    def _get_ms_value_matrix_from_file(self, file_name):
        return pd.read_csv(file_name, sep=' ', header=None, usecols=[self.time_stamp_column, self.value_column]).values


class HeinzAnalyzer(Analyzer):

    @cached_property
    def time_stamps(self):
#        return pd.DatetimeIndex(self.first_column * 1000000)#.tz_localize("UTC").tz_convert("CET")
        return pd.DatetimeIndex(self.first_column * 1000000).shift(1, freq='H')


class TriggerAnalyzer(Analyzer):

    @cached_property
    def time_stamps(self):
        #return pd.DatetimeIndex(self.first_column).tz_localize("UTC").tz_convert("CET")
        return pd.DatetimeIndex(self.first_column).shift(1, freq='H')

    @cached_property
    def cum_val_array(self):
        return np.cumsum(self.val_array)

    def _get_ms_value_matrix_from_file(self, file_name):
        return pd.read_csv(file_name, sep=',', usecols=[self.time_stamp_column, self.value_column]).values


class DAQAnalyzer(Analyzer):
    def __init__(self, name='', unit='', time_stamp_column=0, value_column=1, category_column=2, rms_interval=30*60*1000, file_names=None):
        self.excluded_categories = []
        self.category_column = category_column
        super().__init__(name=name, unit=unit, time_stamp_column=time_stamp_column, value_column=value_column, rms_interval=rms_interval, file_names=file_names)

    def _get_ms_value_matrix_from_file(self, file_name):
        return pd.read_csv(file_name, sep=',', usecols=[self.time_stamp_column, self.value_column, self.category_column]).values

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
        #return pd.DatetimeIndex(self.first_column).tz_localize("UTC").tz_convert("CET")
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