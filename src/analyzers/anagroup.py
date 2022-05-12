__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

from analyzers import ana
import config
import pandas as pd
from functools import cached_property


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
        file_names = config.InputFileNames(args.datelist)
        ana_group.beam_mom = ana.BeamAnalyzer(file_names=file_names.beam_mom)
        ana_group.detector_status = ana.DetectorStatusAnalyzer(file_names=config.InputFileNames.detector_status)
        ana_group.trig = ana.TriggerAnalyzer(file_names=file_names.trig)
        ana_group.daq = ana.DAQAnalyzer(file_names=file_names.daq, excl_cats=['commissioning', 'calibration'])
        ana_group.life_time = ana.LifeTimeAnalyzer(file_names=file_names.life_time)
        ana_group.curr = ana.HeinzAnalyzer(file_names=file_names.curr, val_name='curr')
        ana_group.volt = ana.HeinzAnalyzer(file_names=file_names.volt, val_name='volt')
        ana_group.comb = ana.CombinedHeinzAnalyzer([ana_group.curr, ana_group.volt])
        return ana_group


class HeinzGroup:
    def __init__(self):
        self.curr = None
        self.volt = None
        self.beam_mom = None

    @classmethod
    def from_args(cls, args):
        ana_group = cls()
        file_names = config.InputFileNames(args.datelist)
        ana_group.beam_mom = ana.BeamAnalyzer(file_names=file_names.beam_mom)
        ana_group.curr = ana.HeinzAnalyzer(file_names=file_names.curr, val_name='curr')
        ana_group.volt = ana.HeinzAnalyzer(file_names=file_names.volt, val_name='volt')
        return ana_group


class StreamerGroup:
    def __init__(self):
        self.detector_status = None
        self.streamer = None
        self.daq = None

    @classmethod
    def from_args(cls, args):
        ana_group = cls()
        file_names = config.InputFileNames(args.datelist)
        ana_group.detector_status = ana.DetectorStatusAnalyzer(file_names=file_names.detector_status)
        ana_group.streamer = ana.StreamerAnalyzer(file_names=file_names.streamer)
        ana_group.streamer_active = ana_group.streamer.get_active_copy(ana_group.detector_status)
        ana_group.daq = ana.DAQAnalyzer(file_names=file_names.daq, excl_cats=['commissioning', 'calibration'])
        return ana_group


