import logging
import time
import re
import hashlib
import formencode as fe

from includes.utils import *
from const.message import *
from config import *
from errors import *
from foodforfun.models.xception import Xception

LOGGER = logging.getLogger(__name__)


class RouteHandler:

    def __init__(self):
        self.xception_model = Xception()

    async def identify(self, request):
        data = await request.post()
        print("data", data)
        image = data['image']
        if image is null:
            
            identified_class = self.xception_model.predict(data['image'])
            return success({"status": 200, "identified": identified_class})