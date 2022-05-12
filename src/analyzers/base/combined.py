__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import pandas as pd
from functools import cached_property
import abc


class CombinedAnalyzer:
    """Wrapper class for data frames that are horizontally joined"""
    def __init__(self, analyzer_list=None):
        self.analyzer_list = analyzer_list

    @abc.abstractmethod
    def _get_data_frames(self):
        return []

    @abc.abstractmethod
    def _get_modified_data_frame(self, df):
        return df

    @cached_property
    def data_frame(self):
        df = pd.concat(self._get_data_frames(), axis=1)
        df = self._get_modified_data_frame(df)
        return df


class ResampledAnalyzer(CombinedAnalyzer):
    def __init__(self, analyzer_list):
        super().__init__(analyzer_list)
        self.resample_rate = 'S'

    def _get_data_frames(self):
        dfs = []
        for ana in self.analyzer_list:
            dfs.append(self._resample_value(ana))
            dfs.append(self._resample_count(ana))
        return dfs

    def _resample_value(self, ana):
        res = ana.data_frame.resample(self.resample_rate)[ana.val_name].sum()
        return pd.Series.to_frame(res).rename(columns={ana.val_name: 'sum'+ana.val_name})

    def _resample_count(self, ana):
        res = ana.data_frame.resample(self.resample_rate)[ana.val_name].count()
        return pd.Series.to_frame(res).rename(columns={ana.val_name: 'n'+ana.val_name})


class DurationAnalyzer(CombinedAnalyzer):
    """Handles instances of StreamerAnalyzer"""
    def __init__(self, analyzer_dict=None, binning=None):
        self.analyzer_dict = analyzer_dict
        self.binning = binning

    def _get_data_frames(self):
        data_frames = []
        for key, value in self.analyzer_dict.items():
            data_frames.append(self._get_data_frame(df=value.data_frame, title=key))
        return data_frames
