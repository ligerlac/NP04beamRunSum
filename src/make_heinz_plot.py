__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"

import argparse
import logging
from plotting import summaryplot
from analyzers import anagroup


def main(args):
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.WARNING)
    analyzer_group = anagroup.HeinzGroup.from_args(args)
    heinz_plot = summaryplot.HeinzPlot.from_args(args)
    heinz_plot.analyzer_group = analyzer_group
    heinz_plot.plot()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
#    parser.add_argument("--datelist", type=list, default=['2018-10-16', '2018-10-17', '2018-10-18',
#                                                          '2018-10-19', '2018-10-20', '2018-10-21'],
#                        help="dates to consider")
    parser.add_argument("--datelist", type=list, default=['2018-09-20'], help="dates to consider")
    parser.add_argument("--debug", default=False, action="store_true", help="activate debug level logging")
    parser.add_argument("--output", type=str, default="output/heinz_plot.png", help="name of output file")
    args = parser.parse_args()
    main(args)