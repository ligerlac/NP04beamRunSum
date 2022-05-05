__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from datetime import datetime
from matplotlib import transforms
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from datetime import timedelta
import pandas as pd
import os
import sys
from analyzers import ana
from utils import formatting

startTime = datetime.now()

# USER: Make a list of the days you want to include in the plot here.
#       There should be a corresponding files in $ROOTDIR/data.

# datelist = ['2018-10-19','2018-10-20']
# datelist = ['2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01']
# datelist = ['2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-11-03','2018-11-04','2018-11-05','2018-11-06','2018-11-07','2018-11-08','2018-11-09','2018-11-10','2018-11-11']
# datelist = ['2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24','2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14']
# datelist = ['2018-09-14','2018-09-15','2018-09-16','2018-09-17','2018-09-18','2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24','2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14','2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-11-03','2018-11-04','2018-11-05','2018-11-06','2018-11-07','2018-11-08','2018-11-09','2018-11-10','2018-11-11']

# datelist = ['2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24','2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14','2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-11-03','2018-11-04','2018-11-05','2018-11-06','2018-11-07','2018-11-08','2018-11-09','2018-11-10','2018-11-11','2018-11-12']
datelist = ['2018-09-19']
datelist = ['2018-10-16', '2018-10-17', '2018-10-18', '2018-10-19', '2018-10-20', '2018-10-21']

file_name = 'data/beamMom.csv'
analyzer_beam_mom = ana.BeamAnalyzer(file_names=[file_name])

file_name = 'data/TIMBER_DATA_alltriggers-DAQaddedNov1.csv'
analyzer_trig = ana.TriggerAnalyzer(file_names=[file_name])

file_name = 'data/DAQ-runlist.csv'
analyzer_daq = ana.DAQAnalyzer(file_names=[file_name], excl_cats=['commissioning', 'calibration'])

file_name = 'data/prm_Top_lifetime_data.csv'
analyzer_lifetime = ana.LifeTimeAnalyzer(file_names=[file_name])

file_names = ['data/heinzCurr_' + d + '.csv' for d in datelist]
analyzer_curr = ana.HeinzAnalyzer(file_names=file_names, val_name='curr')
file_names = ['data/heinzVolt_' + d + '.csv' for d in datelist]
analyzer_volt = ana.HeinzAnalyzer(file_names=file_names, val_name='volt')
comb_ana = ana.CombinedHeinzAnalyzer([analyzer_curr, analyzer_volt])
comb_ana.write_streamer_periods('output/test.csv')

#########################
### Plotting:
#########################

# make the figure and organize the different panels of the plot

fig = plt.figure(figsize=(15, 8))
grid = gridspec.GridSpec(ncols=1, nrows=5, figure=fig, height_ratios=[2, 1.5, 1.5, 0.2, 1.5])

fig.subplots_adjust(left=0.06, bottom=0.1, right=0.94, top=0.93, wspace=None, hspace=0.)

a2 = fig.add_subplot(grid[2, 0])  # a2:   electric field
a4 = fig.add_subplot(grid[4, 0], sharex=a2)  # a3:   HV uptime
a3 = fig.add_subplot(grid[3, 0], xticklabels=[], sharex=a2)  # a3:   HV stat
a1 = fig.add_subplot(grid[1, 0], xticklabels=[], sharex=a2)  # a1:   e- lifetime
a0 = fig.add_subplot(grid[0, 0], xticklabels=[], sharex=a2)  # a0:   beam momentum
a0_0 = a0.twinx()  # a0_0: trigger count

a0.set_ylabel('Beam Momentum\n[GeV/c]', color='black')
a0.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a0.grid(color='grey', linestyle='--', linewidth=0.5)
a0.tick_params(labelbottom=False)

a0_0.set_ylabel('Beam Trigger Count', color='blue')
a0_0.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a0_0.tick_params(axis='y', colors='blue', labelcolor='blue')
a0_0.tick_params(labelbottom=False)

# chose if you want the purity monitor data expressed in terms of
# contamination (plotContamination = True) or lifetime (plotContamination = False)

plotContamination = True
# plotContamination = False

if not plotContamination:
    a1.set_ylabel('e- lifetime\n[ms]', color='darkviolet')
    a1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    a1.tick_params(axis='y', colors='darkviolet', labelcolor='darkviolet')
    a1.grid(color='grey', linestyle='--', linewidth=0.5)
    a1.set_ylim(-0.5, 6.5)
    a1.spines['left'].set_color('darkviolet')
    a1.tick_params(labelbottom=False)

else:
    a1.set_ylabel('Contamination\n' + r'[ppb O$^{2}$ equiv.]', color='darkviolet')
    a1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    a1.tick_params(axis='y', which='both', colors='darkviolet', labelcolor='darkviolet')
    a1.grid(color='grey', linestyle='--', linewidth=0.5)
    # a1.xaxis_date()
    a1.tick_params(labelbottom=False)

    a1_1 = a1.twinx()
    a1_1.tick_params(labelbottom=False, labeltop=False)
    a1_1.set_ylabel('e- lifetime\n[ms]', color='darkviolet')
    a1_1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    a1_1.tick_params(axis='y', which='both', colors='darkviolet', labelcolor='darkviolet')
    a1_1.spines['left'].set_color('darkviolet')
    a1_1.spines['right'].set_color('darkviolet')
    # a1_1.xaxis_date()

# cosmetics...

a2.set_ylabel('Drift Field\n[V/cm]', color='red')
a2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a2.tick_params(axis='y', colors='red', labelcolor='red')
a2.grid(color='grey', linestyle='--', linewidth=0.5)
a2.spines['left'].set_color('red')
a2.set_ylim(-30., 630.)
a2.tick_params(labelbottom=False, left=False)

