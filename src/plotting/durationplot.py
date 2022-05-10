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
        self.analyzer = None
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
        df = self.analyzer.data_frame.sort_values(by='duration', ignore_index=True)
        self._plot_duration(df)
        df = self.analyzer.data_frame_on

    def _plot_duration(self, df):
        df = df['duration_s']
        df.plot(kind='line', ax=self.duration_plot, logy=True, title='logarithmic streamer durations')

    def plot_simple_hist(self, cut_off=float('inf')):
        df = self.analyzer.data_frame['duration_s']
        df = df.loc[df < cut_off]
        df.hist(bins=10, ax=self.simple_hist_plot)

    def plot_hist(self, binning=None):
        if binning is None:
            binning = [0, 5, 10, 100]
        df = self.analyzer.data_frame
        df["bins"] = pd.cut(df['duration_s'], binning)
        df["bins"].value_counts(sort=False).plot.bar(ax=self.custom_hist_plot)

    def plot_cum_duration(self, binning=None):
        if binning is None:
            binning = [0, 5, 10, 100, float('inf')]
        df = self.analyzer.data_frame
        df["bins"] = pd.cut(df['duration_s'], binning)
        df = df["bins"].value_counts(sort=False)
        for row in self.analyzer.data_frame.itertuples(index=True, name='Pandas'):
            df.loc[row.bins] += row.duration_s
        print(f'df =\n{df}')
        df.plot.bar(ax=self.cum_hist_plot)



    def plot(self):
        self.plot_duration()
        self.plot_simple_hist(cut_off=16)
        self.plot_hist(binning=[0, 10, 60, 3600, 24*3600, float('inf')])
        self.plot_cum_duration(binning=[0, 10, 60, 3600, 24*3600, float('inf')])
        self.apply_cosmetics()
        plt.savefig(self.output_name, format='png', dpi=1200)
        plt.show()