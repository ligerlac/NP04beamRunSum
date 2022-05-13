__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from functools import cached_property


class HeinzPlot:
    def __init__(self):
        self.plot_contamination = True
        self.fig = None
        self.grid = None
        self.analyzer_group = None
        self.trig_plot_id = None
        self.daq_plot_id = None
        self.output_name = None
        self.create_skeloton()

    @classmethod
    def from_args(cls, args):
        heinz_plot = cls()
        heinz_plot.output_name = args.output
        return heinz_plot

    def create_skeloton(self):
        self.fig = plt.figure(figsize=(6, 8))
        self.grid = gridspec.GridSpec(ncols=1, nrows=2, figure=self.fig, height_ratios=[1, 1])
        self.fig.subplots_adjust(left=0.06, bottom=0.1, right=0.94, top=0.93, wspace=None, hspace=0.)

    @cached_property
    def curr_plot(self):
        a = self.fig.add_subplot(self.grid[1, 0])
        a.set_ylim(-50., 210.)
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.set_ylabel('Heinzinger Current [uA]', color='red')
        a.tick_params(axis='y', colors='red', labelcolor='red')
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.xaxis.set_tick_params(rotation=90)
        a.tick_params(axis='x', rotation=90)
        return a

    @cached_property
    def volt_plot(self):
        a = self.fig.add_subplot(self.grid[0, 0], xticklabels=[], sharex=self.curr_plot)
        a.set_ylabel('Heinzinger Voltage [kV]', color='blue')
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.tick_params(axis='y', colors='blue', labelcolor='blue')
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.tick_params(labelbottom=False)
        rect1 = patches.Rectangle((0.2, 1.075), 0.1, 0.1, clip_on=False, facecolor='green',
                                  edgecolor='green', alpha=0.2, transform=a.transAxes)
        a.add_patch(rect1)
        a.text(0.32, 1.075, 'Beam ON', transform=a.transAxes)
        rect2 = patches.Rectangle((0.6, 1.075), 0.1, 0.1, clip_on=False, facecolor='salmon',
                                  edgecolor='salmon', alpha=0.2, transform=a.transAxes)
        a.add_patch(rect2)
        a.text(0.72, 1.075, 'Beam OFF', transform=a.transAxes)
        return a

    @cached_property
    def curr_std_plot(self):
        a = self.curr_plot.twinx()
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.set_ylabel('30-min. Current RMS [uA]', color='darkviolet')
        a.tick_params(axis="y", colors='green', labelcolor='darkviolet')
        a.spines['right'].set_color('darkviolet')
        a.spines['left'].set_color('red')
        return a

    @cached_property
    def volt_std_plot(self):
        a = self.volt_plot.twinx()
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.set_ylabel('30-min. Voltage RMS [kV]', color='green')
        a.tick_params(axis="y", colors='green', labelcolor='green')
        a.spines['right'].set_color('green')
        a.spines['left'].set_color('blue')
        a.tick_params(labelbottom=False)
        return a

    def color_plots(self):
        plot_list = [self.curr_plot, self.volt_plot]
        for plot in plot_list:
            plot.axvspan(self.analyzer_group.beam_mom.data_frame.index[0],
                         self.analyzer_group.beam_mom.data_frame.index[-1],
                         facecolor='salmon', alpha=0.2)
            for period in self.analyzer_group.beam_mom.active_periods:
                plot.axvspan(period[0], period[1], facecolor='green', alpha=0.2)


    def plot(self):
        self.analyzer_group.curr.plot_on(self.curr_plot)
        self.analyzer_group.volt.plot_on(self.volt_plot)
        self.analyzer_group.curr.plot_std_on(self.curr_std_plot)
        self.analyzer_group.volt.plot_std_on(self.volt_std_plot)
        c_ts = self.analyzer_group.curr.data_frame.index
        self.curr_plot.set_xlim(c_ts[0], c_ts[-1])
        days = mdates.DayLocator()
        self.curr_plot.xaxis.set_major_locator(days)
        self.color_plots()
        plt.savefig(self.output_name, format='png', dpi=1200)
        plt.show()

