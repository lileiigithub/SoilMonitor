# -*- coding: utf-8 -*-
'''
use dbscan algorithm to segment img of soil;
'''
import logging

logger = logging.getLogger("utility")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch_formatter = logging.Formatter('%(levelname)s - %(message)s')
ch.setFormatter(ch_formatter)
logger.addHandler(ch)

#test
# a = [1,2,3,6]
# logger.debug('debug%s',a)
# logger.debug(a)
# logger.info('info%s',a)
# logger.warning('warning')
# logger.error("error")