# a3.set_ylabel('HV Status', rotation='horizontal', labelpad=30, va='center')
# a3.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
# a3.yaxis.labelpad = 50
a3.tick_params(labelbottom=False, left=False, labelleft=False)
a3.grid(axis='x', color='grey', linestyle='--', linewidth=0.5)

a4.set_ylabel('HV 12-hour Uptime\n[%]', color='navy')
a4.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a4.tick_params(axis='y', colors='navy', labelcolor='navy')
a4.grid(color='grey', linestyle='--', linewidth=0.5)
a4.spines['left'].set_color('navy')
a4.tick_params(axis='x', rotation=90)

rect1 = patches.Rectangle((0.2, 1.05), 0.1, 0.1, clip_on=False, facecolor='green', edgecolor='green', alpha=0.2,
                          transform=a0.transAxes)
a0.add_patch(rect1)
a0.text(0.32, 1.07, 'Beam ON', transform=a0.transAxes)
rect2 = patches.Rectangle((0.6, 1.05), 0.1, 0.1, clip_on=False, facecolor='salmon', edgecolor='salmon', alpha=0.2,
                          transform=a0.transAxes)
a0.add_patch(rect2)
a0.text(0.72, 1.07, 'Beam OFF', transform=a0.transAxes)


comb_ana.plot_efield_on_axis(a2)
analyzer_beam_mom.plot_on_axis(a0)
BItrig = analyzer_trig.plot_on_axis(a0_0)
DAQtrig = analyzer_daq.plot_on_axis(a0_0)
comb_ana.plot_uptime_on_axis(a4)
if plotContamination:
    analyzer_lifetime.plot_contam_on_axis(a1_1)
else:
    analyzer_lifetime.plot_lifetime_on_axis(a1)


secBins = comb_ana.data_frame.index
# cosmetics done after plotting
a0_0.legend((BItrig[0], DAQtrig[0]), ('BI Trigger Count', 'DAQ Trigger Count'))
a0_0.ticklabel_format(axis='y', style='sci', scilimits=(0, 0))
a0_0.set_yticks([0, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000])
a2.set_xlim(secBins[0], secBins[-1])
a0.set_yticks([0, 1, 2, 3, 4, 5, 6, 7])
a4.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
# a4.xaxis.set_major_locator(plt.MaxNLocator(6))
a2.set_yticks([0, 100, 200, 300, 400, 500, 600])

# make a tick every day

days = mdates.DayLocator()
a0.xaxis.set_major_locator(days)
a1.xaxis.set_major_locator(days)
a2.xaxis.set_major_locator(days)
a3.xaxis.set_major_locator(days)
a4.xaxis.set_major_locator(days)

# paint beam-on and beam-off periods on background

a0.axvspan(secBins[0], secBins[-1], facecolor='salmon', alpha=0.2)
a1.axvspan(secBins[0], secBins[-1], facecolor='salmon', alpha=0.2)
a2.axvspan(secBins[0], secBins[-1], facecolor='salmon', alpha=0.2)
a4.axvspan(secBins[0], secBins[-1], facecolor='salmon', alpha=0.2)

for period in analyzer_beam_mom.active_periods:
    a0.axvspan(period[0], period[1], facecolor='green', alpha=0.2)
    a1.axvspan(period[0], period[1], facecolor='green', alpha=0.2)
    a2.axvspan(period[0], period[1], facecolor='green', alpha=0.2)
    a4.axvspan(period[0], period[1], facecolor='green', alpha=0.2)

#########################
### Streamer Periods:
#########################
a3.axvspan(secBins[0], secBins[-1], facecolor='green')
for cut in comb_ana.streamer_intervals:
    a3.axvspan(cut[0], cut[1], facecolor='red')

#########################
### Data Taking Periods:
#########################

# TODO: CHECK TIME ZONE IS HANDLED CORRECTLY!!!

# a3.axvspan(secBins[0],secBins[-1],facecolor='salmon')

# with open(ROOTDIR + '/data/DAQ-runlist.csv',newline='') as f:
#    reader = csv.reader(f,delimiter=',')
#    for row in reader:
#        startString = row[2]
#        startString = startString[:-4]
#        startDAQ = datetime.strptime(startString, '%a, %d %b %Y %H:%M:%S')
#        endString = row[3]
#        endString = endString[:-4]
#        endDAQ = datetime.strptime(endString, '%a, %d %b %Y %H:%M:%S')
#        runType = str(row[1])
#        if runType == "physics":
#            a3.axvspan(startDAQ,endDAQ,facecolor='green',alpha=0.5)
#        if runType == "cosmics":
#            a3.axvspan(startDAQ,endDAQ,facecolor='blue',alpha=0.5)
#        else:
#            a3.axvspan(startDAQ,endDAQ,facecolor='purple',alpha=0.5)

########################

print('run time [s]')
print(datetime.now() - startTime)
# plt.tight_layout(pad=0)
# plt.savefig(ROOTDIR + '/output/beamRunSummary_new.eps', format='eps', dpi=1200)
# plt.savefig(ROOTDIR + '/output/beamRunSummary_new.svg', format='svg', dpi=1200)
# plt.savefig(ROOTDIR + '/output/beamRunSummary_new.pdf', format='pdf', dpi=1200)
plt.savefig('output/beamRunSummary_new.png', format='png', dpi=1200)
# plt.savefig(ROOTDIR + '/output/beamRunSummary_new.ps', format='ps', dpi=1200)
# plt.show()

plt.show()
