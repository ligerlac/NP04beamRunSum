import pandas as pd
import src.analyzers.group as group
import inspect


class DummyArgs:
    datelist = None


def test_analyzer_groups_data_frames():
    for obj in group.__dict__.values():
        _test_obj_data_frames(obj)


def _test_obj_data_frames(obj):
    if inspect.isclass(obj):
        _test_class_data_frames(obj)


def _test_class_data_frames(cls):
    ins = cls.from_args(DummyArgs)
    _test_instance_data_frames(ins)


def _test_instance_data_frames(ins):
    for analyzer in ins.__dict__.values():
        assert isinstance(analyzer.data_frame, pd.DataFrame)
