__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import src.analyzers.single as single
import src.analyzers.combined as combined
from src import config


class SummaryGroup:
    """Group for summary plot"""
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
        file_names = config.InputFileNames(args.datelist)
        ana_group.beam_mom = single.BeamAnalyzer(file_names=file_names.beam_mom)
        ana_group.detector_status = single.DetectorStatusAnalyzer(file_names=config.InputFileNames.detector_status)
        ana_group.trig = single.TriggerAnalyzer(file_names=file_names.trig)
        ana_group.daq = single.DAQAnalyzer(file_names=file_names.daq, excl_cats=['commissioning', 'calibration'])
        ana_group.life_time = single.LifeTimeAnalyzer(file_names=file_names.life_time)
        ana_group.curr = single.CurrAnalyzer(file_names=file_names.curr)
        ana_group.volt = single.VoltAnalyzer(file_names=file_names.volt)
        ana_group.comb = combined.CombinedHeinzAnalyzer([ana_group.curr, ana_group.volt])
        return ana_group


class HeinzGroup:
    """Group for Heinzinger plots"""
    def __init__(self):
        self.curr = None
        self.volt = None
        self.beam_mom = None

    @classmethod
    def from_args(cls, args):
        ana_group = cls()
        file_names = config.InputFileNames(args.datelist)
        ana_group.beam_mom = single.BeamAnalyzer(file_names=file_names.beam_mom)
        ana_group.curr = single.CurrAnalyzer(file_names=file_names.curr)
        ana_group.volt = single.VoltAnalyzer(file_names=file_names.volt)
        return ana_group


class StreamerGroup:
    """Group for streamer interval duration plots"""
    def __init__(self):
        self.detector_status = None
        self.streamer = None
        #self.daq = None

    @classmethod
    def from_args(cls, args=None):
        ana_group = cls()
        file_names = config.InputFileNames()
        ana_group.detector_status = single.DetectorStatusAnalyzer(file_names=file_names.detector_status)
        ana_group.streamer = single.StreamerAnalyzer(file_names=file_names.streamer)
        ana_group.streamer_active = ana_group.streamer.get_projected_copy(ana_group.detector_status)
        ana_group.duration = combined.SimpleDurationAnalyzer(
            analyzer_dict={'all': ana_group.streamer, 'active': ana_group.streamer_active})
        ana_group.cum_duration = combined.CumDurationAnalyzer(
            analyzer_dict={'all': ana_group.streamer, 'active': ana_group.streamer_active}
        )
        return ana_group


