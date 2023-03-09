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
from lamina.core.configurators.basic import Configurator
from lamina.core.utils.error import ERC
from lamina.core.buffers.membuff import MemQueue
from lamina.inputs.mqtt import MQTT_Input_Agent, Configuration
from lamina.outputs.mqtt import MQTT_Output_Service

# thirdparty imports
# ..



class Stream:
    def __init__(self):
        self.__buffer_mq: MemQueue = None
        self.__input = None
        self.__output = None

        # self.__combiner = None
        # self.__processor = None
        # self.__router = None

        self.__relay_service = Thread(target = self.__relayer, name = "input_stream_handler")
        self.__is_requested_stop = True


    def configure(self, config: Configurator) -> ERC:
        self.__buffer_mq = MemQueue()
        self.__buffer_mq.add_queue("inbox")

        self.__output = MQTT_Output_Service(config.get_that_output_config('mqtt', 'bambo'))
        
        self.__input = MQTT_Input_Agent(
            config = Configuration(config.get_that_input_config('mqtt', 'rambo')), 
            on_recv_cb = lambda data : self.__buffer_mq.push("inbox", data))
        
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
            try:
                item = self.__buffer_mq.pop("inbox", timeout_s = 2)
                if item is not None:
                    self.__output.request_send(item)
            except:
                pass