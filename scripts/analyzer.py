import pandas as pd
from functools import cached_property
import math
import numpy as np


class Analyzer:
    def __init__(self, name='', unit='', value_column=1, rms_interval=30*60*1000, file_names=None):
        self.name = name
        self.unit = unit
        self.value_column = value_column
        self.rms_interval = rms_interval
        self.file_names = file_names

    @cached_property
    def val_array(self):
        return self._ms_val_matrix[:, 1]

    @cached_property
    def ms_array(self):
        return self._ms_val_matrix[:, 0].astype(int)

    @cached_property
    def time_stamps(self):
        return pd.arrays.DatetimeArray((self.ms_array + 1000*60*60) * 1000000)

    @cached_property
    def val_std_array(self):
        return np.array([np.std(self.val_array[m]) for m in self._interval_masks])

    @cached_property
    def ms_std_array(self):
        return self.ms_array[[m[0] for m in self._interval_masks]]

    @cached_property
    def interval_time_stamps(self):
        return self.time_stamps[[int(np.median(m)) for m in self._interval_masks]]

    @cached_property
    def _ms_val_matrix(self):
        return np.concatenate([self._get_ms_value_matrix_from_file(f) for f in self.file_names])

    @cached_property
    def _n_intervals(self):
        return math.ceil((self.ms_array[-1] - self.ms_array[0]) / self.rms_interval)

    @cached_property
    def _ms_interval_edgess(self):
        return [self.ms_array[0] + i*self.rms_interval for i in range(self._n_intervals+1)]

    @cached_property
    def _interval_masks(self):
        masks = []
        for i in range(self._n_intervals):
            ms_0, ms_1 = [self._ms_interval_edgess[i], self._ms_interval_edgess[i+1]]
            masks.append(np.where((self.ms_array >= ms_0) * (self.ms_array < ms_1))[0])
        return masks

    def _get_ms_value_matrix_from_file(self, file_name):
        return pd.read_csv(file_name, sep=' ', header=None, usecols=[0, self.value_column]).values