# standard imports
import tomllib
from typing import Dict

# package imports
from lamina.utils.error import ERC
from lamina.utils import typing

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
        print(f"{Configurator.NAME} reading config at - {config_path}")
        
        try: Configurator.DATA = tomllib.load(open(config_path, mode = "rb"))
        except Exception as e:
            print(f"{Configurator.NAME} exception - {e}")
            return ERC.EXCEPTION
        
        Configurator.__inspect()        # may raise errors
        return ERC.SUCCESS


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
        

    # NSFW content below, proceed at your own risk!
    @staticmethod
    def __inspect() -> None:
        
        # inspect, verify and handle application level configs
        suspect: dict = Configurator.get_app_config()
        if "instance" in suspect:
            typing.is_str(suspect["instance"], "lamina.instance")
        else:
            Configurator.DATA["lamina"]["instance"] = ""

        if "log" in suspect:
            if "stdout" in suspect["log"]:
                if "level" not in suspect["log"]["stdout"]:
                    raise KeyError("Missing 'level' config key in 'lamina.log.stdout'")
                elif typing.is_int(suspect["log"]["stdout"]["level"], "lamina.log.stdout.level"):
                    if suspect["log"]["stdout"]["level"] not in [0, 1, 2, 4, 5]:
                        raise ValueError(f"Invalid lamina.log.stdout.level = {suspect['log']['stdout']['level']} specified. Must be within 0 to 5.")
            
            if "fileout" in suspect["log"]:
                if "level" not in suspect["log"]["fileout"]:
                    raise KeyError("Missing 'level' config key in 'lamina.log.fileout'")
                elif typing.is_int(suspect["log"]["fileout"]["level"], "lamina.log.fileout.level"):
                    if suspect["log"]["fileout"]["level"] not in [0, 1, 2, 4, 5]:
                        raise ValueError(f"Invalid lamina.log.fileout.level = {suspect['log']['fileout']['level']} specified. Must be within 0 to 5.")               
                
                if "path" not in suspect["log"]["fileout"]:
                    raise KeyError("Missing 'path' config key in 'lamina.log.fileout'")
                else:
                    typing.is_str(suspect["log"]["fileout"]["path"], "lamina.log.fileout.path")

        # inspect and verify input plugins listings
        # suspect: dict = Configurator.get_inputs_config()

        # inspect and verify output plugins listings
        # suspect: dict = Configurator.get_outputs_config()

        # inspect and verify stream configuration
        # TODO : check the validity of plugin references, like the actual strings (maybe use regex)
        suspect: dict = Configurator.get_stream_config()
        if typing.is_list(suspect["inputs"], "stream.inputs"):
            if len(suspect['inputs']) == 0:
                raise ValueError("stream.inputs can't be empty. Must have atleast one input plugin mentioned.")
            for inplug in suspect["inputs"]:
                if typing.is_str(inplug, "stream.inputs"):
                    if list(suspect["inputs"]).count(inplug) > 1:
                        raise ValueError(f"Duplicate input plugin mentioned for '{inplug}'")

        if typing.is_list(suspect["outputs"], "stream.outputs"):
            if len(suspect['outputs']) == 0:
                raise ValueError("stream.outputs can't be empty. Must have atleast one output plugin mentioned.")
            for outplug in suspect["outputs"]:
                if typing.is_str(outplug, "stream.outputs"):
                    if list(suspect["outputs"]).count(outplug) > 1:
                        raise ValueError(f"Duplicate output plugin mentioned for '{outplug}'")