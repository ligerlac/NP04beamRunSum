__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import pandas as pd
import src.analyzers.base.combined as combined
from src.utils import downtimecalculator, streamersearcher
from functools import cached_property
import csv


class CombinedHeinzAnalyzer(combined.ResampledAnalyzer):
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
        b_df = df.iloc[df.index <= start_ts]
        d_df = df.iloc[(df.index > start_ts) * (df.index < end_ts)]
        a_df = df.iloc[(df.index >= end_ts)]
        df.loc[df.index <= start_ts, 'stable'] = (b_df['resistance'] > 1452) * (b_df['resistance'] < 1472) * (b_df['avgvolt'] > 120000)
        df.loc[(df.index > start_ts) * (df.index < end_ts), 'stable'] = (d_df['resistance'] > 1465) * (d_df['avgvolt'] > 120000)
        df.loc[df.index >= end_ts, 'stable'] = (a_df['resistance'] > 1465) * (a_df['avgvolt'] > 180000)
        return df

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


class SimpleDurationAnalyzer(combined.DurationAnalyzer):
    def _get_data_frame(self, df, title='title'):
        df[title] = pd.cut(df['duration_s'], self.binning)
        df_plot = df[title].value_counts(sort=False)
        return df_plot / df_plot.sum()


class CumDurationAnalyzer(combined.DurationAnalyzer):
    def _get_data_frame(self, df, title='title'):
        df['temp'] = pd.cut(df['duration_s'], self.binning)
        df_plot = df[title].value_counts(sort=False)
        for row in df.itertuples(index=True, name='Pandas'):
            df_plot.loc[row.temp] += row.duration_s
        df.rename({'temp': title})
        return df_plot / df_plot.sum()
