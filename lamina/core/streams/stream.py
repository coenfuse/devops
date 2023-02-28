# description about this module in 50 words
# ..


# standard imports
# ..

# internal imports
import json

# module imports
from lamina.core.utils.error import ERC
from lamina.core.buffers.membuff import MemBuff
from lamina.inputs.mqtt import MQTT_Input_Agent, Configuration
from lamina.outputs.mqtt import MQTT_Output_Service

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
            self.__outputs = MQTT_Output_Service(json.dumps(config.get_output_mqtt()))
            self.__inputs = MQTT_Input_Agent(Configuration(json.dumps(config.get_input_mqtt())), self.__buffer_mq)            
            # ..
            return ERC.SUCCESS

        def start(self) -> ERC:
            self.__inputs.start()
            self.__outputs.start()
            return ERC.SUCCESS

        def stop(self) -> ERC:
            self.__outputs.stop()
            self.__inputs.stop()
            return ERC.SUCCESS

        def is_running(self) -> bool:
            return self.__inputs.is_active() and self.__outputs.is_active()
            return True