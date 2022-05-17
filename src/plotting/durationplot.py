__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from functools import cached_property


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
        self.fig = plt.figure(figsize=(11, 5))
        self.grid = gridspec.GridSpec(nrows=2, ncols=2, figure=self.fig, height_ratios=[0.4, 0.1])
        self.fig.subplots_adjust(left=0.06, bottom=0.1, right=0.94, top=0.93, wspace=None, hspace=0.)

    @cached_property
    def duration_plot(self):
        a = self.fig.add_subplot(self.grid[0, 0])
        a.set_ylabel('Number of entries [a.u.]')
        a.set_xlabel('Streamer duration [s] (excl. bins)')
        return a

    @cached_property
    def cum_duration_plot(self):
        a = self.fig.add_subplot(self.grid[0, 1])
        a.set_ylabel('Cumulative time [a.u.]')
        a.set_xlabel('Streamer duration [s] (excl. bins)')
        return a

    @cached_property
    def text_plot(self):
        a = self.fig.add_subplot(self.grid[0, 1])
        return a

    def apply_cosmetics(self):
        self.duration_plot.tick_params(axis='x', labelrotation=45)
        self.cum_duration_plot.tick_params(axis='x', labelrotation=45)
        self.duration_plot.set_xticklabels(('<10sec', '<1min', '<1h', '<1d', '>1d') )
        self.cum_duration_plot.set_xticklabels(('<10sec', '<1min', '<1h', '<1d', '>1d') )

    def plot_duration(self, binning=None):
        if binning is None:
            binning = [0, 5, 10, 100, float('inf')]
        self.analyzer_group.duration.binning = binning
        df_plot = self.analyzer_group.duration.data_frame
        df_plot.plot.bar(ax=self.duration_plot, rot=0, logy=True)

    def plot_cum_duration(self, binning=None):
        if binning is None:
            binning = [0, 5, 10, 100, float('inf')]
        self.analyzer_group.cum_duration.binning = binning
        df_plot = self.analyzer_group.cum_duration.data_frame
        df_plot.plot.bar(ax=self.cum_duration_plot, rot=0, logy=True)

    def plot(self):
        self.plot_duration(binning=[0, 10, 60, 3600, 24*3600, float('inf')])
        self.plot_cum_duration(binning=[0, 10, 60, 3600, 24*3600, float('inf')])
        self.apply_cosmetics()
        plt.savefig(self.output_name, format='png', dpi=1200)
        plt.show()