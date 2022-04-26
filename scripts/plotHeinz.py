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




def get_ms_and_curr_arrays(file_name):
    raw = pd.read_csv(file_name, sep=' ', header=None, usecols=[0, 1]).values
    mseconds_raw = raw[:, 0].astype(int)
    currents_raw = raw[:, 1]
    return mseconds_raw, currents_raw


def get_index_arrays_for_interval(ms_array, ms_interval):
    n_intervals = int((ms_array[-1] - ms_array[0]) / ms_interval) + 1
    index_arrays = []
    for i in range(n_intervals):
        ms_0, ms_1 = [i * ms_interval + ms[0], (i + 1) * ms_interval + ms[0]]
        index_arrays.append(np.where((ms >= ms_0) * (ms < ms_1))[0])
    return index_arrays


class Analyzer:
    def __init__(self, name='', unit='', value_column=1, rms_interval=30, file_names=None):
        self.name = name
        self.unit = unit
        self.value_column = value_column
        self.rms_interval = rms_interval
        self.file_names = file_names
        self.ms_array = np.array([], dtype=int)
        self.value_array = np.array([])
        self.time_stamps = []
        self.time_stamps = None

    @property
    def time_stamps(self):
        return self._time_stamps

    @time_stamps.setter
    def time_stamps(self):
        self._temperature = pd.arrays.DatetimeArray(self.ms_array * 1000000)

    def _get_msecs_and_values_from_file(self, file_name):
        raw = pd.read_csv(file_name, sep=' ', header=None, usecols=[0, self.value_column]).values
        return raw[:, 0].astype(int), raw[:, 1]

    def set_msecs_and_values(self):
        for file_name in self.file_names:
            ms_temp, val_temp = self._get_msecs_and_values_from_file(file_name)
            self.ms_array = np.concatenate((self.ms_array, ms_temp))
            self.value_array = np.concatenate((self.value_array, val_temp))

    def get_index_arrays(self):
        n_intervals = int((self.ms_array[-1] - self.ms_array[0]) / self.rms_interval) + 1
        index_arrays = []
        for i in range(n_intervals):
            ms_0, ms_1 = [i * self.rms_interval + ms[0], (i + 1) * self.rms_interval + ms[0]]
            index_arrays.append(np.where((ms >= ms_0) * (ms < ms_1))[0])
        return index_arrays

    @property
    def time_stamps(self):
        self.

file_list = [ROOTDIR + '/data/heinzCurr_' + d + '.csv' for d in datelist]
analyzer = Analyzer(name='Current', unit='uA', value_column=1, rms_interval=30, file_names=file_list)
analyzer.set_msecs_and_values()


for d in datelist:
    inFile = ROOTDIR + '/data/heinzCurr_' + d + '.csv'
    ms, curr = get_ms_and_curr_arrays(inFile)
    ts = pd.arrays.DatetimeArray(ms * 1000000)
    index_arrays = get_index_arrays_for_interval(ms, 1800. * 1000.)
    [rms, rms_ms] = np.empty(len(index_arrays)), np.empty(len(index_arrays))
    for i, index_array in enumerate(index_arrays):
        ms_view, curr_view = [ms[index_array], curr[index_array]]
        rms[i] = np.std(curr_view)
        rms_ms[i] = ms[index_array[0]]
    rms_ms = ms[[index_array[0] for index_array in index_arrays]]
    rms_ts = pd.arrays.DatetimeArray(rms_ms * 1000000)


for d in datelist:
    inFile = ROOTDIR + '/data/heinzVolt_' + d + '.csv'
    volt_ms, volt = get_ms_and_curr_arrays(inFile)
    volt_ts = pd.arrays.DatetimeArray(volt_ms * 1000000)
    index_arrays = get_index_arrays_for_interval(volt_ms, 1800. * 1000.)
    [vrms, vrms_ms] = np.empty(len(index_arrays)), np.empty(len(index_arrays))
    for i, index_array in enumerate(index_arrays):
        ms_view, volt_view = [volt_ms[index_array], volt[index_array]]
        vrms[i] = np.std(volt_view)
        rms_ms[i] = ms[index_array[0]]
    vrms_ms = volt_ms[[index_array[0] for index_array in index_arrays]]
    vrms_ts = pd.arrays.DatetimeArray(vrms_ms * 1000000)


a0.plot_date(ts,curr,color='red',markersize=0.15)
a1.plot_date(rms_ts,rms,color='darkviolet',markersize=0.5)
a2.plot_date(volt_ts,volt,color='blue',markersize=0.15)
a3.plot_date(vrms_ts,vrms,color='green',markersize=0.5)
a0.set_xlim(ts[0],ts[-1])

days = mdates.DayLocator()
a0.xaxis.set_major_locator(days)

a0.axvspan(ts[0],ts[-1],facecolor='salmon',alpha=0.2)
a2.axvspan(ts[0],ts[-1],facecolor='salmon',alpha=0.2)

for period in beamperiod:
    a0.axvspan(period[0],period[1], facecolor='green', alpha=0.2)
    a2.axvspan(period[0],period[1], facecolor='green', alpha=0.2)

print('run time [s] = ')
print(datetime.now() - startTime)
#plt.tight_layout(pad=0)
plt.savefig('if.png')
plt.show()
