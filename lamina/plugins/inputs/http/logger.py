# standard imports
import logging

# internal imports
# ..

# module imports
from lamina.utils import stdlog

# thirdparty imports
# ..



class HTTPLog:
    
    __logger = None

    @staticmethod
    def configure(tag, level):
        HTTPLog.__logger = stdlog.create_logger("input.http", tag, level)

    @staticmethod
    def trace(message: str) -> None:
        if HTTPLog.__logger is not None:
            HTTPLog.__logger.log(5, message)

    @staticmethod
    def debug(message: str) -> None:
        if HTTPLog.__logger is not None:
            HTTPLog.__logger.debug(message)

    @staticmethod
    def info(message: str) -> None:
        if HTTPLog.__logger is not None:
            HTTPLog.__logger.info(message)

    @staticmethod
    def warn(message: str) -> None:
        if HTTPLog.__logger is not None:
            HTTPLog.__logger.warn(message)

    @staticmethod
    def error(message: str) -> None:
        if HTTPLog.__logger is not None:
            HTTPLog.__logger.error(message)

    @staticmethod
    def critical(message: str) -> None:
        if HTTPLog.__logger is not None:
            HTTPLog.__logger.critical(message)