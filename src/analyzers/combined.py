__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import pandas as pd
from analyzers import base
from utils import streamersearcher
from utils import downtimecalculator
from functools import cached_property
import csv


class CombinedHeinzAnalyzer(base.CombinedAnalyzer):
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

    def write_streamer_periods(self, file_name, do_timestamps=False):
        with open(file_name, mode='w') as f:
            writer = csv.writer(f, delimiter=',')
            for interval in self.streamer_intervals:
                if do_timestamps:
                    writer.writerow([interval[0].timestamp(), interval[1].timestamp()])
                else:
                    writer.writerow(interval)


class CombinedDurationAnalyzer(base.CombinedAnalyzer):
    """Handles instances of StreamerAnalyzer"""
    def __init__(self, analyzer_dict=None, binning=None):
        self.analyzer_dict = analyzer_dict
        self.binning = binning

    def _get_data_frames(self):
        data_frames = []
        for key, value in self.analyzer_dict.items():
            data_frames.append(self._get_data_frame(df=value.data_frame, title=key))
        return data_frames

    def _get_data_frame(self, df, title='title'):
        df[title] = pd.cut(df['duration_s'], self.binning)
        df_plot = df[title].value_counts(sort=False)
        return df_plot / df_plot.sum()


class CombinedCumDurationAnalyzer(CombinedDurationAnalyzer):
    def _get_data_frame(self, df, title='title'):
        df['temp'] = pd.cut(df['duration_s'], self.binning)
        df_plot = df[title].value_counts(sort=False)
        for row in df.itertuples(index=True, name='Pandas'):
            df_plot.loc[row.temp] += row.duration_s
        df.rename({'temp': title})
        return df_plot / df_plot.sum()
