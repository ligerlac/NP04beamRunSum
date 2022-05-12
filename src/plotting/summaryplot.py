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
from datetime import datetime
from utils import formatting


class SummaryPlot:
    def __init__(self):
        self.plot_contamination = True
        self.fig = None
        self.grid = None
        self.analyzer_group = None
        self.trig_plot_id = None
        self.daq_plot_id = None
        self.output_name = None
        self.create_skeloton()

    def plot_e_field(self):
        self.e_field_plot.plot(self.analyzer_group.comb.data_frame.index,
                               self.analyzer_group.comb.data_frame['efield'],
                               color='red', markersize=0.15)

    def plot_beam_mom(self):
        self.beam_mom_plot.plot(self.analyzer_group.beam_mom.data_frame.index,
                                self.analyzer_group.beam_mom.data_frame['beam_mom'],
                                linewidth=3, markersize=3, color='black')

    def color_plots(self):
        plot_list = [self.beam_mom_plot, self.life_time_plot, self.e_field_plot, self.up_time_plot]
        for plot in plot_list:
            plot.axvspan(self.analyzer_group.beam_mom.data_frame.index[0],
                         self.analyzer_group.beam_mom.data_frame.index[-1],
                         facecolor='salmon', alpha=0.2)
            for period in self.analyzer_group.beam_mom.active_periods:
                plot.axvspan(period[0], period[1], facecolor='green', alpha=0.2)

    def plot_trig(self):
        self.trig_plot_id = self.trig_count_plot.plot(self.analyzer_group.trig.data_frame.index,
                                                 self.analyzer_group.trig.data_frame['trig_count_sum'],
                                                 color='blue', markersize=0, linestyle='solid')[0]

    def plot_daq(self):
        self.daq_plot_id = self.trig_count_plot.plot(self.analyzer_group.daq.data_frame.index,
                                                     self.analyzer_group.daq.data_frame['trig_count_sum'],
                                                     color='blue', markersize=0, linestyle='dashed')

    def plot_up_time(self):
        self.up_time_plot.plot(self.analyzer_group.comb.avg_up_time_data_frame.index,
                               self.analyzer_group.comb.avg_up_time_data_frame['avg_up_time'],
                               color='navy', markersize=0.3, linestyle='solid')


    def plot_lifetime(self):
        self.life_time_plot.plot(self.analyzer_group.data_frame.index,
                            self.analyzer_group.data_frame['lifetime'],
                            linestyle='None', color='darkviolet', marker='o', markersize=3)
        self.life_time_plot.set_yticks([0, 1, 2, 3, 4, 5, 6])


    def plot_contam(self):
        self.life_time_plot.plot(self.analyzer_group.life_time.data_frame.index,
                                 self.analyzer_group.life_time.data_frame['contamination'],
                                 linestyle='None', color='darkviolet', marker='o', markersize=3)
        self.life_time_plot.set_yscale("log")
        a1_bot, a1_top = self.life_time_plot.get_ylim()
        self.life_time_plot.set_ylim(bottom=a1_bot, top=a1_top)
        from matplotlib.ticker import FuncFormatter
        self.life_time_plot.yaxis.set_major_formatter(FuncFormatter(formatting.format_fn))
        self.life_time_plot.yaxis.set_minor_formatter(FuncFormatter(formatting.minorFormat_fn))

    def plot_streamers(self):
        self.hv_stat_plot.axvspan(self.analyzer_group.comb.data_frame.index[0],
                                  self.analyzer_group.comb.data_frame.index[-1], facecolor='green')
        for cut in self.analyzer_group.comb.streamer_intervals:
            self.hv_stat_plot.axvspan(cut[0], cut[1], facecolor='red')

    def fill_sub_plots(self):
        self.plot_e_field()
        self.plot_beam_mom()
        self.plot_trig()
        self.plot_daq()
        self.plot_up_time()
        if self.plot_contamination:
            self.plot_contam()
        else:
            self.plot_lifetime()

    def apply_cosmetics(self):
        self.trig_count_plot.legend((self.trig_plot_id, self.daq_plot_id), ('BI Trigger Count', 'DAQ Trigger Count'))
        self.trig_count_plot.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
        self.trig_count_plot.set_yticks([0, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000])
        sec_bins = self.analyzer_group.comb.data_frame.index
        self.e_field_plot.set_xlim(sec_bins[0], sec_bins[-1])
        self.beam_mom_plot.set_yticks([0, 1, 2, 3, 4, 5, 6, 7])
        self.up_time_plot.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        self.e_field_plot.set_yticks([0, 100, 200, 300, 400, 500, 600])

    def set_locators(self):
        days = mdates.DayLocator()
        self.beam_mom_plot.xaxis.set_major_locator(days)
        #self.life_time_plot.xaxis.set_major_locator(days)
        self.e_field_plot.xaxis.set_major_locator(days)
        self.hv_stat_plot.xaxis.set_major_locator(days)
        self.up_time_plot.xaxis.set_major_locator(days)

    def plot(self):
        startTime = datetime.now()
        self.fill_sub_plots()
        self.apply_cosmetics()
        self.set_locators()
        self.color_plots()
        self.plot_streamers()
        print('run time [s]')
        print(datetime.now() - startTime)
        plt.savefig(self.output_name, format='png', dpi=1200)
#        plt.show()

    @classmethod
    def from_args(cls, args):
        summary_plot = cls()
        summary_plot.plot_contamination = args.plotcontamination
        summary_plot.output_name = args.output
        return summary_plot

    @cached_property
    def beam_mom_plot(self):
        a = self.fig.add_subplot(self.grid[0, 0], sharex=self.e_field_plot)
        a.set_ylabel('Beam Momentum\n[GeV/c]', color='black')
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.tick_params(labelbottom=False)
        return a

    @cached_property
    def trig_count_plot(self):
        a = self.beam_mom_plot.twinx()
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

    def _get_contamination_plot(self):
        a = self.fig.add_subplot(self.grid[1, 0], sharex=self.e_field_plot)
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

    def _get_life_time_plot(self):
        a = self.fig.add_subplot(self.grid[1, 0], sharex=self.e_field_plot)
        a.set_ylabel('e- lifetime\n[ms]', color='darkviolet')
        a.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        a.tick_params(axis='y', colors='darkviolet', labelcolor='darkviolet')
        a.grid(color='grey', linestyle='--', linewidth=0.5)
        a.set_ylim(-0.5, 6.5)
        a.spines['left'].set_color('darkviolet')
        a.tick_params(labelbottom=False)
        return a

    @cached_property
    def life_time_plot(self):
        if self.plot_contamination:
            return self._get_contamination_plot()
        else:
            return self._get_life_time_plot()

    @cached_property
    def e_field_plot(self):
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
    def hv_stat_plot(self):
        a = self.fig.add_subplot(self.grid[3, 0], sharex=self.e_field_plot)
        a.tick_params(labelbottom=False, left=False, labelleft=False)
        a.grid(axis='x', color='grey', linestyle='--', linewidth=0.5)
        return a

    @cached_property
    def up_time_plot(self):
        a = self.fig.add_subplot(self.grid[4, 0], sharex=self.e_field_plot)
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
