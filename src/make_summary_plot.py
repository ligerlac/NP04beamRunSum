__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import argparse
import logging
from plotting import summaryplot
from analyzers import anagroup
from datetime import datetime


def main(args):
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)
    analyzer_group = anagroup.AnalyzerGroup.from_args(args)
    summary_plot = summaryplot.SummaryPlot.from_args(args)
    summary_plot.analyzer_group = analyzer_group
    summary_plot.plot()
    analyzer_group.comb.write_streamer_periods('data/np04_hv_cut_periods.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--plotcontamination", default=False, action="store_true",
                        help="activate to plot contamination instead of lifetime")
    parser.add_argument("--datelist", nargs="+", default=None, help="dates to consider")
    parser.add_argument("--debug", default=False, action="store_true", help="activate debug level logging")
    parser.add_argument("--output", type=str, default="output/beam_run_summary.png", help="name of output file")
    args = parser.parse_args()
    main(args)