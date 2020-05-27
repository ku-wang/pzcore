import logging


def log_obj(log_name=1, logger_name='mainModule'):

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter(fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    handler = logging.FileHandler('../logs/{name}.log'.format(name=log_name))
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)

    logger.addHandler(handler)
    logger.addHandler(console)

    return logger


logger = log_obj()

logger.info("creating an instance of subModule.subModuleClass")
logger.info("calling subModule.subModuleClass.doSomething")
logger.info("done with  subModule.subModuleClass.doSomething")
logger.info("calling subModule.some_function")
logger.info("done with subModule.some_function")


class Log_obj(object):
    _file_format = '%(asctime)s  %(filename)s-%(funcName)s  %(levelname)s: %(message)s'
    _console_format = '%(asctime)s  %(filename)s-%(funcName)s  %(levelname)s: %(message)s'
    _logger = logging.getLogger()

    def __init__(self, filename):
        self.filename = filename

    def set_file_formatter(self, format):
        formatter = logging.Formatter(fmt=format)
