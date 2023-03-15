# this mqtt based output service handles all the outbound messages to a remote
# MQTT broker. Any interested component can request this service to publish 
# messages given that the agent is connected to the broker. In case of the 
# connection is dropped, the service will maintain a local buffer to store all 
# the pending outbound messages. Once the service reconnects to the broker, it 
# will resume pushing the messages to the broker.


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


# ------------------------------------------------------------------------------
class MQTT_Output_Plugin:

    # docs
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__CNAME   = "OUTPLUG - MQTT"
        self.__client: _MQTTDriver_ = None
        
        self.__buffer = MemQueue()
        self.__buffer.add_queue("outbox")
        
        self.__publisher = Thread(target = self.__publish_job)
        self.__is_requested_stop = True


    # docs
    # --------------------------------------------------------------------------
    def configure(self, client_id: str, config: dict) -> ERC:
        self.__client_id = client_id
        self.__config = Configuration(config)
        return ERC.SUCCESS


    # docs
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

        self.__is_requested_stop = False
        self.__publisher.start()

        return status


    # docs
    # --------------------------------------------------------------------------
    def stop(self):
        status = ERC.SUCCESS
        self.__is_requested_stop = True
        self.__publisher.join()
        self.__client.disconnect()
        self.__client = None


    # docs
    # --------------------------------------------------------------------------
    def is_active(self) -> bool:
        return self.__client.is_connected()


    # The following method can be called by any interested instance. The plugin
    # will ensure the publishing of message either instantly, after time_interval,
    # or whenever the connection resumes.
    # --------------------------------------------------------------------------
    def request_send(self, message):
        # TODO : encode the message using appropriate encoder
        self.__buffer.push("outbox", message)

    # TODO : Implement the reconnector, this ensures the client is cleared, and
    # restarted cleanly. This must happen only if approval is given via application
    # config and must be activated after a certain threshold only. Like failcount.
    # ---------------------------------------------------------------------------
    def __reconnect_on_fail(self):
        pass


    # TODO : Add facility for supporting failed messages, that are saved in 
    # separate buffer (file maybe?)

    # Publishes queued messages to a broker using a client at a configured topic. 
    # It waits for outbound messages of type Message in an internal buffer queue,
    # sends a copy to the broker, pops the original message from the queue after
    # a successful publish
    # --------------------------------------------------------------------------
    def __publish_job(self):
        while not self.__is_requested_stop:
            try: 
                message = self.__buffer.peek("outbox", timeout_s = 5)
                if isinstance(message, _MQTTMessage_):
                    message.topic = self.__config.get_publish_topic()           # must be assigned by processor, may be removed later        
                    if self.__client.publish(message) == 0:
                        self.__buffer.pop("outbox")

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
