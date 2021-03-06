__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import argparse
import logging
from src.plotting import heinzplot
from src.analyzers import group


def main(args):
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)
    analyzer_group = group.HeinzGroup.from_args(args)
    heinz_plot = heinzplot.HeinzPlot.from_args(args)
    heinz_plot.analyzer_group = analyzer_group
    heinz_plot.plot()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--datelist", nargs="+", default=None, help="dates to consider")
    parser.add_argument("--debug", default=False, action="store_true", help="activate debug level logging")
    parser.add_argument("--output", type=str, default="data/output/heinz_plot.png", help="name of output file")
    args = parser.parse_args()
    main(args)