# description about this module in 50 words
# ..


# standard imports
from time import sleep

# internal imports
from lamina.plugins.inputs.mqtt.config import Configurator

# module imports
from lamina.drivers.mqtt import MQTTClient as _MQTTDriver_
from lamina.drivers.mqtt import Message as _MQTTMessage_
from lamina.utils.error import ERC

# thirdparty imports
# ..



# ==============================================================================
# TODO : docs
# ==============================================================================
class MQTT_Input_Plugin:

    # TODO : docs
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__NAME   = "INPLUG - MQTT"
        self.__client: _MQTTDriver_ = None


    # TODO : docs and checks
    # --------------------------------------------------------------------------
    def configure(self, client_id: str, config: dict, on_recv_cb) -> ERC:
        self.__client_id = client_id
        self.__config = Configurator(config)
        self.__on_recv_cb = on_recv_cb
        return ERC.SUCCESS


    # TODO : docs
    # --------------------------------------------------------------------------
    def start(self) -> ERC:
        status = ERC.SUCCESS
        self.__client = _MQTTDriver_(
            client_id = self.__client_id, 
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


    # TODO : docs
    # --------------------------------------------------------------------------
    def stop(self):
        status = ERC.SUCCESS
        
        for subscription in self.__config.get_subscriptions():
            self.__client.unsubscribe(subscription)

        self.__client.disconnect()
        self.__client = None


    # TODO : docs
    # --------------------------------------------------------------------------
    def is_active(self) -> bool:
        return self.__client.is_connected()


    # This function will be called whenever a new message is received on MQTT by
    # the MQTT Agent
    # --------------------------------------------------------------------------
    def __generic_msg_collector(self, client_ref, userdata, message):
        message = _MQTTMessage_(message)
        self.__on_recv_cb(message)

        # use the created filter to parse/sanitize the received message
        # then send the data-block to specified callback where something happens
        # to that data object.

    # TODO : Add a reconnector that ensures consistent connection. More like an 
    # internal watchdog but a lazy one. Since it requires a whip to activate.