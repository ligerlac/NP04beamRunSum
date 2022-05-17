__author__ = "Lino Gerlach"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"


import pandas as pd
import src.analyzers.group as group
import src.utils.misc as misc


class DummyArgs:
    datelist = None


def test_duration_analyzer():
    streamer_group_0 = group.StreamerGroup.from_args(DummyArgs)
    streamer_group_0.duration.binning = [0, 0]
    _test_all_cols_are_nan(streamer_group_0.duration.data_frame)
    streamer_group_inf = group.StreamerGroup.from_args(DummyArgs)
    streamer_group_inf.duration.binning = [0, float('inf')]
    _test_all_cols_are_one(streamer_group_inf.duration.data_frame)


def test_analyzer_groups_data_frames():
    for cls in misc.get_all_classes(group):
        ins = cls.from_args(DummyArgs)
        _test_analyzer_group_data_frames(ins)


def _test_analyzer_group_data_frames(ins):
    for analyzer in ins.__dict__.values():
        assert isinstance(analyzer.data_frame, pd.DataFrame)


def _test_all_cols_are_nan(df):
    for col in df:
        assert df[col].isnull().values.any()


def _test_all_cols_are_one(df):
    for col in df:
        assert (df[col] == 1).values.any()
