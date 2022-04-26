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

curr     = []
ts       = []
rms      = []
rms_ts   = []
rms_tmp  = []
volt     = []
volt_ts  = []
vrms_tmp = []
vrms     = []
vrms_ts  = []

tup = datetime(2000,1,1,0,0,0)

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


def convert_to_time_stamp(ts):
    converted = datetime.utcfromtimestamp(ts) + timedelta(hours=1)
    return converted


convert_to_time_stamp_vec = np.vectorize(convert_to_time_stamp)


def get_ms_and_curr_arrays(file_name):
    raw = pd.read_csv(file_name, sep=' ', header=None, usecols=[0, 1]).values
    mseconds_raw = raw[:, 0].astype(int)
    currents_raw = raw[:, 1]
    return mseconds_raw, currents_raw


def get_index_arrays_for_interval(ms_array, ms_interval):
    n_intervals = int((ms_array[-1] - ms_array[0]) / ms_interval) + 1
    index_arrays = []
    for i in range(n_intervals):
        ms_0, ms_1 = [i * ms_interval + ms_new[0], (i + 1) * ms_interval + ms_new[0]]
        index_arrays.append(np.where((ms_new >= ms_0) * (ms_new < ms_1))[0])
    return index_arrays


t_0 = time.time()
for d in datelist:
    inFile = ROOTDIR + '/data/heinzCurr_' + d + '.csv'
    ms_new, curr_new = get_ms_and_curr_arrays(inFile)
    ts_new = pd.arrays.DatetimeArray(ms_new*1000000)
    index_arrays = get_index_arrays_for_interval(ms_new, 1800. * 1000.)
    [rms_new, rms_ms_new] = np.empty(len(index_arrays)), np.empty(len(index_arrays))
    for i, index_array in enumerate(index_arrays):
        ms_view, curr_view = [ms_new[index_array], curr_new[index_array]]
        rms_new[i] = np.std(curr_view)
        rms_ms_new[i] = ms_new[index_array[0]]
    rms_ts_new = convert_to_time_stamp_vec(rms_ms_new/1000)
print(f'my method took {time.time()-t_0} sec')

t_0 = time.time()
for d in datelist:
    inFile = ROOTDIR + '/data/heinzCurr_' + d + '.csv'
    with open(inFile,newline='') as f:
        reader = csv.reader(f,delimiter=' ')
        for row in reader:
            time_in_s = float(row[0])/1e3   #in seconds
            t = datetime.utcfromtimestamp(time_in_s) + timedelta(hours=1)
            #print(t)
            c = float(row[1])
            ts.append(t)
            curr.append(c)
            rms_tmp.append(c)
            #print((t-tup).total_seconds())
            if (t-tup).total_seconds() > 1800.:
            #if True:
                std = np.std(rms_tmp)
                rms.append(std)
                rms_ts.append(t)       # should be average not t_up, fix later
                tup = t
                #print(rms_tmp)
                #print('~~~~~~~~~~~~~~~~~~~~~~~~~~~')
                rms_tmp = []
print(f'Kevins method took {time.time()-t_0} sec')


#print(f'curr = {curr}')
#print(f'curr_new = {curr_new}')


print(f'p.ma.allequal(ts_new, ts) = {np.ma.allequal(ts_new, ts)}')
print(f'p.ma.allequal(curr_new, curr) = {np.ma.allequal(curr_new, curr)}')

print(f'p.ma.allequal(rms_new, rms) = {np.ma.allequal(rms_new, rms)}')
print(f'p.ma.allequal(rms_ts_new, rms_ts) = {np.ma.allequal(rms_ts_new, rms_ts)}')

#print(f'rms = {rms}')
#print(f'rms_new = {rms_new}')

sys.exit(0)

print(f'ts == ts_new_conv = {ts==ts_new_conv}')
print(f'curr == curr_new = {curr==curr_new}')
print(f'type(ts) = {type(ts)}')
print(f'len(ts) = {len(ts)}')
print(f'type(curr) = {type(curr)}')
print(f'len(curr) = {len(curr)}')

tup = datetime(2000,1,1,0,0,0)

for d in datelist:
    inFile = ROOTDIR + '/data/heinzVolt_' + d + '.csv'
    with open(inFile,newline='') as f:
        reader = csv.reader(f,delimiter=' ')
        for row in reader:
            time = float(row[0])/1e3   #in seconds
            t = datetime.utcfromtimestamp(time) + timedelta(hours=1)
            v = float(row[1])/1e3      # in kV
            volt_ts.append(t)
            volt.append(v)
            vrms_tmp.append(v)
            if (t-tup).total_seconds() > 1800.:
            #if True:
                std = np.std(vrms_tmp)
                vrms.append(std)
                vrms_ts.append(t)       # should be average not t_up, fix later
                tup = t
                vrms_tmp = []

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
