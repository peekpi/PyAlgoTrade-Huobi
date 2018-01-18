import liveLogger

logger = liveLogger.getLiveLogger("Exception")

def ErrorShow(msg):
    logger.warning(msg.encode('utf8'))

