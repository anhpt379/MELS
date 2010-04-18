__version_info__ = (0, 1)
__version__ = '.'.join([str(v) for v in __version_info__])

from columnfamily import *
from columnfamilymap import *
from types import *
from connection import *

from lib.cassandra.ttypes import ConsistencyLevel, InvalidRequestException, \
    NotFoundException, UnavailableException, TimedOutException
