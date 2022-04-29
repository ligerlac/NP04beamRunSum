from functools import cached_property
import math

class IntervalHandler:
    def __init__(self, interval, first_ts, last_ts):
        self.interval = interval
        self.first_ts = first_ts
        self.last_ts = last_ts

    @cached_property
    def n(self):
        return math.ceil((self.last_ts - self.first_ts) / self.interval)

    @cached_property
    def edges(self):
        return [self.first_ts + i * self.interval for i in range(self.n + 1)]

    @cached_property
    def mean_time_stamps(self):
        return [self.edges[i] + self.interval / 2 for i in range(self.n)]