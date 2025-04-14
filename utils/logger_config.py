import logging

def get_logger(name = 'olympic_logger'):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(asctime)s %(levelname)s - %(message)s]')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

