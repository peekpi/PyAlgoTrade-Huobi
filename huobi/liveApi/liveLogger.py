import logging
from pyalgotrade import logger
import liveUtils

log_format = "%(asctime)s %(name)s [%(levelname)s] %(message)s"
level = logging.INFO
file_log = "/tmp/huobi.log"

fileHandler = None


class Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        return "[%s]"%liveUtils.localTime()

def initLogger(logger):
    global fileHandler
    if fileHandler is None:
        fileHandler = logging.FileHandler(file_log)
        fileHandler.setFormatter(log_format)
        fileHandler.setFormatter(Formatter(log_format))
    logger.addHandler(fileHandler)

def getLiveLogger(name):
    log = logger.getLogger(name)
    initLogger(log)
    return log

