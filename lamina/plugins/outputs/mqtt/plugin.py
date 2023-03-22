# This module contains implementation of MQTT_Output_Plugin that allows Lamina
# to have subscriptions and receive inbound messages over MQTT network. The
# following plugin uses an internally defined Configurator and MQTT Driver.


# standard imports
from threading import Thread

# internal imports
from lamina.plugins.outputs.mqtt.config import Configuration

# module imports
from lamina.core.buffers.membuff import MemQueue
from lamina.drivers.mqtt import MQTTClient as _MQTTDriver_
from lamina.drivers.mqtt import Message as _MQTTMessage_
from lamina.utils.error import ERC
from lamina.utils import stdlog

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
class MQTT_Output_Plugin:

    # Simple constructor initializing the name of plugin that will be used in
    # logging and creating an empty client variable that will be laterr initialized
    # MQTTClient object
    # We also initialize a buffer instance that will store all the outbound msgs
    # and a publishing service thread that will use that buffer to actually send
    # out the messages to MQTT broker
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__CNAME   = "OUTPLUG - MQTT"
        self.__client: _MQTTDriver_ = None
        
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
        return ERC.SUCCESS


    # starts te mqtt output plugin by connecting to broker on specified configs
    # and starting the publisher service runtime
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
            self.__is_requested_stop = False
            self.__publisher.start()

        return status


    # stops the publishing service, disconnects from broker and deinitializes the
    # MQTT instance variable
    # --------------------------------------------------------------------------
    def stop(self) -> ERC:

        status = ERC.SUCCESS
        self.__is_requested_stop = True
        self.__publisher.join()
        
        if self.__client.disconnect() == 0:
            self.__client = None
            return ERC.SUCCESS
        else:
            return ERC.FAILURE


    # seriously?
    # --------------------------------------------------------------------------
    def is_active(self) -> bool:
        return self.__client.is_connected()


    # The following method can be called by any interested instance. The plugin
    # will ensure the publishing of message either instantly, after time_interval,
    # or whenever the connection resumes.
    # --------------------------------------------------------------------------
    def send(self, message):
        # TODO : encode the message using appropriate encoder
        self.__buffer.push("outbox", message)


    # TODO : Add facility for supporting failed messages, that are saved in 
    # separate buffer (file maybe?)

    # Publishes queued messages to a broker using a client at a configured topic. 
    # It waits for outbound messages of type Message in an internal buffer queue,
    # sends a copy to the broker, pops the original message from the queue after
    # a successful publish to all the specified topics
    # --------------------------------------------------------------------------
    def __publish_job(self):
        while not self.__is_requested_stop:
            try: 
                mqitem = self.__buffer.peek("outbox", timeout_s = 5)
                if mqitem is not None:
                    message = mqitem.get_value()
                    if isinstance(message, _MQTTMessage_):
                        publish_status = 0
                        for pub_config in self.__config.get_publish_topics():
                            message.topic = pub_config["topic"]
                            message.qos   = pub_config["qos"]
                            message.mid   = pub_config["mid"]
                            message.retain= pub_config["retain"]
                            publish_status += self.__client.publish(message)        # aggregate all the publish responses
                    
                        if publish_status == 0:                                     # only pop from outbox if all the publishing is done successfully
                            self.__buffer.pop("outbox")

            # TODO : think of removing it since this won't happen most probably
            # when the queue doesn't exist
            except KeyError as e:
                stdlog.critical(f"{self.__CNAME} : buffer queue does not exist")
            
            # Index error will only be raised when the queue is empty
            # No logging required, will be raised after every timeout_s expiration
            except IndexError as e:
                pass

            # any other exception
            except Exception as e:
                stdlog.error(f"{self.__CNAME} : {e}")