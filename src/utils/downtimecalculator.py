__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

from functools import cached_property
import pandas as pd


class DownTimeCalculator:
    def __init__(self, down_intervals=None, time_axis=None, refresh_period=pd.Timedelta(1, "h"),
                 averaging_period=pd.Timedelta(12, "h")):
        self._down_intervals = [x for x in down_intervals]
        self._time_axis = time_axis
        self._refresh_period = refresh_period
        self._averaging_period = averaging_period

    @cached_property
    def _n_avg(self):
        return int(self._averaging_period / self._refresh_period)

    @cached_property
    def _n_bins(self):
        return int(round((self._time_axis[-1] - self._time_axis[0]) / self._refresh_period, 0))

    @cached_property
    def _time_stamps(self):
        return [self._time_axis[0] + i * self._refresh_period for i in range(self._n_bins)]

    @cached_property
    def _down_time_list(self):
        down_time_list = [pd.Timedelta(0, "h")] * self._n_bins
        for i, ts in enumerate(self._time_stamps):
            n_ts = ts + self._refresh_period
            for interval in self._down_intervals:
                a, b = interval
                if a >= n_ts:
                    break
                elif b <= ts:
                    continue
                elif ts <= a <= b <= n_ts:
                    down_time_list[i] += (b - a)
                    self._down_intervals.remove(interval)
                elif ts <= a <= n_ts <= b:
                    down_time_list[i] += (n_ts - a)
                elif n_ts >= b >= ts >= a:
                    down_time_list[i] += (b - ts)
                elif a <= ts <= n_ts <= b:
                    down_time_list[i] += (n_ts - ts)
                else:
                    print('This corner case should not exist')
        return down_time_list

    @cached_property
    def _avg_up_time_percentage_list(self):
        avg_up_time_list = [pd.Timedelta(0, "h")] * self._n_bins
        for i in range(self._n_bins):
            avg_down_time = pd.Timedelta(0, "h")
            k = self._n_avg-1 if i >= self._n_avg-1 else i
            for j in range(i-k, i+1):
                avg_down_time += self._down_time_list[j]
            avg_down_time = avg_down_time / (k+1)
            avg_up_time_list[i] = (self._refresh_period - avg_down_time) / self._refresh_period * 100.
        return avg_up_time_list

    @cached_property
    def data_frame(self):
        return pd.DataFrame({'avg_up_time': self._avg_up_time_percentage_list}, index=self._time_stamps)
