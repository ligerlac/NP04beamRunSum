__author__ = "Lino Gerlach"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import argparse
import logging
from src.plotting import durationplot
import src.analyzers.group as group


def main(args):
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)
    ana_group = group.StreamerGroup.from_args(args)
    duration_plot = durationplot.DurationPlot.from_args(args)
    duration_plot.analyzer_group = ana_group
    duration_plot.plot()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--datelist", nargs="+", default=None, help="dates to consider")
    parser.add_argument("--debug", default=False, action="store_true", help="activate debug level logging")
    parser.add_argument("--output", type=str, default="data/output/duration_plots.png", help="name of output file")
    args = parser.parse_args()
    main(args)