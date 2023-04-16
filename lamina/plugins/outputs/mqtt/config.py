# standard imports
from typing import List

# internal imports
# ..

# module imports
from lamina.utils import stdlog

# thirdparty imports
# ..



# ==============================================================================
# TODO : Docs
# ==============================================================================
class Configuration:

    # TODO : docs
    # --------------------------------------------------------------------------
    def __init__(self, config: dict, client_id: str):
        self.__config = {}
        self.__config["id"] = client_id
        self.__inspect(config)              # may raise errors

        # assign config to internal config variable if no errors raised
        # looping in just to not override "id" key
        for key, value in config.items():
            self.__config[key] = value


    # Not adding type or validity checks here, just existence checks. Since types
    # and validity checks are going to handled by the drivers themselves
    # --------------------------------------------------------------------------
    def __inspect(self, suspect) -> None:
        if not isinstance(suspect, dict):
            raise TypeError("Invalid MQTT config block format. Must be a TOML block with header in format -> [outputs.mqtt.<plugin-name>]")

        # inspect host config keys
        if "host" not in suspect or not isinstance(suspect["host"], dict):
            raise KeyError(f"Missing 'host' config group in 'outputs.mqtt.{self.get_client_id()}'")
        else:
            for attr in ["ip", "port"]:
               if attr not in suspect["host"]:
                   raise KeyError(f"Missing '{attr}' config key in 'mqtt.{self.get_client_id()}.host'")

        # inspect session config keys
        if "session" not in suspect or not isinstance(suspect["session"], dict):
            raise KeyError(f"Missing 'session' config group in 'outputs.mqtt.{self.get_client_id()}'")
        else:
            for attr in ["clean", "timeout_s", "reconnect_on_fail", "reconnect_timeout_s"]:
                if attr not in suspect["session"]:
                   raise KeyError(f"Missing '{attr}' config key in 'mqtt.{self.get_client_id()}.session'")

        # inspect publish configs
        if "pubs" not in suspect or not isinstance(suspect["pubs"], list):
            raise KeyError(f"Missing 'pubs' list block. Must have TOML list with headers as -> [[outputs.mqtt.{self.get_client_id()}.pubs]]")
        elif suspect["pubs"] == [{}]:
            raise ValueError(f"Empty 'pubs' list in outputs.mqtt.{self.get_client_id()}. Must have atleast one publish detail")
        else:
            pub_index = 1
            for pub in suspect["pubs"]:
                try:
                    pub["topic"]
                    pub["qos"]
                    pub["retain"]
                    pub["tags"]
                except Exception as e:
                    raise KeyError(f"Missing key: '{e}' in publish config item: {pub_index} in config: outputs.mqtt.{self.get_client_id()}")
                pub_index = pub_index + 1

        # inspect logging config keys [OPTIONAL]
        if "log" in suspect:
            if not isinstance(suspect["log"], dict):
                raise ValueError(f"Invalid 'log' attribute structure in 'outputs.mqtt.{self.get_client_id()}'")
            else:
                for attr in ["level"]:
                    if attr not in suspect["log"]:
                        raise KeyError(f"Missing '{attr}' config key in 'outputs.mqtt.{self.get_client_id()}.log'")

        # .. add more inspections units (if necessary)


    # --------------------------------------------------------------------------
    def get_client_id(self) -> str:
        return self.__config["id"]


    # --------------------------------------------------------------------------
    def get_host(self) -> str:
        return self.__config["host"]["ip"]


    # --------------------------------------------------------------------------
    def get_port(self) -> int:
        return self.__config["host"]["port"]


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
    def get_publish_topics(self) -> List[dict]:
        return self.__config["pubs"]
    
    
    # --------------------------------------------------------------------------
    def is_logging_enabled(self) -> bool:
        return True if "log" in self.__config else False
    

    # --------------------------------------------------------------------------
    def logging_level(self) -> int:
        return self.__config["log"]["level"]