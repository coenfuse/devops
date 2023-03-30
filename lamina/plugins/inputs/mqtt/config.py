# standard imports
from typing import List

# internal imports
# ..

# module imports
from lamina.drivers.mqtt import Subscription

# thirdparty imports
# ..



# ==============================================================================
# TODO : docs
# ==============================================================================
class Configurator:

    # TODO : docs
    # --------------------------------------------------------------------------
    def __init__(self, config: dict, client_id: str):
        self.__config = {}
        self.__config["id"] = client_id
        self.__inspect(suspect = config)    # may raise errors

        # assign config to internal config variable if no errors are raised
        # Looping instead of direct assignment to not overwrite "id" key
        for key, value in config.items():
            self.__config[key] = value


    # Not adding type or validity checks here, just existence checks. Since types
    # and validity checks are handled by the drivers themselves
    # --------------------------------------------------------------------------
    def __inspect(self, suspect) -> None:
        if not isinstance(suspect, dict):
            raise TypeError("Invalid MQTT config block format. Must be a TOML block with header in format -> [inputs.mqtt.<plugin_name>]")
        
        # inspect host config keys
        if "host" not in suspect or not isinstance(suspect["host"], dict):
            raise KeyError(f"Missing 'host' config group in 'inputs.mqtt.{self.get_client_id()}'")
        else:
            for attr in ["ip", "port"]:
               if attr not in suspect["host"]:
                   raise KeyError(f"Missing '{attr}' config key in 'mqtt.{self.get_client_id()}.host'")

        # inspect session config keys
        if "session" not in suspect or not isinstance(suspect["session"], dict):
            raise KeyError(f"Missing 'session' config group in 'inputs.mqtt.{self.get_client_id()}'")
        else:
            for attr in [
                "clean", "timeout_s", "reconnect_on_fail", "reconnect_timeout_s"]:
                if attr not in suspect["session"]:
                   raise KeyError(f"Missing '{attr}' config key in 'mqtt.{self.get_client_id()}.session'")

        # inspect subscriptions config
        if "subs" not in suspect or not isinstance(suspect["subs"], list):
            raise KeyError(f"Missing 'subs' list block. Must have TOML list with headers as -> [[inputs.mqtt.{self.get_client_id()}.subs]]")
        elif suspect["subs"] == [{}]:
            raise ValueError(f"Empty 'subs' list in inputs.mqtt.{self.get_client_id()}. Must have atleast one subscription detail")
        else:
            subs_list = []
            sub_index = 1
            for sub in suspect["subs"]:
                sub_obj = Subscription()
                try:
                    sub_obj.qos = sub["qos"]
                    # sub_obj.tag = sub["tag"]
                    sub_obj.topic = sub["topic"]
                except Exception as e:
                    raise KeyError(f"Missing key: '{e}' in subscription item: {sub_index} in config: inputs.mqtt.{self.get_client_id()}")
                subs_list.append(sub_obj)
                sub_index = sub_index + 1
            suspect["subs"] = subs_list

        # .. add more inspection units (if necessary)


    # --------------------------------------------------------------------------
    def get_client_id(self) -> str:
        return self.__config["id"]


    # --------------------------------------------------------------------------
    def get_is_clean_session(self) -> bool:
        return self.__config["session"]["clean"]


    # --------------------------------------------------------------------------
    def get_keep_alive_s(self) -> int:
        return self.__config["session"]["timeout_s"]
    

    # --------------------------------------------------------------------------
    def get_is_reconnect_enabled(self) -> bool:
        return self.__config["session"]["reconnect_on_fail"]
    

    # --------------------------------------------------------------------------
    def get_reconnect_timeout_s(self) -> int:
        return self.__config["session"]["reconnect_timeout_s"]
    

    # --------------------------------------------------------------------------
    def get_host(self) -> str:
        return self.__config["host"]["ip"]


    # --------------------------------------------------------------------------
    def get_port(self) -> int:
        return self.__config["host"]["port"]


    # --------------------------------------------------------------------------
    def get_subscriptions(self) -> List[Subscription]:
        return self.__config["subs"]