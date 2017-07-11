from ._version import get_versions
import logging


__version__ = get_versions()['version']
del get_versions


# module level logger
fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=fmt)
MAINFORMATTER = logging.Formatter(fmt)
MAINLOGGER = logging.getLogger("auxiclean")


# put this at the end to prevent import loop
from .selector import Selector  # noqa
