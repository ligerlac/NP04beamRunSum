__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import argparse
import logging
from plotting import durationplot
from analyzers import ana


def main(args):
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)
    streamer_analyzer = ana.StreamerAnalyzer(file_names=[args.input])
    duration_hist = durationplot.DurationPlot.from_args(args)
    duration_hist.analyzer = streamer_analyzer
    duration_hist.plot()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data/np04_hv_cut_periods.csv")
    parser.add_argument("--debug", default=False, action="store_true", help="activate debug level logging")
    parser.add_argument("--output", type=str, default="output/duration_hist.png", help="name of output file")
    args = parser.parse_args()
    main(args)