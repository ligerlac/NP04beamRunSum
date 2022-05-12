__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import pandas as pd
import numpy as np
from analyzers.base import single
from functools import cached_property


class StreamerAnalyzer(single.GeneralAnalyzer):
    def __init__(self, file_names=None):
        self.file_names = file_names

    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', usecols=[0, 1], names=['begin', 'end'], parse_dates=[0, 1])

    def _get_modified_data_frame(self, df):
        df['duration'] = df['end'] - df['begin']
        df = self._decorate_cols_in_sec(df, ['duration', 'begin', 'end'])
        return df

    def _project_on_status_analyzer(self, status_analyzer):
        binning = status_analyzer.get_active_cut_binning()
        self._project_on_binning(binning)

    def _project_on_binning(self, binning):
        df = self.data_frame
        df['bin_begin'] = pd.cut(df['begin_s'], binning)  # is NaN if not in active period
        df['bin_end'] = pd.cut(df['end_s'], binning)  # is NaN if not in active period
        self.data_frame = df.loc[~df['bin_begin'].isnull() * ~df['bin_end'].isnull()].reset_index()

    def get_projected_copy(self, status_analyzer):
        copy = self.get_copy()
        copy._project_on_status_analyzer(status_analyzer)
        return copy


class CurrAnalyzer(single.HeinzAnalyzer):
    def __init__(self, interval=pd.Timedelta(30, "m"), file_names=None):
        super().__init__(interval=interval, file_names=file_names)
        self.val_name = 'curr'

    def plot_on(self, plot):
        return plot.plot_date(self.data_frame.index, self.data_frame[self.val_name], color='red',
                              markersize=0.15, linestyle='solid')

    def plot_std_on(self, plot):
        return plot.plot_date(self.interval_handler.mean_time_stamps, self.val_std_array, color='darkviolet',
                              markersize=0.5)


class VoltAnalyzer(single.HeinzAnalyzer):
    def __init__(self, interval=pd.Timedelta(30, "m"), file_names=None):
        super().__init__(interval=interval, file_names=file_names)
        self.val_name = 'volt'

    def plot_on(self, plot):
        return plot.plot_date(self.data_frame.index, self.data_frame[self.val_name], color='blue',
                              markersize=0.15, linestyle='solid')

    def plot_std_on(self, plot):
        return plot.plot_date(self.interval_handler.mean_time_stamps, self.val_std_array, color='green',
                              markersize=0.5)


class DetectorStatusAnalyzer(single.GeneralAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', usecols=[0, 1], names=['begin', 'end'], header=None, parse_dates=[0,1])

    def _get_modified_data_frame(self, df):
        df = self._decorate_cols_in_sec(df, ['begin', 'end'])
        return df

    def get_active_cut_binning(self):
        bin_tuples = []
        for row in self.data_frame.itertuples(index=True, name='Pandas'):
            bin_tuples.append((row.begin_s, row.end_s))
        return pd.IntervalIndex.from_tuples(bin_tuples)


class TriggerAnalyzer(single.TimeStampedAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=0, usecols=[0, 2],
                           names=['timestamp', 'trig_count'], header=0)

    def _get_modified_data_frame(self, df):
        df['trig_count_sum'] = np.cumsum(df['trig_count'])
        return df


class DAQAnalyzer(single.TimeStampedAnalyzer):
    def __init__(self, file_names=None, excl_cats=None,
                 upper_ts=pd.to_datetime("2018-11-12 10:00:00", utc=True)):
        super().__init__(file_names=file_names)
        self.excl_cats = excl_cats
        self.upper_ts = upper_ts

    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=1, usecols=[1, 3, 4],
                           names=['cat', 'timestamp', 'trig_count'], parse_dates=True)

    def _get_modified_data_frame(self, df):
        df = df[~df['cat'].isin(self.excl_cats)]
        df = df.loc[df.index < self.upper_ts]
        df = df.iloc[::-1]
        df['trig_count_sum'] = np.cumsum(df['trig_count'])
        return df


class NewDAQAnalyzer(single.GeneralAnalyzer):
    def __init__(self, file_names=None, excl_cats=None,
                 upper_ts=pd.to_datetime("2018-11-12 10:00:00", utc=True)):
        super().__init__(file_names=file_names)
        self.excl_cats = excl_cats
        self.upper_ts = upper_ts

    def _get_data_frame_from_file(self, fn):
        #5844, physics, "Mon, 12 Nov 2018 06:04:10 GMT", "Mon, 12 Nov 2018 08:02:19 GMT", 11584
        return pd.read_csv(fn, sep=',', index_col=0, usecols=[0, 1, 2, 3, 4],
                           names=['runnumber', 'cat', 'begin', 'end', 'trig_count'], parse_dates=[2, 3])

    def _get_modified_data_frame(self, df):
        #df = df[~df['cat'].isin(self.excl_cats)]
        #df = df.loc[df.index < self.upper_ts]
        #df = df.iloc[::-1]
        #df['trig_count_sum'] = np.cumsum(df['trig_count'])
        return df


class LifeTimeAnalyzer(single.TimeStampedAnalyzer):
    @staticmethod
    def _get_data_frame_from_file(fn):
        return pd.read_csv(fn, sep=',', index_col=0, usecols=[0, 1],
                           names=['timestamp', 'lifetime'], header=0)

    def _get_modified_data_frame(self, df):
        df['contamination'] = 0.3 / df['lifetime']
        return df


class BeamAnalyzer(single.TimeStampedAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=0, usecols=[0, 1],
                           names=['timestamp', 'beam_mom'], header=0)

    @cached_property
    def active_periods(self):
        active_periods = []
        is_active = False
        for row in self.data_frame.itertuples(index=True, name='Pandas'):
            if is_active:
                if row.beam_mom == 0:
                    is_active = False
                    b = row.Index
                    active_periods.append([a, b])
            else:
                if row.beam_mom > 0:
                    is_active = True
                    a = row.Index
        return active_periods

    def _get_modified_data_frame(self, df):
        df['beam_on'] = df['beam_mom'] > 0
        return df


class EFieldAnalyzer(single.TimeStampedAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=' ', index_col=0, usecols=[0, 1],
                           names=['timestamp', 'efield'], header=0)

