# description about this module in 50 words
# ..


# standard imports
import json
from queue import Queue
from threading import Thread
from time import sleep

# internal imports
# ..

# module imports
from lamina.core.utils.error import ERC
from lamina.core.buffers.membuff import MemBuff
from lamina.inputs.mqtt import MQTT_Input_Agent, Configuration
from lamina.outputs.mqtt import MQTT_Output_Service

# thirdparty imports
# ..



class Stream:
    def __init__(self):
        self.__buffer_mq: MemBuff = None
        self.__input = None
        self.__output = None

        # self.__combiner = None
        # self.__processor = None
        # self.__router = None

        self.__relay_service = Thread(target = self.__relayer)
        self.__is_requested_stop = True


    def configure(self, config) -> ERC:
        self.__buffer_mq = MemBuff()
        self.__buffer_mq.make_buffer("inbox")

        self.__buffer = Queue()

        self.__output = MQTT_Output_Service(json.dumps(config.get_output_mqtt()))
        
        self.__input = MQTT_Input_Agent(
            config = Configuration(json.dumps(config.get_input_mqtt())), 
            on_recv_cb = lambda data : self.__buffer.put(data))
        
        return ERC.SUCCESS


    def start(self):
        self.__is_requested_stop = False
        self.__relay_service.start()
        self.__output.start()
        self.__input.start()
        return ERC.SUCCESS


    def stop(self):
        self.__is_requested_stop = True
        self.__input.stop()
        self.__output.stop()
        self.__relay_service.join(timeout = 5)
        return ERC.SUCCESS

    def is_running(self):
        return self.__input.is_active() or self.__output.is_active() or self.__relay_service.is_alive()

    def __relayer(self):
        while not self.__is_requested_stop:
            item = self.__buffer.get()
            # item = self.__buffer_mq.pop("inbox")
            if item is not None:
                self.__output.request_send(item)