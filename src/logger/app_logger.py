import logging

class AppLogger:

    __instance__ = None

    logger = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls.__instance__ is None:
            cls.__instance__ = cls.__new__(cls)
            cls.__instance__.__configure_logger__()
        return cls.__instance__

    def __configure_logger__(self):
        self.logger = logging.getLogger('Application-Logger')
        self.logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    @classmethod
    def debug(cls, message:str):
        AppLogger.instance().logger.debug(message)
    
    @classmethod
    def info(cls, message:str):
        AppLogger.instance().logger.info(message)

    @classmethod
    def warn(cls, message:str):
        AppLogger.instance().logger.warn(message)
        
    @classmethod
    def error(cls, message:str):
        AppLogger.instance().logger.error(message)
