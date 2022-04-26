import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import csv
from datetime import datetime
from datetime import timedelta
from matplotlib import transforms
import numpy as np
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import os
import pandas as pd
import sys
import time
from functools import cached_property
import math
from itertools import cycle

# NB: should be run with python3

# beginning of rms calulcation not right, need to initiate properly

startTime = datetime.now()
ROOTDIR = os.environ["NP04BRSROOT"]


fig = plt.figure(figsize=(6, 8))
grid = gridspec.GridSpec(ncols=1,nrows=2,figure=fig,height_ratios=[1,1])
#fig, ax = plt.subplots(3, 1, sharex='col')

fig.subplots_adjust(left=0.06, bottom=0.1, right=0.94, top=0.93, wspace=None, hspace=0.)

a0 = fig.add_subplot(grid[1,0]) # a0: current (a1 -> RMS)
a2 = fig.add_subplot(grid[0,0],xticklabels=[],sharex=a0) # a2: voltage (a3 -> RMS)

a0.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a0.set_ylabel('Heinzinger Current [uA]',color='red')
a0.tick_params(axis='y',colors='red',labelcolor='red')
a0.grid(color='grey',linestyle='--',linewidth=0.5)
a0.xaxis.set_tick_params(rotation=90)
a0.tick_params(axis='x', rotation=90)
a0.set_ylim(-50.,210.)

a1 = a0.twinx()
a1.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a1.set_ylabel('30-min. Current RMS [uA]',color='darkviolet')
a1.tick_params(axis="y",colors='green',labelcolor='darkviolet')
a1.spines['right'].set_color('darkviolet')
a1.spines['left'].set_color('red')

a2.set_ylabel('Heinzinger Voltage [kV]',color='blue')
a2.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a2.tick_params(axis='y',colors='blue',labelcolor='blue')
a2.grid(color='grey',linestyle='--',linewidth=0.5)
#a4.set_ylim(-50.,210.)
a2.tick_params(labelbottom=False)

a3 = a2.twinx()
a3.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
a3.set_ylabel('30-min. Voltage RMS [kV]',color='green')
a3.tick_params(axis="y",colors='green',labelcolor='green')
a3.spines['right'].set_color('green')
a3.spines['left'].set_color('blue')
a3.tick_params(labelbottom=False)

rect1 = patches.Rectangle((0.2,1.075),0.1,0.1,clip_on=False,facecolor='green',edgecolor='green',alpha=0.2,transform=a2.transAxes)
a2.add_patch(rect1)
a2.text(0.32, 1.075,'Beam ON',transform=a2.transAxes)
rect2 = patches.Rectangle((0.6,1.075),0.1,0.1,clip_on=False,facecolor='salmon',edgecolor='salmon',alpha=0.2,transform=a2.transAxes)
a2.add_patch(rect2)
a2.text(0.72, 1.075,'Beam OFF',transform=a2.transAxes)


#datelist = ['2018-11-01','2018-11-02','2018-11-03','2018-11-04']
#datelist = ['2018-10-31','2018-11-01']
#datelist = ['2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01']
#datelist = ['2018-09-14','2018-09-15','2018-09-16','2018-09-17','2018-09-18','2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24','2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14','2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-11-03','2018-11-04','2018-11-05','2018-11-06','2018-11-07']

#datelist = ['2018-09-19','2018-09-20','2018-09-21','2018-09-22','2018-09-23','2018-09-24','2018-09-25','2018-09-26','2018-09-27','2018-09-28','2018-09-29','2018-09-30','2018-10-01','2018-10-02','2018-10-03','2018-10-04','2018-10-05','2018-10-06','2018-10-07','2018-10-08','2018-10-09','2018-10-10','2018-10-11','2018-10-12','2018-10-13','2018-10-14','2018-10-15','2018-10-16','2018-10-17','2018-10-18','2018-10-19','2018-10-20','2018-10-21','2018-10-22','2018-10-23','2018-10-24','2018-10-25','2018-10-26','2018-10-27','2018-10-28','2018-10-29','2018-10-30','2018-10-31','2018-11-01','2018-11-02','2018-11-03','2018-11-04','2018-11-05','2018-11-06','2018-11-07','2018-11-08','2018-11-09','2018-11-10','2018-11-11','2018-11-12']

datelist = ['2018-09-20']

