__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"


all_date_list = ['2018-09-14', '2018-09-15', '2018-09-16', '2018-09-17', '2018-09-18', '2018-09-19',
                 '2018-09-20', '2018-09-21', '2018-09-22', '2018-09-23', '2018-09-24', '2018-09-25',
                 '2018-09-26', '2018-09-27', '2018-09-28', '2018-09-29', '2018-09-30', '2018-10-01',
                 '2018-10-02', '2018-10-03', '2018-10-04', '2018-10-05', '2018-10-06', '2018-10-07',
                 '2018-10-08', '2018-10-09', '2018-10-10', '2018-10-11', '2018-10-12', '2018-10-13',
                 '2018-10-14', '2018-10-15', '2018-10-16', '2018-10-17', '2018-10-18', '2018-10-19',
                 '2018-10-20', '2018-10-21', '2018-10-22', '2018-10-23', '2018-10-24', '2018-10-25',
                 '2018-10-26', '2018-10-27', '2018-10-28', '2018-10-29', '2018-10-30', '2018-10-31',
                 '2018-11-01', '2018-11-02', '2018-11-03', '2018-11-04', '2018-11-05', '2018-11-06',
                 '2018-11-07', '2018-11-08', '2018-11-09', '2018-11-10', '2018-11-11', '2018-11-12']


class InputFileNames:
    beam_mom = ['data/input/beamMom.csv']
    trig = ['data/input/TIMBER_DATA_alltriggers-DAQaddedNov1.csv']
    daq = ['data/input/DAQ-runlist.csv']
    life_time = ['data/input/prm_Top_lifetime_data.csv']
    detector_status = ['data/input/detector_status.csv']

    def __init__(self, date_list=None):
        if date_list is None:
            self.date_list = all_date_list
        else:
            self.date_list = date_list
        self.beam_mom = ['data/input/beamMom.csv']
        self.trig = ['data/input/TIMBER_DATA_alltriggers-DAQaddedNov1.csv']
        self.daq = ['data/input/DAQ-runlist.csv']
        self.life_time = ['data/input/prm_Top_lifetime_data.csv']
        self.detector_status = ['data/input/detector_status.csv']
        self.streamer = ['data/input/np04_hv_cut_periods.csv']
        self.curr = ['data/input/heinzCurr_' + d + '.csv' for d in self.date_list]
        self.volt = ['data/input/heinzVolt_' + d + '.csv' for d in self.date_list]