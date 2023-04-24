# description about this module in 50 words
# ..


# standard imports
# ..

# internal imports
# ..

# module imports
from lamina.core.configurators.basic import Configurator
from lamina.core.buffers.membuff import MemQueue, MQItem
from lamina.plugins.lut import PLUGIN_LUT
from lamina.utils.error import ERC

# thirdparty imports
# ..



# ==============================================================================
# TODO : docs
# ==============================================================================
class Stream:

    # docs
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__inputs = []
        self.__outputs = []


    # docs
    # --------------------------------------------------------------------------
    def configure(self, config: Configurator) -> ERC:
        self.__mq = MemQueue()
        self.__mq.add_queue("inbox")

        for input_plugin in config.get_stream_config().get("inputs"):
            inplug_type, inplug_name = input_plugin.split('.')
            inplug = PLUGIN_LUT.get(f"{inplug_type}_in")()
            inplug.configure(
                name = inplug_name, 
                config = config.get_that_input_config(inplug_type, inplug_name), 
                data_handler = lambda data: self.__passive_router(data))
            self.__inputs.append(inplug)

        for output_plugin in config.get_stream_config().get("outputs"):
            outplug_type, outplug_name = output_plugin.split('.')
            outplug = PLUGIN_LUT.get(f"{outplug_type}_out")()
            outplug.configure(
                name = outplug_name,
                config = config.get_that_output_config(outplug_type, outplug_name))
            self.__outputs.append(outplug)
        
        return ERC.SUCCESS


    # docs
    # --------------------------------------------------------------------------
    def start(self):
        for output_plugin in self.__outputs:
            output_plugin.start()

        for input_plugin in self.__inputs:
            input_plugin.start()

        return ERC.SUCCESS


    # docs
    # --------------------------------------------------------------------------
    def stop(self):
        for input_plugin in self.__inputs:
            input_plugin.stop()

        for output_plugin in self.__outputs:
            output_plugin.stop()

        # self.__relay_service.join(timeout = 5)
        return ERC.SUCCESS


    # docs
    # --------------------------------------------------------------------------
    def is_running(self):
        return all(inplug.is_active() for inplug in self.__inputs) or all(outplug.is_active() for outplug in self.__outputs)

    
    # docs
    # --------------------------------------------------------------------------
    def __passive_router(self, data: MQItem):
        for outplug in self.__outputs:
            outplug.send(data)