# This module contains implementation of MQTT_Output_Plugin that allows Lamina
# to have subscriptions and receive inbound messages over MQTT network. The
# following plugin uses an internally defined Configurator and MQTT Driver.


# standard imports
from threading import Thread
from typing import Dict

# internal imports
from lamina.plugins.outputs.mqtt.config import Configuration
from lamina.plugins.outputs.mqtt.logger import MQTTLog

# module imports
from lamina.core.buffers.membuff import MemQueue, MQItem
from lamina.drivers.mqtt import MQTTClient as _MQTTDriver_
from lamina.drivers.mqtt import Message as _MQTTMessage_
from lamina.utils.error import ERC

# thirdparty imports
# ..


# ==============================================================================
# This plugins provides functionality for publishing messages to an MQTT broker.
# Any interested component can request this service to publish messages, provided
# the agent is connected to the broker. If the connection is dropped, the service
# will maintain a local buffer to store all the pending outbound messages. Once 
# the service reconnects to the broker, it will resume pushing the messages to 
# the broker. This plugin allows users to publish messages to an MQTT broker, 
# connecting to a single broker at a time that is available locally or remotely.
# Outbound messages are first staged in an outbox buffer, waiting for the publi-
# sher runtime to publish them serially. The functionality of the outbox buffer 
# will be later expanded into publisher rate controlling.
# ==============================================================================
class MQTTOutputPlugin:

    # Simple constructor initializing the name of plugin that will be used in
    # logging and creating an empty client variable that will be laterr initialized
    # MQTTClient object
    # We also initialize a buffer instance that will store all the outbound msgs
    # and a publishing service thread that will use that buffer to actually send
    # out the messages to MQTT broker
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__client: _MQTTDriver_ = None                                      # type: ignore (sonarlint)
        self.__logger_name = ""
        self.log = MQTTLog()
        
        self.__buffer = MemQueue()
        self.__buffer.add_queue("outbox")
        
        self.__publisher = Thread(target = self.__publish_job)
        self.__is_requested_stop = True


    # Configure the Plugin
    # - name   : used here as client id, plugin will create a client instance
    #            with this name
    # - config : config block from global configuration
    # --------------------------------------------------------------------------
    def configure(self, name: str, config: dict) -> ERC:
        self.__config = Configuration(config, name)  # may raise exceptions
        self.__tag_maps: Dict[str, set] = {}
        
        for each_pub in self.__config.get_publish_topics():
            self.__tag_maps[each_pub["topic"]] = set(each_pub["tags"])

        if self.__config.is_logging_enabled():
            self.log.configure(
                self.__config.get_client_id(),
                self.__config.logging_level())
            
            # fetch and store the logger name in a local variable since that is
            # required to be sent to the MQTT driver for using correct logger
            self.__logger_name = self.log.get_logger_name()

        return ERC.SUCCESS


    # starts te mqtt output plugin by connecting to broker on specified configs
    # and starting the publisher service runtime
    # --------------------------------------------------------------------------
    def start(self) -> ERC:
        status = ERC.FAILURE

        self.__client = _MQTTDriver_(
            client_id = self.__config.get_client_id(),
            clean_session = self.__config.get_is_clean_session(),
            logger = self.__logger_name)

        if self.__client is not None:
            status = ERC.SUCCESS        

        if status == ERC.SUCCESS:
            res = self.__client.connect(
                host = self.__config.get_host(),
                port = self.__config.get_port(),
                keep_alive_s = self.__config.get_keep_alive_s(),
                reconnect_on_fail = self.__config.get_is_reconnect_enabled(),
                reconnect_timeout_s = self.__config.get_reconnect_timeout_s())
            status = ERC.SUCCESS if res == 0 else ERC.FAILURE

        if status == ERC.SUCCESS:
            self.__is_requested_stop = False
            self.__publisher.start()

        if status == ERC.SUCCESS:
            self.log.info("start SUCCESS")
        else:
            self.log.error("start FAILURE")

        return status


    # stops the publishing service, disconnects from broker and deinitializes the
    # MQTT instance variable
    # --------------------------------------------------------------------------
    def stop(self) -> ERC:

        self.__is_requested_stop = True
        self.__publisher.join()
        
        if self.__client.disconnect() == 0:
            self.__client = None                                                # type: ignore (sonarlint)
            self.log.info("stop SUCCESS")
            return ERC.SUCCESS
        else:
            self.log.error("stop FAILURE")
            return ERC.FAILURE


    # seriously?
    # --------------------------------------------------------------------------
    def is_active(self) -> bool:
        return self.__client.is_connected()


    # The following method can be called by any interested instance. The plugin
    # will ensure the publishing of message either instantly, after time_interval,
    # or whenever the connection resumes.
    # --------------------------------------------------------------------------
    def send(self, data: MQItem):
        self.__buffer.push("outbox", self._encode(data))


    # TODO : use appropriate encoders and data serializers while prepping payload
    # --------------------------------------------------------------------------
    @staticmethod
    def _encode(data: MQItem) -> MQItem:
        content = data.get_value()
        
        if not isinstance(content, _MQTTMessage_):
            message = _MQTTMessage_()
            message.payload = str(content)
            data.set_value(message)
        
        return data



    # TODO : Add facility for supporting failed messages, that are saved in 
    # separate buffer (file maybe?)

    # Publishes enqueued msgs to the broker using client at configured topics. A
    # message is only published to a topic if its tag is mentioned in publishing
    # topics
    # 
    # This service waits for outbound messages to arrive in the internal queue,
    # the waiting is finite and throws a timeout every 5 seconds if no message is
    # received. This timeout is handled silently and is required to ensure smooth
    # termination of this process and Lamina itself. 
    # Once an outbound packet is received in the buffer the process pulls a copy
    # of it using peek(). The plugin then 'tries' to publish the outbound packet
    # to all the topics atleast once (given the tag of outbound packet is in
    # publishing topic's allowed tags list) using specified qos and retention. 
    # --------------------------------------------------------------------------
    def __publish_job(self):
        while not self.__is_requested_stop:
            try: 
                mqitem: MQItem = self.__buffer.peek("outbox", timeout_s = 5)    
                
                if mqitem is not None:
                    message: _MQTTMessage_ = mqitem.get_value()       
                
                    for pub_conf in self.__config.get_publish_topics():
                        allowed_tags: set = self.__tag_maps[pub_conf["topic"]]
                
                        if (mqitem.get_tag() in allowed_tags) or (len(allowed_tags) == 0):    
                            message.topic  = pub_conf["topic"]
                            message.qos    = pub_conf["qos"]                            
                            message.retain = pub_conf["retain"]             
                            self.__client.publish(message) 

                    self.__buffer.pop("outbox") 
            
            # Index error will only be raised when the queue is empty
            # No logging required, will be raised after every timeout_s expiration
            # We are not logging any messages here since we want to silently
            # handle this timeout exception since a definite timeout_s in peek()
            # gives us an option of shutting down this publish job gracefully
            # without halting Lamina
            except IndexError as e:
                pass

            # any other exception
            except Exception as e:
                self.log.error(str(e))