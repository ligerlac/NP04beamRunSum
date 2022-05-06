from analyzers import ana


class AnalyzerGroup:
    def __init__(self):
        self.beam_mom = None
        self.trig = None
        self.daq = None
        self.life_time = None
        self.curr = None
        self.volt = None
        self.comb = None

    @classmethod
    def from_args(cls, args):
        ana_group = cls()
        date_list = args.datelist
        ana_group.beam_mom = ana.BeamAnalyzer(file_names=['data/beamMom.csv'])
        ana_group.trig = ana.TriggerAnalyzer(file_names=['data/TIMBER_DATA_alltriggers-DAQaddedNov1.csv'])
        ana_group.daq = ana.DAQAnalyzer(file_names=['data/DAQ-runlist.csv'],
                                        excl_cats=['commissioning', 'calibration'])
        ana_group.life_time = ana.LifeTimeAnalyzer(file_names=['data/prm_Top_lifetime_data.csv'])
        ana_group.curr = ana.HeinzAnalyzer(file_names=['data/heinzCurr_' + d + '.csv' for d in date_list],
                                           val_name='curr')
        ana_group.volt = ana.HeinzAnalyzer(file_names=['data/heinzVolt_' + d + '.csv' for d in date_list],
                                           val_name='volt')
        ana_group.comb = ana.CombinedHeinzAnalyzer([ana_group.curr, ana_group.volt])
        return ana_group
