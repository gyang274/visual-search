import logging
import sys

logger = logging.getLogger('YG-VS')

_logging_target = sys.stdout
_handler = logging.StreamHandler(_logging_target)
_handler.setFormatter(logging.Formatter('%(levelname)s|%(name)s|%(filename)s|LINE:%(lineno)s|%(funcName)s|%(message)s'))

logger.addHandler(_handler)

logger.setLevel(level='INFO')
