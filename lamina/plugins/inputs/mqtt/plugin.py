# This module contains implementation of MQTT_Input_Plugin that allows Lamina
# to have subscriptions and receive inbound messages over MQTT network. The
# following plugin uses an internally defined Configurator and MQTT Driver.


# standard imports
from time import sleep

# internal imports
from lamina.plugins.inputs.mqtt.config import Configurator

# module imports
from lamina.core.buffers.membuff import MQItem
from lamina.drivers.mqtt import MQTTClient as _MQTTDriver_
from lamina.drivers.mqtt import Message as _MQTTMessage_
from lamina.utils.error import ERC
from lamina.utils import stdlog

# thirdparty imports
# ..


# ==============================================================================
# A simple MQTT input plugin that enables a connection to single broker that is
# available locally or remotely. The plugin also permits multiple subscriptions
# with custom callback, so user can specify different event triggers on receiving
# messages on different topics. This class does not provide input buffering or
# message publishing facility.
# ==============================================================================
class MQTT_Input_Plugin:

    # Simple constructor initializing the name of plugin that will be used in
    # logging and creating an empty client variable that will be later initialzed
    # MQTTClient object
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__NAME   = "INPLUG - MQTT"
        self.__client: _MQTTDriver_ = None


    # Configure the Plugin
    # - name         : plugin will create a client instance with this name. 
    #                  The name must be a non-zero string and unique for both
    #                  broker and for local system.
    # - config       : config block from global configuration
    # - data_handler : A custom message handler that will be invoked whenever
    #                  a new message is received by the client in this plugin
    #                  The handler must take in one parameter that will be 
    #                  receievd message
    # --------------------------------------------------------------------------
    def configure(self, name: str, config: dict, data_handler) -> ERC:
        self.__config = Configurator(config, name)    # may raise exception
        self.__on_recv_cb_hndl = data_handler
        return ERC.SUCCESS


    # starts the mqtt input plugin by connecting to broker on specified configs
    # and subscribing to all the topics mentioned.
    # --------------------------------------------------------------------------
    def start(self) -> ERC:
        status = ERC.FAILURE
        
        self.__client = _MQTTDriver_(
            client_id = self.__config.get_client_id(), 
            clean_session = self.__config.get_is_clean_session(), 
            silent = False)
        
        if self.__client is not None:
            status = ERC.SUCCESS

        if status == ERC.SUCCESS:
            res = self.__client.connect(
                host = self.__config.get_host(), 
                port = self.__config.get_port(), 
                keep_alive_s = self.__config.get_keep_alive_s())
            status = ERC.SUCCESS if res == 0 else ERC.FAILURE

        if status == ERC.SUCCESS:
            for subscription in self.__config.get_subscriptions():
                subscription.callback = self.__generic_msg_collector
                if self.__client.subscribe(subscription) != 0:
                    status = ERC.WARNING
                    break

        return status


    # unsusbscribes from all the topic mentioned in the startup config, disconnects
    # from all the broker and deinitializes the MQTTClient instance variable
    # --------------------------------------------------------------------------
    def stop(self) -> ERC:
        # unsub from all registered topics, don't care about unsubscription response
        # since we are disconnecting from the broker anyway
        for subscription in self.__config.get_subscriptions():
            self.__client.unsubscribe(subscription)

        if self.__client.disconnect() == 0:
            self.__client = None
            return ERC.SUCCESS
        else:
            return ERC.FAILURE
    

    # you really need docs for this too?
    # --------------------------------------------------------------------------
    def is_active(self) -> bool:
        return self.__client.is_connected()


    # This function will be called whenever a new message is received on MQTT by
    # the MQTT Agent
    # --------------------------------------------------------------------------
    def __generic_msg_collector(self, client_ref, userdata, message):
        message = _MQTTMessage_(message)
        # print(f"recv data on {message.topic}")
        mqitem = MQItem(message)
        self.__on_recv_cb_hndl(mqitem)

        # use the created filter to parse/sanitize the received message
        # then send the data-block to specified callback where something happens
        # to that data object.