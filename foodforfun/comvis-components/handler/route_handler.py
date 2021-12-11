import logging
import time
import re
import hashlib
import formencode as fe

from includes.utils import *
from const.message import *
from config import *
from errors import *

LOGGER = logging.getLogger(__name__)


class RouteHandler:

    def __init__(self):
        return