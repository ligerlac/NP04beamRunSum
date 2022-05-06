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


class SummaryPlot:
    def __init__(self):
        self.plot_contamination = True
        self.fig = None
        self.grid = None
        self.analyzer_group = None
        self.create_skeloton()

    def plot(self):
        self.analyzer_group.comb.plot_efield_on_axis(self.e_field_axis)
        self.analyzer_group.beam_mom.plot_on_axis(self.beam_mom_axis)
        BItrig = self.analyzer_group.trig.plot_on_axis(self.trig_count_axis)
        DAQtrig = self.analyzer_group.daq.plot_on_axis(self.trig_count_axis)
        self.analyzer_group.comb.plot_uptime_on_axis(self.up_time_axis)
        if self.plot_contamination:
            self.analyzer_group.life_time.plot_contam_on_axis(self.contamination_axis)
        else:
            self.analyzer_group.life_time.plot_lifetime_on_axis(self.life_time_axis)
        secBins = self.analyzer_group.comb.data_frame.index

        # cosmetics done after plotting
        self.trig_count_axis.legend((BItrig[0], DAQtrig[0]), ('BI Trigger Count', 'DAQ Trigger Count'))
        self.trig_count_axis.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        self.trig_count_axis.set_yticks([0, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000])
        self.e_field_axis.set_xlim(secBins[0], secBins[-1])
        self.beam_mom_axis.set_yticks([0, 1, 2, 3, 4, 5, 6, 7])
        self.up_time_axis.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        self.e_field_axis.set_yticks([0, 100, 200, 300, 400, 500, 600])

        days = mdates.DayLocator()
        self.beam_mom_axis.xaxis.set_major_locator(days)
        self.life_time_axis.xaxis.set_major_locator(days)
        self.e_field_axis.xaxis.set_major_locator(days)
        self.hv_stat_axis.xaxis.set_major_locator(days)
        self.up_time_axis.xaxis.set_major_locator(days)

        self.analyzer_group.beam_mom.color_axes(
            [self.beam_mom_axis, self.life_time_axis, self.e_field_axis, self.up_time_axis])

        self.analyzer_group.comb.plot_streamers_on_axis(self.hv_stat_axis)
        plt.savefig('output/beamRunSummary_new.png', format='png', dpi=1200)
        plt.show()

    @classmethod
    def from_args(cls, args):
        summary_plot = cls()
        summary_plot.plot_contamination = args.plotcontamination
        return summary_plot

    @cached_property
    def beam_mom_axis(self):
        a = self.fig.add_subplot(self.grid[0, 0], sharex=self.e_field_axis)
        a.set_ylabel('Beam Momentum\n[GeV/c]', color='black')
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.tick_params(labelbottom=False)
        return a

    @cached_property
    def trig_count_axis(self):
        a = self.beam_mom_axis.twinx()
        a.set_ylabel('Beam Trigger Count', color='blue')
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.tick_params(axis='y', colors='blue', labelcolor='blue')
        a.tick_params(labelbottom=False)
        rect1 = patches.Rectangle((0.2, 1.05), 0.1, 0.1, clip_on=False, facecolor='green', edgecolor='green', alpha=0.2,
                          transform=a.transAxes)
        a.add_patch(rect1)
        a.text(0.32, 1.07, 'Beam ON', transform=a.transAxes)
        rect2 = patches.Rectangle((0.6, 1.05), 0.1, 0.1, clip_on=False, facecolor='salmon', edgecolor='salmon', alpha=0.2,
                          transform=a.transAxes)
        a.add_patch(rect2)
        a.text(0.72, 1.07, 'Beam OFF', transform=a.transAxes)
        return a

    @cached_property
    def contamination_axis(self):
        a = self.fig.add_subplot(self.grid[1, 0], sharex=self.e_field_axis)
        a.set_ylabel('Contamination\n' + r'[ppb O$^{2}$ equiv.]', color='darkviolet')
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.tick_params(axis='y', which='both', colors='darkviolet', labelcolor='darkviolet')
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.tick_params(labelbottom=False)
        a1_1 = a.twinx()
        a1_1.tick_params(labelbottom=False, labeltop=False)
        a1_1.set_ylabel('e- lifetime\n[ms]', color='darkviolet')
        a1_1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a1_1.tick_params(axis='y', which='both', colors='darkviolet', labelcolor='darkviolet')
        a1_1.spines['left'].set_color('darkviolet')
        a1_1.spines['right'].set_color('darkviolet')
        return a1_1

    @cached_property
    def life_time_axis(self):
        a = self.fig.add_subplot(self.grid[1, 0], sharex=self.e_field_axis)
        a.set_ylabel('e- lifetime\n[ms]', color='darkviolet')
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.tick_params(axis='y', colors='darkviolet', labelcolor='darkviolet')
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.set_ylim(-0.5, 6.5)
        a.spines['left'].set_color('darkviolet')
        a.tick_params(labelbottom=False)
        return a

    @cached_property
    def e_field_axis(self):
        a = self.fig.add_subplot(self.grid[2, 0])
        a.set_ylabel('Drift Field\n[V/cm]', color='red')
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.tick_params(axis='y', colors='red', labelcolor='red')
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.spines['left'].set_color('red')
        a.set_ylim(-30., 630.)
        a.tick_params(labelbottom=False, left=False)
        return a

    @cached_property
    def hv_stat_axis(self):
        a = self.fig.add_subplot(self.grid[3, 0], sharex=self.e_field_axis)
        a.tick_params(labelbottom=False, left=False, labelleft=False)
        a.grid(axis='x', color='grey', linestyle='--', linewidth=0.5)
        return a

    @cached_property
    def up_time_axis(self):
        a = self.fig.add_subplot(self.grid[4, 0], sharex=self.e_field_axis)
        a.set_ylabel('HV 12-hour Uptime\n[%]', color='navy')
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.tick_params(axis='y', colors='navy', labelcolor='navy')
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.spines['left'].set_color('navy')
        a.tick_params(axis='x', rotation=90)
        return a

    def create_skeloton(self):
        self.fig = plt.figure(figsize=(15, 8))
        self.grid = gridspec.GridSpec(ncols=1, nrows=5, figure=self.fig,
                                      height_ratios=[2, 1.5, 1.5, 0.2, 1.5])
        self.fig.subplots_adjust(left=0.06, bottom=0.1, right=0.94, top=0.93, wspace=None, hspace=0.)
