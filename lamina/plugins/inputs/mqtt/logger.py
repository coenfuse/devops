# standard imports
# ..

# internal imports
# ..

# module imports
from lamina.utils import stdlog

# thirdparty imports
# ..


class MQTTLog:

    # NOTE : make sure to use underscores instead of periods as that causes 
    # unnecessary heirarchy in logging that is not required.
    def __init__(self):
        self.__logger = None
    
    def configure(self, name, level):
        self.__logger = stdlog.create_logger(
            name = f"input_mqtt_{name}",
            tag = f"INPUT  : [mqtt.{name}]",
            level = level)

    def get_logger_name(self) -> str:
        return self.__logger.name if self.__logger is not None else ""

    def trace(self, message: str) -> None:
        if self.__logger is not None:
            self.__logger.log(5, message)

    def debug(self, message: str) -> None:
        if self.__logger is not None:
            self.__logger.debug(message)

    def info(self, message: str) -> None:
        if self.__logger is not None:
            self.__logger.info(message)

    def warn(self, message: str) -> None:
        if self.__logger is not None:
            self.__logger.warn(message)

    def error(self, message: str) -> None:
        if self.__logger is not None:
            self.__logger.error(message)

    def critical(self, message: str) -> None:
        if self.__logger is not None:
            self.__logger.critical(message)