# standard imports
import codecs
import os
from typing import List
from typing import Union       # Use this for return hints as Union[type, type]

# internal imports
# ..

# module imports
from lamina.utils import typing

# thirdparty imports
# ..


# ==============================================================================
# TODO : docs
# ==============================================================================
class Configuration:

    # docs
    # --------------------------------------------------------------------------
    def __init__(self, config: dict, client_id: str):
        self.__config = {}
        self.__config["id"] = client_id
        self.__inspect(config)                      # may raise exceptions
        self.__verify(config)                       # ...

        # assign config to internal config variable if no errors are raised
        # Looping instead of direct assignment to not overwrite "id" key
        for key, value in config.items():
            self.__config[key] = value



    # Inspects config blog for EXISTENCE of required paramters. Validity of values
    # is checked by the dependent plugin itself at time of config or running.
    # --------------------------------------------------------------------------
    def __inspect(self, suspect) -> None:
        if not isinstance(suspect, dict):
            raise TypeError("Invalid HTTP config block format. Must be a TOML block with header in format -> [inputs.http.<plugin_name>]")

        # inspect host config keys
        if "host" not in suspect or not isinstance(suspect["host"], dict):
            raise KeyError(f"Missing 'host' config group in 'inputs.http.{self.get_client_id()}'")
        else:
            for attr in ["url"]:
                if attr not in suspect["host"]:
                    raise KeyError(f"Missing '{attr}' config key in 'input.http.{self.get_client_id()}.host'")
            
        # inspect request return Falseconfig keys [OPTIONAL]
        if "req" not in suspect or not isinstance(suspect["req"], dict):
            self.__config["req"] = {
                "method" : "GET",
                "headers": {},
                "params" : {},
                "encoding": "",
                "data" : ""
            }
        else:   #if 'req' config block exists then following keys must be present
            for attr in ["method", "headers", "params", "data", "file", "timeout_s"]:
                if attr not in suspect["req"]:
                    raise KeyError(f"Missing '{attr}' config key in 'inputs.http.{self.get_client_id()}.req'")

        # inspect response config keys
        if "res" not in suspect or not isinstance(suspect["res"], dict):
            raise KeyError(f"Missing 'res' config group in 'inputs.http.{self.get_client_id()}'")
        else:
            for cfg_blk in ["success", "content"]:
                if cfg_blk not in suspect["res"]:
                    raise KeyError(f"Missing '{cfg_blk}' config sub-group in 'inputs.http.{self.get_client_id()}.res'")
            if "success" not in suspect["res"]:
                raise KeyError(f"Missing 'success' status codes array in config sub-group in 'inputs.http.{self.get_client_id()}.res'")
            for attr in ["allow_duplicates", "decoding", "tag", "max_size_bytes"]:
                if attr not in suspect["res"]["content"]:
                    raise KeyError(f"Missing '{attr}' config key in config sub-group in 'inputs.http.{self.get_client_id()}.req.content'")            

        # inspect poll config keys
        if "poll" not in suspect or not isinstance(suspect["poll"], dict):
            raise KeyError(f"Missing 'poll' config group in 'inputs.http.{self.get_client_id()}'")
        else:
            for attr in ["rate_s", "variance_s", "max_attempt"]:
                if attr not in suspect["poll"]:
                    raise KeyError(f"Missing '{attr}' config key in 'inputs.http.{self.get_client_id()}.poll'")

        # inspect logging config keys [OPTIONAL]
        if "log" in suspect:
            if not isinstance(suspect["log"], dict):
                raise ValueError(f"Invalid 'log' attribute structure in 'inputs.http.{self.get_client_id()}'")
            else:
                for attr in ['level']:
                    if attr not in suspect["log"]:
                        raise KeyError(f"Missing '{attr}' config key in 'inputs.http.{self.get_client_id()}.log'")


        # .. add more inspection units (if necessary)



    # [EXPERIMENTAL] verifies validity of all mentioned config parameters
    # --------------------------------------------------------------------------
    def __verify(self, suspect: dict) -> None:
        
        # verify host config keys
        typing.is_url(suspect["host"]["url"], f"http.{self.get_client_id()}.host.url")
                
        # verify req config keys (if exist)
        if "req" in suspect:
            typing.is_str(suspect["req"]["method"], f"inputs.http.{self.get_client_id()}.req.method", "and must be any of these methods 'GET', 'PATCH', 'POST', 'PUT'")
            typing.is_dict(suspect["req"]["headers"], f"inputs.http.{self.get_client_id()}.req.headers", "and must be a TOML key value group as {'key' = 'value'}. Can also be an empty TOML group as well written like e.g. { }")
            typing.is_dict(suspect["req"]["params"], f"inputs.http.{self.get_client_id()}.req.params", "and must be a TOML key value group as {'key' = 'value'}. Can also be an empty TOML group as well written like e.g. { }")
            typing.is_str(suspect["req"]["data"], f"inputs.http.{self.get_client_id()}.req.data")
            typing.is_str(suspect["req"]["file"], f"inputs.http.{self.get_client_id()}.req.file")
            typing.is_int(suspect["req"]["timeout_s"], f"http.{self.get_client_id()}.req.timeout_s", "and must be positive non-zero integer")
            
            if suspect["req"]["method"] not in ["GET", "PATCH", "POST", "PUT"]:
                raise ValueError(f"Invalid http.{self.get_client_id()}.req.method = {suspect['req']['method']} specified. Must be GET, PATCH, POST or PUT")
            
            # It is strongly recommended that you open files in binary mode. This
            # is because Requests may attempt to provide the Content-Length header
            # for you, and if it does this value will be set to the number of 
            # bytes in the file. Errors may occur if you open the file in text mode.
            if os.path.isfile(suspect["req"]["file"]):
                suspect["req"]["file"] = open(suspect["req"]["file"], "rb").read()

            if suspect["req"]["timeout_s"] <= 0:
                raise ValueError(f"Invalid http.{self.get_client_id()}.req.timeout_s = {suspect['req']['timeout_s']}, it must be a positive non-zero integer")

        # verify res config keys
        if "res" in suspect:
            typing.is_list(suspect["res"]["success"], f"inputs.http.{self.get_client_id()}.res", "and it must contain atleast one positive non-zero integer code e.g. [200]")
            typing.is_bool(suspect["res"]["content"]["allow_duplicates"], f"inputs.http.{self.get_client_id()}.res.content.allow_duplicates")
            typing.is_str(suspect["res"]["content"]["decoding"], f"inputs.http.{self.get_client_id()}.res.content.decoding")
            typing.is_str(suspect["res"]["content"]["tag"], f"inputs.http.{self.get_client_id()}.res.content.tag")
            typing.is_int(suspect["res"]["content"]["max_size_bytes"], f"inputs.http.{self.get_client_id()}.res.content.max_size_bytes", "and must be positive non-zero integer")

            if len(suspect["res"]["success"]) == 0:
                raise ValueError(f"Configuration inputs.http.{self.get_client_id()}.res.success can't be an empty array, it must contain atleast one positive non-zero integer code e.g. [200]")

            try: codecs.lookup(suspect["res"]["content"]["decoding"])
            except LookupError:
                if suspect["res"]["content"]["decoding"] in ["auto", "raw"]:
                    pass
                else:
                    raise ValueError(f"Invalid input.http.{self.get_client_id()}.res.content.decoding = {suspect['res']['content']['decoding']}, it must be 'auto', 'raw' or any valid python codec as mentioned in docs") 

            if suspect["res"]["content"]["max_size_bytes"] <= 0:
                raise ValueError(f"Invalid inputs.http.{self.get_client_id()}.res.content.max_size_bytes = {suspect['res']['content']['max_size_bytes']}, it must be a positive non-zero integer")

        # verify poll config keys
        if "poll" in suspect:
            typing.is_int(suspect["poll"]["rate_s"], f"inputs.http.{self.get_client_id()}.poll.rate_s", "and must be positive non-zero integer")
            typing.is_int(suspect["poll"]["variance_s"], f"inputs.http.{self.get_client_id()}.poll.variance_s", "and must be positive non-zero integer")
            typing.is_int(suspect["poll"]["max_attempt"], f"inputs.http.{self.get_client_id()}.poll.max_attempt", "and must be positive non-zero integer")

            if suspect["poll"]["rate_s"] <= 0:
                raise ValueError(f"Invalid input.http.{self.get_client_id()}.poll.rate_s = {suspect['poll']['rate_s']} specified. Must be a positive non-zero integer.")
        
            if suspect["poll"]["variance_s"] < 0:
                raise ValueError(f"Invalid input.http.{self.get_client_id()}.poll.variance_s = {suspect['poll']['variance_s']} specified. Must be a positive integer.")
        
            if suspect["poll"]["max_attempt"] <= 0:
                raise ValueError(f"Invalid input.http.{self.get_client_id()}.poll.max_attempt = {suspect['poll']['max_attempt']} specified. Must be a positive non-zero integer.")

        # verify log config keys
        if "log" in suspect:
            if "level" in suspect["log"]:
                if typing.is_int(suspect["log"]["level"], f"inputs.http.{self.get_client_id}.log.level", "and must be positive non-zero integer"):
                    if suspect["log"]["level"] not in range(0,5):
                        raise ValueError(f"Invalid input.http.{self.get_client_id()}.log.level = {suspect['log']['level']} specified. Must be within 0 to 5.")

    # docs
    # --------------------------------------------------------------------------
    def get_client_id(self) -> str:
        return self.__config["id"]


    # docs
    # --------------------------------------------------------------------------
    def url(self) -> str:
        return self.__config["host"]["url"]


    # docs
    # --------------------------------------------------------------------------
    def method(self) -> str:
        return self.__config["req"]["method"]


    # docs
    # --------------------------------------------------------------------------
    def headers(self) -> dict:
        return self.__config["req"]["headers"]


    # docs
    # --------------------------------------------------------------------------
    def params(self) -> dict:
        return self.__config["req"]["params"]


    # docs
    # --------------------------------------------------------------------------
    def data(self) -> str:
        return self.__config["req"]["data"]
    

    # docs
    # --------------------------------------------------------------------------
    def file(self) -> str:
        return self.__config["req"]["file"]


    # docs
    # --------------------------------------------------------------------------
    def timeout_s(self) -> int:
        return self.__config["req"]["timeout_s"]


    # docs
    # --------------------------------------------------------------------------
    def success_codes(self) -> List:
        return self.__config["res"]["success"]


    # docs
    # --------------------------------------------------------------------------
    def allow_duplicates(self) -> bool:
        return self.__config["res"]["content"]["allow_duplicates"]


    # docs
    # --------------------------------------------------------------------------
    def content_decoder(self) -> str:
        return self.__config["res"]["content"]["decoding"]


    # returns the tag string that will be attached to data received from on this
    # HTTP client from specified URL
    # --------------------------------------------------------------------------
    def tag(self) -> str:
        return self.__config["res"]["content"]["tag"]


    # docs
    # --------------------------------------------------------------------------
    def max_content_size(self) -> int:
        return self.__config["res"]["content"]["max_size_bytes"]


    # docs
    # --------------------------------------------------------------------------
    def poll_rate_s(self) -> int:
        return self.__config["poll"]["rate_s"]


    # docs
    # --------------------------------------------------------------------------
    def poll_variance_s(self) -> int:
        return self.__config["poll"]["variance_s"]


    # docs
    # --------------------------------------------------------------------------
    def max_poll_attempts(self) -> int:
        return self.__config["poll"]["max_attempt"]
    

    # docs
    # --------------------------------------------------------------------------
    def is_logging_enabled(self) -> bool:
        return True if "log" in self.__config else False
    

    # docs
    # --------------------------------------------------------------------------
    def logging_level(self) -> int:
        return self.__config["log"]["level"]