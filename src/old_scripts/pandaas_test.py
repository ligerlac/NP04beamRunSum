import pandas as pd
import numpy as np
import time
from analyzer import GeneralAnalyzer
import sys
import os

ROOTDIR = os.environ["NP04BRSROOT"]

fn = ROOTDIR + '/data/DAQ-runlist.csv'

fn1 = ROOTDIR + '/data/DAQ-runlist1.csv'
fn2 = ROOTDIR + '/data/DAQ-runlist2.csv'
file_names = [fn]

#column_dict = {'timestamps': 3, 'trig_count': 4, 'category': 1}
#test_analyzer = GeneralAnalyzer(column_dict=column_dict, index_col=3, std_interval=30*60*1000, file_names=[file_name])
#print(f'test_analyzer.get_data_frame = {test_analyzer.get_data_frame()}')

data_frame = pd.concat([pd.read_csv(fn, sep=',', index_col=1, usecols=[1, 3, 4], names=['cat', 'timestamp', 'trig_count'])
               for fn in file_names], axis=0)

print(f'data_frame =\n{data_frame}')

sys.exit(0)

data = [1,2,3]

time_stamps = ["2018-09-29 07:00:09.735000", "2018-09-29 07:00:10.735000", "2018-09-29 07:00:12.735000"]
date_time_index = pd.DatetimeIndex(time_stamps)
date_time_index = date_time_index.tz_localize("UTC")

series = pd.Series(data, date_time_index)

#print(series)

#print(date_time_index.tz_convert('CET'))


data = np.array([i for i in range(1000000)])

t_0 = time.time()
a = pd.arrays.DatetimeArray((data + 1000*60*60) * 1000000)
print(f'took {time.time()-t_0} sec for pandas array method')

t_0 = time.time()
b = pd.DatetimeIndex(data * 1000000).tz_localize("UTC").tz_convert("CET")
print(f'took {time.time()-t_0} sec for pandas localize method')

t_0 = time.time()
b = pd.DatetimeIndex(data * 1000000).shift(1, freq='H')
print(f'took {time.time()-t_0} sec for pandas shift method')


#print(f'a = {a}')
#print(f'b = {b}')