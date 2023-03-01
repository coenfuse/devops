# standard imports
import enum
import queue
import threading

# third-party imports
# ..

#      cl         fn                                      fn             cl 
#    Driver     Decoder                                 Encoder        Driver
#      |           |                                       |_____________|
#      |           |                                                     |
#      v           V                                                     v
# Input Agent--->Filter--->[Combiner]--->[Processor]--->[Router]--->Output Agent
#      A          srv          srv           srv          srv            A
#      |                                                                 |
#      |                                                                 |
# Input Base                                                        Output Base
#     srv                                                               srv

class ERC(enum.Enum):
    SUCCESS = 0
    FAILURE = 1
    EXCEPTION = 2

# A simple queuing database the supports secure thread-locking and could contain
# multiple multi-prod, multi-cons 
class LMDB:
    def __init__(self):
        self.__block = {}
        self.__block.setdefault(None)
        
    def make_buffer(self, key, size = 0):
        self.__block[key] = queue.Queue(maxsize = size)

    def push(self, key, value):
        if key in self.__block:
            queue.Queue(self.__block[key]).put(value, block = True, timeout = None)      # Push value in buffer as soon as buffer is available else wait

    def pop(self, key) -> any:
        if key in self.__block:
            return queue.Queue(self.__block[key]).get(block = True, timeout = None)      # Pop value from buffer as soon as buffer is available else wait 



# A random input decoder for a particular data type (that will be specified) by
# the config file that parses the input from input agent into an open dictionary
def data_decoder(raw_data) -> dict:
    pass

# A simple filter agent that pulls data from the central pipe and pulls raw msgs
# from the inbox
class Filter:
    def __init__(self):
        pass

    def configure(self, filter_config) -> ERC:
        pass

    def start(self) -> ERC:
        pass

    def stop(self) -> ERC:
        pass

    def is_running(self) -> bool:
        pass


# Simple wrapper over paho.mqtt library that provides the using agent a minimal
# interface for communicating messages over a MQTT network
class MQTT_Driver:
    def __init__(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass

    def is_connected(self):
        pass

    def subscribe(self):
        pass

    def publish(self):
        pass


# A input collection service that connects over MQTT network using the MQTT driver
# and dumps the decoded input into database using the specified decoder.
class MQTT_Input_Agent:
    def __init__(self):
        self.__NAME = "IAGT-MQTT"
        self.__is_requested_stop = False
        self.__runtime = threading.Thread(target = self.__collector)

    def configure(self, host, port, subscription):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def is_running(self):
        pass

    def __collector(self):
        pass


