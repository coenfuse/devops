# standard imports
# ..

# internal imports
# ..

# module imports
from lamina.core.utils import stdlog

# thirdparty imports
import json5


class Configuration:
    def __init__(self, config: dict):
        self.__config: dict = config

    def get_client_id(self) -> str:
        return "banana"

    def get_host(self) -> str:
        return self.__config["host"]["ip"]

    def get_port(self) -> int:
        return self.__config["host"]["port"]

    def get_username(self) -> str:
        return self.__config["auth"]["username"]

    def get_password(self) -> str:
        return self.__config["auth"]["password"]

    def get_is_clean_session(self) -> bool:
        return self.__config["session"]["clean"]
    
    def get_keep_alive_s(self) -> int:
        return self.__config["session"]["timeout_s"]

    def get_to_reconnect(self) -> bool:
        return self.__config["session"]["reconnect_on_fail"]
    
    def get_reconnect_fail_count(self) -> bool:
        return self.__config["session"]["reconnect_timeout_s"]

    def get_publish_topic(self) -> str:
        return self.__config["pubs"][0]["topic"]

    def get_publish_rate_s(self) -> int:
        return self.__config["pubs"][0]["rate_s"]