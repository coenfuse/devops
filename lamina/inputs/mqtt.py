# description about this module in 50 words
# ..


# standard imports
from typing import List

# internal imports
from lamina.inputs import Base_Waiting_Agent

# module imports
from lamina.codecs import jsoncodec
from lamina.core.utils import stdlog
from lamina.drivers.mqtt import Agent, Subscription, Message
from lamina.core.utils.error import ERC

# thirdparty imports
# ..


class Configuration:
    def __init__(self, config):
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

    def get_client_id(self) -> str:
        return "tuco"

    def get_is_clean_session(self) -> bool:
        return self.__config["session"]["clean"]

    def get_host(self) -> str:
        return self.__config["host"]["ip"]

    def get_port(self) -> int:
        return self.__config["host"]["port"]

    def get_keep_alive_s(self) -> int:
        return self.__config["session"]["timeout_s"]

    def get_username(self) -> str:
        return self.__config["auth"]["username"]

    def get_password(self) -> str:
        return self.__config["auth"]["password"]

    def get_subscriptions(self) -> List[Subscription]:
        return self.__config["subs"]



class MQTT_Input_Agent:
    def __init__(self, config: Configuration, on_recv_cb):
        self.__NAME   = "MQTTSRV_I"
        self.__config = config
        self.__filter = None            # create a filter with the passed config
        self.__client: Agent = None
        self.__on_recv_cb = on_recv_cb

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
        message = Message(message)
        # open_msg = jsoncodec.decode(message.payload)
        # filt_msg = 
        stdlog.debug(f"{self.__NAME} : recv message {message.payload}")
        self.__on_recv_cb(message)

        # use the created filter to parse/sanitize the received message
        # then send the data-block to specified callback where something happens
        # to that data object.

    # TODO : Add a reconnector that ensures consistent connection. More like an 
    # internal watchdog but a lazy one. Since it requires a whip to activate.