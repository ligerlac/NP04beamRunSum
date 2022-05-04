import pandas as pd


class StreamerSearcher:
    streamer_intervals = []

    @classmethod
    def get_streamer_intervals(cls, df):
        df = df.loc[df['nvolt'] * df['ncurr'] != 0]
        streamer_on = False
        for row in df.itertuples(index=True, name='Pandas'):
            if streamer_on:
                if row.stable:
                    streamer_on = False
                    b = row.Index + pd.Timedelta(2, "s")
                    if len(cls.streamer_intervals) != 0 and cls.streamer_intervals[-1][1] > a:
                        cls.streamer_intervals[-1][1] = b
                    else:
                        cls.streamer_intervals.append([a, b])
            else:
                if not row.stable:
                    streamer_on = True
                    a = row.Index - pd.Timedelta(2, "s")
        return cls.streamer_intervals