beamperiod = [[datetime(2018,9,20,18,0,0),datetime(2018,9,26,8,0,0)],[datetime(2018,9,26,18,0,0),datetime(2018,10,3,8,0,0)],[datetime(2018,10,10,18,0,0),datetime(2018,10,17,8,0,0)],[datetime(2018,10,17,18,0,0),datetime(2018,10,18,8,0,0)],[datetime(2018,10,18,18,0,0),datetime(2018,10,24,8,0,0)],[datetime(2018,11,1,18,0,0),datetime(2018,11,7,8,0,0)],[datetime(2018,11,7,18,0,0),datetime(2018,11,12,6,0,0)]]


class Analyzer:
    def __init__(self, name='', unit='', value_column=1, rms_interval=30*60*1000, file_names=None):
        self.name = name
        self.unit = unit
        self.value_column = value_column
        self.rms_interval = rms_interval
        self.file_names = file_names

    @cached_property
    def val_array(self):
        return self._ms_val_matrix[:, 1]

    @cached_property
    def ms_array(self):
        return self._ms_val_matrix[:, 0].astype(int)

    @cached_property
    def time_stamps(self):
        return pd.arrays.DatetimeArray(self.ms_array * 1000000)

    @cached_property
    def val_std_array(self):
        return np.array([np.std(self.val_array[m]) for m in self._interval_masks])

    @cached_property
    def ms_std_array(self):
        return self.ms_array[[m[0] for m in self._interval_masks]]

    @cached_property
    def interval_time_stamps(self):
        return self.time_stamps[[m[0] for m in self._interval_masks]]

    @cached_property
    def _ms_val_matrix(self):
        return np.concatenate([self._get_ms_value_matrix_from_file(f) for f in self.file_names])

    @cached_property
    def _n_intervals(self):
        return math.ceil((self.ms_array[-1] - self.ms_array[0]) / self.rms_interval)

    @cached_property
    def _ms_interval_edgess(self):
        return [self.ms_array[0] + i*self.rms_interval for i in range(self._n_intervals+1)]

    @cached_property
    def _interval_masks(self):
        masks = []
        for i in range(self._n_intervals):
            ms_0, ms_1 = [self._ms_interval_edgess[i], self._ms_interval_edgess[i+1]]
            masks.append(np.where((self.ms_array >= ms_0) * (self.ms_array < ms_1))[0])
        return masks

    def _get_ms_value_matrix_from_file(self, file_name):
        print(f'self.__name__ = {self}')
        print(f'file_name = {file_name}')
        return pd.read_csv(file_name, sep=' ', header=None, usecols=[0, self.value_column]).values



file_list= [ROOTDIR + '/data/heinzCurr_' + d + '.csv' for d in datelist]
analyzer_curr = Analyzer(name='Current', unit='uA', value_column=1, rms_interval=30*60*1000, file_names=file_list)

file_list = [ROOTDIR + '/data/heinzVolt_' + d + '.csv' for d in datelist]
analyzer_volt = Analyzer(name='heinzVolt', unit='kV', value_column=1, rms_interval=30*60*1000, file_names=file_list)


a0.plot_date(analyzer_curr.time_stamps, analyzer_curr.val_array, color='red', markersize=0.15)
a1.plot_date(analyzer_curr.interval_time_stamps, analyzer_curr.val_std_array, color='darkviolet', markersize=0.5)
a2.plot_date(analyzer_volt.time_stamps, analyzer_volt.val_array, color='blue', markersize=0.15)
a3.plot_date(analyzer_volt.interval_time_stamps, analyzer_volt.val_std_array, color='green', markersize=0.5)
a0.set_xlim(analyzer_curr.time_stamps[0], analyzer_curr.time_stamps[-1])

days = mdates.DayLocator()
a0.xaxis.set_major_locator(days)

a0.axvspan(analyzer_curr.time_stamps[0], analyzer_curr.time_stamps[-1],facecolor='salmon',alpha=0.2)
a2.axvspan(analyzer_curr.time_stamps[0], analyzer_curr.time_stamps[-1],facecolor='salmon',alpha=0.2)

for period in beamperiod:
    a0.axvspan(period[0],period[1], facecolor='green', alpha=0.2)
    a2.axvspan(period[0],period[1], facecolor='green', alpha=0.2)

print('run time [s] = ')
print(datetime.now() - startTime)
#plt.tight_layout(pad=0)
plt.savefig('if.png')
plt.show()
