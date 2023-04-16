# standard imports
# ..

# internal imports
# ..

# module imports
from lamina.utils import stdlog

# thirdparty imports
# ..


class MQTTLog:
    
    __logger = None

    @staticmethod
    def configure(tag, level):
        MQTTLog.__logger = stdlog.create_logger("output.mqtt", tag, level)

    @staticmethod
    def get_logger_name() -> str:
        return "output.mqtt"
    
    @staticmethod
    def trace(message: str) -> None:
        MQTTLog.__logger.log(5, message)

    @staticmethod
    def debug(message: str) -> None:
        MQTTLog.__logger.debug(message)

    @staticmethod
    def info(message: str) -> None:
        MQTTLog.__logger.info(message)

    @staticmethod
    def warn(message: str) -> None:
        MQTTLog.__logger.warn(message)

    @staticmethod
    def error(message: str) -> None:
        MQTTLog.__logger.error(message)

    @staticmethod
    def critical(message: str) -> None:
        MQTTLog.__logger.critical(message)