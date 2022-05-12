__author__ = "Lino Gerlach"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import argparse
import logging
from plotting import durationplot
from analyzers import ana, anagroup
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
import sys
import config


def main(args):
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)
    ana_group = anagroup.StreamerGroup.from_args(args)
    duration_plot = durationplot.DurationPlot.from_args(args)
    duration_plot.analyzer_group = ana_group
    duration_plot.plot()
    sys.exit(0)

    print(f'ana_group.streamer.data_frame =\n{ana_group.streamer.data_frame}')
    print(f'ana_group.detector_status.data_frame =\n{ana_group.detector_status.data_frame}')
    binning = []
    for row in ana_group.detector_status.data_frame.itertuples(index=True, name='Pandas'):
        binning.append(row.begin)
        binning.append(row.end)
    print(f'bins = {binning}')
    df = ana_group.streamer.data_frame

    streamer_periods_on, streamer_periods_off = [[], []]
    detector_status_iterator = 0
    #for row in ana_group.streamer.data_frame.itertuples(index=True, name='Pandas'):
    #    if row.begin

    df["bin_begin"] = pd.cut(df['begin'], binning)  # is NaN if not in active period
    df["bin_end"] = pd.cut(df['end'], binning)  # is NaN if not in active period

    print(f'df =\n{df}')

    df_loc = df.loc[~df['bin_begin'].isnull()]
    df_loc = df_loc.loc[df_loc['bin_end'].isnull()]
    print(f'df_loc =\n{df_loc}')

    df_loc = df.loc[~df['bin_end'].isnull()]
    df_loc = df_loc.loc[df_loc['bin_begin'].isnull()]
    print(f'df_loc =\n{df_loc}')


    #df["bins"].value_counts(sort=False).plot.bar(ax=self.custom_hist_plot)


#    df = ana_group.curr.data_frame
#    for row in ana_group.detector_status.data_frame.itertuples(index=True, name='Pandas'):
#        print(f'row.begin = {row.begin}, row.end = {row.end}')
#        df_temp = df.loc[df.index > pd.to_datetime(row.begin)]
#        print(f'df_tempe = \n {df_temp}')

    sys.exit(0)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data/np04_hv_cut_periods.csv")
    parser.add_argument("--datelist", nargs="+", default=None, help="dates to consider")
    parser.add_argument("--debug", default=False, action="store_true", help="activate debug level logging")
    parser.add_argument("--output", type=str, default="output/duration_hist.png", help="name of output file")
    args = parser.parse_args()
    main(args)