__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from functools import cached_property
import pandas as pd


class DurationPlot:
    def __init__(self):
        self.fig = None
        self.grid = None
        self.analyzer_group = None
        self.output_name = None
        self.create_skeloton()

    @classmethod
    def from_args(cls, args):
        heinz_plot = cls()
        heinz_plot.output_name = args.output
        return heinz_plot

    def create_skeloton(self):
        self.fig = plt.figure(figsize=(12, 10))
        self.grid = gridspec.GridSpec(nrows=4, ncols=2, figure=self.fig, height_ratios=[0.4, 0.1, 0.4, 0.1])
        self.fig.subplots_adjust(left=0.06, bottom=0.1, right=0.94, top=0.93, wspace=None, hspace=0.)

    @cached_property
    def duration_plot(self):
        a = self.fig.add_subplot(self.grid[0, 0])
        a.set_ylabel('Streamer duration [s]')
        a.set_xlabel('Index (sorted)')
        a.tick_params(axis='y')
        return a

    @cached_property
    def simple_hist_plot(self):
        a = self.fig.add_subplot(self.grid[0, 1])
        a.set_ylabel('Number of entries')
        a.set_xlabel('Streamer duration [s]')
        return a

    @cached_property
    def custom_hist_plot(self):
        a = self.fig.add_subplot(self.grid[2, 0])
        a.set_ylabel('Number of entries')
        a.set_xlabel('Streamer duration [s]')
        return a

    @cached_property
    def cum_hist_plot(self):
        a = self.fig.add_subplot(self.grid[2, 1])
        a.set_ylabel('Cumulative time')
        a.set_xlabel('Streamer duration [s]')
        return a

    @cached_property
    def text_plot(self):
        a = self.fig.add_subplot(self.grid[0, 1])
        return a

    def apply_cosmetics(self):
        self.simple_hist_plot.tick_params(axis='x', labelrotation=0)
        self.custom_hist_plot.tick_params(axis='x', labelrotation=45)
        self.cum_hist_plot.tick_params(axis='x', labelrotation=45)

    def plot_duration(self):
        self._plot_duration(self.analyzer_group.streamer.data_frame, color='blue')
        self._plot_duration(self.analyzer_group.streamer_active.data_frame, color='red')

    def _plot_duration(self, df, color='blue'):
        df = df.sort_values(by='duration', ignore_index=True)
        print(f'df.iloc[-1] =\n{df.iloc[-1]}')
        df = df['duration_s']
        df.plot(kind='line', ax=self.duration_plot, logy=True, title='logarithmic streamer durations', color=color)

    def plot_simple_hist(self, cut_off=float('inf')):
        self._plot_simple_hist(self.analyzer_group.streamer.data_frame, color='blue', cut_off=cut_off)
        self._plot_simple_hist(self.analyzer_group.streamer_active.data_frame, color='red', cut_off=cut_off)

    def _plot_simple_hist(self, df, color='blue', cut_off=float('inf')):
        df = df['duration_s']
        df = df.loc[df < cut_off]
        df.hist(bins=10, ax=self.simple_hist_plot, color=color)

    def plot_hist(self, binning=None):
        if binning is None:
            binning = [0, 5, 10, 100]
        self._plot_hist(self.analyzer_group.streamer.data_frame, binning, color='blue')
        self._plot_hist(self.analyzer_group.streamer_active.data_frame, binning, color='red')

    def _plot_hist(self, df, binning, color='blue'):
        df["bins"] = pd.cut(df['duration_s'], binning)
        df["bins"].value_counts(sort=False).plot.bar(ax=self.custom_hist_plot, color=color)

    def plot_cum_duration(self, binning=None):
        if binning is None:
            binning = [0, 5, 10, 100, float('inf')]
        self._plot_cum_duration(self.analyzer_group.streamer.data_frame, binning, color='blue')
        self._plot_cum_duration(self.analyzer_group.streamer_active.data_frame, binning, color='red')

    def _plot_cum_duration(self, df, binning, color='blue'):
        df["bins"] = pd.cut(df['duration_s'], binning)
        df_plot = df["bins"].value_counts(sort=False)
        for row in df.itertuples(index=True, name='Pandas'):
            df_plot.loc[row.bins] += row.duration_s
        df_plot.plot.bar(ax=self.cum_hist_plot, color=color)


    def plot(self):
        self.plot_duration()
        self.plot_simple_hist(cut_off=16)
        self.plot_hist(binning=[0, 10, 60, 3600, 24*3600, float('inf')])
        self.plot_cum_duration(binning=[0, 10, 60, 3600, 24*3600, float('inf')])
        self.apply_cosmetics()
        plt.savefig(self.output_name, format='png', dpi=1200)
        plt.show()