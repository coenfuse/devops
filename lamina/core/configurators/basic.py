# standard imports
import tomllib
from typing import Dict

# package imports
from lamina.utils.error import ERC

# thirdparty imports
# ..



# ==============================================================================
# TODO : Docs.
# I currently do not find any significant reason to use logging library for
# printing config messages. Since configuration is going to be called very
# frequently but it is always going to return only static data. Which can be
# verified manually by inspecting the file.
# ==============================================================================
class Configurator:

    # docs
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__CNAME: str = "CONFIG   : [MAIN]"
        self.__data: dict = None

    # docs
    # --------------------------------------------------------------------------
    def parse(self, config_path) -> ERC:
        try:
            print(f"{self.__CNAME} reading config at - {config_path}")
            self.__data = tomllib.load(open(config_path, mode = "rb"))
            # self.inspect()
            return ERC.SUCCESS
      
        except Exception as e:
            print(f"{self.__CNAME} exception - {e}")
            return ERC.EXCEPTION

    # docs
    # --------------------------------------------------------------------------
    def get_app_config(self) -> Dict[str, any] | ERC :
        try:
            return self.__data["lamina"]
        except Exception as e:
            print(f"{self.__CNAME} exception - {e}")
            return ERC.EXCEPTION
        
    # docs
    # --------------------------------------------------------------------------
    def get_inputs_config(self) -> Dict[str, any] | ERC:
        try:
            return self.__data["inputs"]
        except Exception as e:
            print(f"{self.__CNAME} exception - {e}")
            return ERC.EXCEPTION
    
    # docs
    # --------------------------------------------------------------------------
    def get_that_input_config(self, type: str, name: str) -> Dict[str, any] | ERC:
        try:
            return self.__data["inputs"][type][name]
        except Exception as e:
            print(f"{self.__CNAME} exception - {e}")
            return ERC.EXCEPTION

    # docs
    # --------------------------------------------------------------------------
    def get_outputs_config(self) -> Dict[str, any] | ERC:
        try:
            return self.__data["outputs"]
        except Exception as e:
            print(f"{self.__CNAME} exception - {e}")
            return ERC.EXCEPTION
        
    # docs
    # --------------------------------------------------------------------------
    def get_that_output_config(self, type: str, name: str) -> Dict[str, any] | ERC:
        try:
            return self.__data["outputs"][type][name]
        except Exception as e:
            print(f"{self.__CNAME} exception - {e}")
            return ERC.EXCEPTION

    # docs
    # --------------------------------------------------------------------------
    def get_stream_config(self) -> Dict[str, any] | ERC:
        try:
            return self.__data["stream"]
        except Exception as e:
            print(f"{self.__CNAME} exception - {e}")
            return ERC.EXCEPTION