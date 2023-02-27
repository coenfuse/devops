# description about this module in 50 words
# ..


# standard imports
# ..

# internal imports
import json

# module imports
from lamina.core.utils.codes import ERC
from lamina.core.buffers.membuff import MemBuff
from lamina.inputs.mqtt import MQTT_Input_Agent, Configuration

# thirdparty imports
# ..



class Stream:
        def __init__(self):
            self.__buffer_mq = None
            self.__inputs = None
            self.__combiner = None
            self.__processor = None
            self.__router = None
            self.__outputs = None

        def configure(self, config) -> ERC:
            self.__buffer_mq = MemBuff()
            self.__inputs = MQTT_Input_Agent(Configuration(json.dumps(config.get_input_mqtt())), self.__buffer_mq)            
            # ..
            return ERC.SUCCESS

        def start(self) -> ERC:
            self.__inputs.start()
            return ERC.SUCCESS

        def stop(self) -> ERC:
            self.__inputs.stop()
            return ERC.SUCCESS

        def is_running(self) -> bool:
            return self.__inputs.is_active()
            return True