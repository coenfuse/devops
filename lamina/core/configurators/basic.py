# standard imports
import tomllib
from typing import Dict

# package imports
from lamina.utils.error import ERC

# thirdparty imports
# ..



# ==============================================================================
# NOTE : I currently do not find any significant reason to use logging library 
# for printing config messages. Since configuration is going to be called very
# frequently but it is always going to return only static data. Which can be
# verified manually by inspecting the file.
#
# This is the root configurator for the Lamina application, this is a class that
# parses and handles the main Lamina's TOML formatted config file. This 
# configurator is used as the parent and source for all sub-config components
# throughout the application. Since this configurator is going to be initialized
# once and used everywhere, it is designed as a Singleton. 
# ==============================================================================
class Configurator:

    NAME: str = "CONFIG   : [MAIN]"
    DATA: dict= {}


    @staticmethod
    def parse(config_path) -> ERC:
        try:
            print(f"{Configurator.NAME} reading config at - {config_path}")
            Configurator.DATA = tomllib.load(open(config_path, mode = "rb"))
            
            # TODO self.__inspect()
            return ERC.SUCCESS
      
        except Exception as e:
            print(f"{Configurator.NAME} exception - {e}")
            return ERC.EXCEPTION


    @staticmethod
    def get_app_config() -> Dict[str, any] | ERC :
        try:
            return Configurator.DATA["lamina"]
        except Exception as e:
            print(f"{Configurator.NAME} exception - {e}")
            return ERC.EXCEPTION
        

    @staticmethod
    def get_inputs_config() -> Dict[str, dict] | ERC:
        try:
            return Configurator.DATA["inputs"]
        except Exception as e:
            print(f"{Configurator.NAME} exception - {e}")
            return ERC.EXCEPTION
    

    @staticmethod
    def get_that_input_config(type: str, name: str) -> Dict[str, any] | ERC:
        try:
            return Configurator.DATA["inputs"][type][name]
        except Exception as e:
            print(f"{Configurator.NAME} exception - {e}")
            return ERC.EXCEPTION


    @staticmethod
    def get_outputs_config() -> Dict[str, any] | ERC:
        try:
            return Configurator.DATA["outputs"]
        except Exception as e:
            print(f"{Configurator.NAME} exception - {e}")
            return ERC.EXCEPTION
        

    @staticmethod
    def get_that_output_config(type: str, name: str) -> Dict[str, any] | ERC:
        try:
            return Configurator.DATA["outputs"][type][name]
        except Exception as e:
            print(f"{Configurator.NAME} exception - {e}")
            return ERC.EXCEPTION

    
    @staticmethod
    def get_stream_config() -> Dict[str, any] | ERC:
        try:
            return Configurator.DATA["stream"]
        except Exception as e:
            print(f"{Configurator.NAME} exception - {e}")
            return ERC.EXCEPTION