__author__ = "Lino Gerlach, Kevin Wood"
__credits__ = [""]
__version__ = "0.0.1"
__maintainer__ = "Lino Gerlach"
__email__ = "lino.oscar.gerlach@cern.ch"


def format_fn(tick_val, tick_pos):
    # tick_val = contamination
    et = (1. / tick_val) * (0.1 * 3.)
    return "{0:0.1f}".format(et)


def minorFormat_fn(tick_val, tick_pos):
    # tick_val = contamination
    et = (1. / tick_val) * (0.1 * 3.)
    if tick_val in [0.05, 0.1, 0.5, 1., 5, ] and et > 0.1:
        return "{0:0.1f}".format(et)
    elif tick_val in [0.05, 0.1, 0.5, 1., 5, ] and et < 0.1:
        return "{0:0.2f}".format(et)
    else:
        return ''
