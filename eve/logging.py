import logging
from os import getenv

log_level = getenv('LOG_LEVEL', 'DEBUG')
logger = logging.getLogger('eve')

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(format))

logger.addHandler(stream_handler)
logger.setLevel('DEBUG')
