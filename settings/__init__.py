
"""Settings module for HDFS Monitor."""
from logging.config import dictConfig

from .default import *  # common for all targets, mostly logging configuration


dictConfig(LOGGING)
logger = logging.getLogger('HDFS Monitor')
if DEBUG:
    logger.setLevel(logging.DEBUG)
    logger.debug('DEBUG is ON.')

logger.info('Settings Loaded')