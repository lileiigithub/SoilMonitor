# -*- coding: utf-8 -*-

import numpy as np
import collections
import cv2
# from log import logger
import logging
logger = logging.getLogger("app")
# logger.setLevel(logging.INFO)
console = logging.StreamHandler()
console.setLevel(logging.INFO)

def fun():
    logger.error("error")
    logger.info("info")
    logger.debug("debug")
fun()
