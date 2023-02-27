# description about this module in 50 words
# ..


# standard imports
import json
from typing import List

# internal imports
from lamina.inputs import Base_Waiting_Agent

# module imports
from lamina.core.utils import stdlog
from lamina.drivers.mqtt import Agent, Subscription
from lamina.core.utils.codes import ERC

# thirdparty imports
# ..


class Configuration:
    def __init__(self, raw_config):
        self.__config: dict = {}
        try:
            self.__config: dict = json.loads(raw_config)
            raw_subs = self.__config.get("subscriptions")
            subs = []
            for sub in raw_subs:
                sub_obj = Subscription()
                sub_obj.mid = sub["mid"]
                sub_obj.qos = sub["qos"]
                sub_obj.topic = sub["topic"]
                subs.append(sub_obj)

            self.__config["subscriptions"] = subs

            # process all the other nested blocks here as well, e.g. subscriptions
        except Exception as e:
            stdlog.critical(f"config parse FAILURE with exception: {e}")

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

    def get_subscriptions(self) -> List[Subscription]:
        return self.__config["subscriptions"]



class MQTT_Input_Agent:
    def __init__(self, config: Configuration, db_ref):
        self.__config = config
        self.__db_ref = db_ref
        self.__filter = None            # create a filter with the passed config
        self.__client: Agent = None

    def start(self) -> ERC:
        status = ERC.SUCCESS
        self.__client = Agent(
            client_id = self.__config.get_client_id(), 
            clean_session = self.__config.get_is_clean_session(), 
            silent = False)

        self.__client.connect(
            host = self.__config.get_host(), 
            port = self.__config.get_port(), 
            keep_alive_s = self.__config.get_keep_alive_s())

        for subscription in self.__config.get_subscriptions():
            subscription.callback = self.__generic_msg_collector
            self.__client.subscribe(subscription)

        return status

    def stop(self):
        status = ERC.SUCCESS
        
        for subscription in self.__config.get_subscriptions():
            self.__client.unsubscribe(subscription)

        self.__client.disconnect()
        self.__client = None

    def is_active(self) -> bool:
        return self.__client.is_connected()

    # This function will be called whenever a new message is received on MQTT by
    # the MQTT Agent
    def __generic_msg_collector(self, client_ref, userdata, message):
        print(f"recv new message {message.payload}")
        # use the created filter to parse/sanitize the received message
        # then push the created data-block into the central data buffer using
        # the passed db reference