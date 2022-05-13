import pandas as pd
import src.analyzers.group as group


def test_streamer_group():
    a_g = group.StreamerGroup.from_args()
    for analyzer in a_g.__dict__.values():
        assert isinstance(analyzer.data_frame, pd.DataFrame)
