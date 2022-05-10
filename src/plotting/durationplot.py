__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
from functools import cached_property


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
        self.fig = plt.figure(figsize=(12, 4))
        self.grid = gridspec.GridSpec(nrows=1, ncols=3, figure=self.fig, height_ratios=[0.3])
        self.fig.subplots_adjust(left=0.06, bottom=0.1, right=0.94, top=0.93, wspace=None, hspace=0.)

    @cached_property
    def duration_plot(self):
        a = self.fig.add_subplot(self.grid[0, 0])
        a.set_ylabel('Streamer duration [s]')
        a.set_xlabel('Index (sorted)')
        a.tick_params(axis='y')
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.xaxis.set_tick_params(rotation=90)
        a.tick_params(axis='x', rotation=90)
        return a

    @cached_property
    def left_hist_plot(self):
        a = self.fig.add_subplot(self.grid[0, 1])
        a.set_ylabel('Number of entries')
        a.set_xlabel('Streamer duration [s]')
        a.tick_params(axis='y')
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.xaxis.set_tick_params(rotation=90)
        a.tick_params(axis='x', rotation=90)
        return a

    @cached_property
    def right_hist_plot(self):
        a = self.fig.add_subplot(self.grid[0, 2])
        a.set_ylabel('Number of entries')
        a.set_xlabel('Streamer duration [s]')
        a.tick_params(axis='y')
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.xaxis.set_tick_params(rotation=90)
        a.tick_params(axis='x', rotation=90)
        return a


    def plot(self):
        self.analyzer.plot_log_on(self.duration_plot)
        self.analyzer.plot_hist_on(self.left_hist_plot, cut_off=15)
        self.analyzer.plot_hist_on(self.right_hist_plot, cut_off=120)
        plt.savefig(self.output_name, format='png', dpi=1200)
        plt.show()