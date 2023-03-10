# this mqtt based output service handles all the outbound messages to a remote
# MQTT broker. Any interested component can request this service to publish 
# messages given that the agent is connected to the broker. In case of the 
# connection is dropped, the service will maintain a local buffer to store all 
# the pending outbound messages. Once the service reconnects to the broker, it 
# will resume pushing the messages to the broker.


# standard imports
from queue import Queue
from threading import Thread
from time import sleep

# internal imports
from lamina.plugins.outputs.mqtt.config import Configuration

# module imports
from lamina.core.buffers.membuff import MemQueue
from lamina.core.utils import stdlog
from lamina.drivers.mqtt import Agent as Client
from lamina.drivers.mqtt import Message
from lamina.core.utils.error import ERC

# thirdparty imports
import json5


# ------------------------------------------------------------------------------
class MQTT_Output_Service:
    def __init__(self, config: dict):
        self.__NAME   = "MQTTSRV_O"
        self.__config = Configuration(config)
        self.__client: Client = None
        
        self.__buffer = MemQueue()
        self.__buffer.add_queue("inbox")
        
        self.__publisher = Thread(target = self.__publish_job, name = "output_publisher")
        self.__is_requested_stop = True


    def start(self) -> ERC:
        status = ERC.SUCCESS
        self.__client = Client(
            client_id = self.__config.get_client_id(),
            clean_session = self.__config.get_is_clean_session(),
            silent = False)

        self.__client.connect(
            host = self.__config.get_host(),
            port = self.__config.get_port(),
            keep_alive_s = self.__config.get_keep_alive_s())

        self.__is_requested_stop = False
        self.__publisher.start()

        return status


    def stop(self):
        status = ERC.SUCCESS
        self.__is_requested_stop = True
        self.__publisher.join()
        self.__client.disconnect()
        self.__client = None


    def is_active(self) -> bool:
        return self.__client.is_connected()


    # The following method can be called by any interested instance. The service
    # will ensure the publishing of message either instantly, after time_interval,
    # or whenever the connection resumes.
    def request_send(self, message):
        # TODO : encode the message using appropriate encoder
        self.__buffer.push("inbox", message)

    # TODO : Implement the reconnector, this ensures the client is cleared, and
    # restarted cleanly. This must happen only if approval is given via application
    # config and must be activated after a certain threshold only. Like failcount.
    def __reconnect_on_fail(self):
        pass


    # TODO : Add facility for supporting failed messages, that are saved in 
    # separate buffer (file maybe?)

    # Publishes queued messages to a broker using a client at a configured topic. 
    # It waits for outbound messages of type Message in an internal buffer queue,
    # sends a copy to the broker, pops the original message from the queue after
    # a successful publish, and waits for a specified amount of time (determined
    # by the publish rate parameter) before repeating the process.
    def __publish_job(self):
        while not self.__is_requested_stop:
            try: 
                message = self.__buffer.peek("inbox", timeout_s = 2)
                if isinstance(message, Message):
                    message.topic = self.__config.get_publish_topic()           # must be assigned by processor, may be removed later        
                    if self.__client.publish(message) == 0:
                        self.__buffer.pop("inbox")
                        sleep(self.__config.get_publish_rate_s())

            # when the queue doesn't exist
            except KeyError as e:
                stdlog.critical(f"{self.__NAME} : buffer queue does not exist")
            
            # Index error will only be raised when the queue is empty
            # No logging required, will be raised after every timeout_s expiration
            except IndexError as e:
                pass

            # any other exception
            except Exception as e:
                stdlog.error(f"{self.__NAME} : {e}")
