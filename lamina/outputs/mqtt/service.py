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
from lamina.outputs.mqtt.config import Configuration

# module imports
from lamina.core.buffers.membuff import MemQueue
from lamina.core.utils import stdlog
from lamina.drivers.mqtt import Agent as Client
from lamina.core.utils.error import ERC

# thirdparty imports
import json5


# ------------------------------------------------------------------------------
class MQTT_Output_Service:
    def __init__(self, raw_config: str):
        self.__NAME   = "MQTTSRV_O"
        self.__config = Configuration(raw_config)
        self.__client: Client = None
        
        self.__buffer = MemQueue()
        self.__buffer.add_queue("inbox")
        
        self.__publisher = Thread(target = self.__publish_job)
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
        self.__publisher.join(timeout = 5)
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


    # TODO : Add facility for supporting failed messages, that are saved in separate
    # buffer (file maybe?)
    def __publish_job(self):
        while not self.__is_requested_stop:
            message = self.__buffer.peek("inbox")       # blocking
            if message is not None:
                message.topic = "lamina/send"
                
                stdlog.debug(f"{self.__NAME} : sending message {message.payload}")
                self.__client.publish(message)

                # if publish is successful
                self.__buffer.pop("inbox")

                sleep(self.__config.get_publish_rate_s())
