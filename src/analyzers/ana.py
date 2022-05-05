import pandas as pd
import numpy as np
from analyzers import base_classes
from utils import streamersearcher
from utils import downtimecalculator
from functools import cached_property
import csv


class HeinzAnalyzer(base_classes.IntervalAnalyzer):
    def __init__(self, interval=pd.Timedelta(30, "m"), file_names=None, val_name=None):
        super().__init__(interval=interval, file_names=file_names)
        self.val_name = val_name

    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=' ', index_col=0, usecols=[0, 1],
                           names=['timestamp', self.val_name])

    def _get_modified_data_frame(self, df):
        df.index = 1000000 * df.index
        return df


class TriggerAnalyzer(base_classes.GeneralAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=',', index_col=0, usecols=[0, 2],
                           names=['timestamp', 'trig_count'], header=0)

    def _get_modified_data_frame(self, df):
        df['trig_count_sum'] = np.cumsum(df['trig_count'])
        return df


class DAQAnalyzer(base_classes.GeneralAnalyzer):
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


class LifeTimeAnalyzer(base_classes.GeneralAnalyzer):
    @staticmethod
    def _get_data_frame_from_file(fn):
        return pd.read_csv(fn, sep=',', index_col=0, usecols=[0, 1],
                           names=['timestamp', 'lifetime'], header=0)

    def _get_modified_data_frame(self, df):
        df['contamination'] = 0.3 / df['lifetime']
        return df


class BeamAnalyzer(base_classes.GeneralAnalyzer):
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


class EFieldAnalyzer(base_classes.GeneralAnalyzer):
    def _get_data_frame_from_file(self, fn):
        return pd.read_csv(fn, sep=' ', index_col=0, usecols=[0, 1],
                           names=['timestamp', 'efield'], header=0)


class CombinedHeinzAnalyzer(base_classes.CombinedAnalyzer):
    def _get_modified_data_frame(self, df):
        df = self._decorate_averages(df)
        df = self._decorate_stable(df)
        return df

    def _decorate_averages(self, df):
        df['avgcurr'] = df['sumcurr'] / df['ncurr']
        df['avgvolt'] = df['sumvolt'] / df['nvolt']
        df['resistance'] = df['avgvolt'] / df['avgcurr']
        df['efield'] = (df['avgvolt'] - 97 * df['avgcurr']) / 360
        return df

    def _decorate_stable(self, df):
        start_ts, end_ts = [pd.to_datetime("2018-10-05 00:00:00"), pd.to_datetime("2018-10-17 12:00:00")]
        b_df = df.loc[df.index <= start_ts]
        d_df = df.loc[(df.index > start_ts) * (df.index < end_ts)]
        a_df = df.loc[(df.index >= end_ts)]
        b_df['stable'] = (b_df['resistance'] > 1452) * (b_df['resistance'] < 1472) * (b_df['avgvolt'] > 120000)
        d_df['stable'] = (d_df['resistance'] > 1465) * (d_df['avgvolt'] > 120000)
        a_df['stable'] = (a_df['resistance'] > 1465) * (a_df['avgvolt'] > 180000)
        return pd.concat([b_df, d_df, a_df], axis=0)

    @cached_property
    def streamer_intervals(self):
        return streamersearcher.get_streamer_intervals(self.data_frame)

    @cached_property
    def avg_up_time_data_frame(self):
        dt_calc = downtimecalculator.DownTimeCalculator(down_intervals=self.streamer_intervals,
                                     time_axis=self.data_frame.index)
        return dt_calc.data_frame

    def write_streamer_periods(self, file_name):
        with open(file_name, mode='w') as f:
            writer = csv.writer(f, delimiter=',')
            for interval in self.streamer_intervals:
                writer.writerow(interval)




