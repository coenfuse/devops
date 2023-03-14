# description about this module in 50 words
# ..


# standard imports
from typing import List

# internal imports
# ..

# module imports
from lamina.utils import stdlog
from lamina.drivers.mqtt import Subscription

# thirdparty imports
# ..



# ==============================================================================
# TODO : docs
# ==============================================================================
class Configurator:

    # TODO : docs
    # --------------------------------------------------------------------------
    def __init__(self, config: dict):
        self.__config: dict = config
        try:
            subs = self.__config.get("subs")
            subscriptions = []
            for sub in subs:
                sub_obj = Subscription()
                sub_obj.mid = sub["mid"]
                sub_obj.qos = sub["qos"]
                sub_obj.topic = sub["topic"]
                subscriptions.append(sub_obj)

            self.__config["subs"] = subscriptions

        except Exception as e:
            stdlog.error(f"config parse FAILURE with exception: {e}")


    # TODO : add inspect() maybe, consider benefit of non-exception behavior
    # --------------------------------------------------------------------------
    # ..


    # TODO : docs
    # --------------------------------------------------------------------------
    def get_client_id(self) -> str:
        return "tuco"


    # TODO : docs
    # --------------------------------------------------------------------------
    def get_is_clean_session(self) -> bool:
        return self.__config["session"]["clean"]


    # TODO : docs
    # --------------------------------------------------------------------------
    def get_host(self) -> str:
        return self.__config["host"]["ip"]


    # TODO : docs
    # --------------------------------------------------------------------------
    def get_port(self) -> int:
        return self.__config["host"]["port"]


    # TODO : docs
    # --------------------------------------------------------------------------
    def get_keep_alive_s(self) -> int:
        return self.__config["session"]["timeout_s"]


    # TODO : docs
    # --------------------------------------------------------------------------
    def get_username(self) -> str:
        return self.__config["auth"]["username"]


    # TODO : docs
    # --------------------------------------------------------------------------
    def get_password(self) -> str:
        return self.__config["auth"]["password"]


    # TODO : docs
    # --------------------------------------------------------------------------
    def get_subscriptions(self) -> List[Subscription]:
        return self.__config["subs"]