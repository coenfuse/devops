# standard imports
# ..

# internal imports
# ..

# module imports
from lamina.core.utils import stdlog

# thirdparty imports
import json5


class Configuration:
    def __init__(self, raw_config):
        self.__config: dict = {}
        try:
            self.__config: dict = json5.loads(raw_config)
        except Exception as e:
            stdlog.error(f"config parse FAILURE with exception: {e}")

    def get_client_id(self) -> str:
        return self.__config["client_id"]

    def get_is_clean_session(self) -> bool:
        return self.__config["is_clean_session"]

    def get_host(self) -> str:
        return self.__config["host"]

    def get_port(self) -> int:
        return self.__config["port"]

    def get_keep_alive_s(self) -> int:
        return self.__config["keep_alive_s"]

    def get_username(self) -> str:
        return self.__config["username"]

    def get_password(self) -> str:
        return self.__config["password"]

    def get_publish_topic(self) -> dict:
        return self.__config["publish_to"]

    def get_publish_rate_s(self) -> int:
        return self.__config["publish_rate_s"]

    def get_to_reconnect(self) -> bool:
        return self.__config["reconnect_on_fail"]

    def get_reconnect_fail_count(self) -> int:
        return self.__config["reconnect_threshold"]