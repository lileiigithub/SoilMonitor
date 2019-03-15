# -*- coding: utf-8 -*-
'''
use dbscan algorithm to segment img of soil;
'''
import logging

class SMLog(object):
    logger =  logging.getLogger("SoilMonitor")
    logger.setLevel(logging.DEBUG)
    consoleHandle = logging.StreamHandler()
    consoleHandle.setLevel(logging.DEBUG)
    ch_formatter = logging.Formatter('%(levelname)s - %(message)s')
    consoleHandle.setFormatter(ch_formatter)
    logger.addHandler(consoleHandle)

    # def __init__(self):
    #     pass

    @staticmethod
    def debug(msg, *args, **kwargs):
        SMLog.logger.debug(msg, *args, **kwargs)

    @staticmethod
    def info(msg, *args, **kwargs):
        SMLog.logger.info(msg, *args, **kwargs)

    @staticmethod
    def warning(msg, *args, **kwargs):
        SMLog.logger.warning(msg, *args, **kwargs)

    @staticmethod
    def error(msg, *args, **kwargs):
        SMLog.logger.error(msg, *args, **kwargs)


if __name__ == '__main__':
    num = 0
    SMLog.debug("debug:%s",num)
    SMLog.info(num)
    SMLog.error("error")


