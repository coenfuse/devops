# description about this module in 50 words ...

# standard imports
from random import uniform
from threading import Thread
from time import sleep
from typing import Callable, Union

# internal imports
from lamina.plugins.inputs.http.config import Configuration
from lamina.plugins.inputs.http.logger import HTTPLog

# module imports
from lamina.core.buffers.membuff import MQItem
from lamina.utils.error import ERC

# thirdparty import
import requests as http



# ==============================================================================
# Loren ipsum color dotor signet
# ==============================================================================
class HTTPInputPlugin:
    
    # docs
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__poller: Thread = Thread()
        self.__is_polling: bool = False
        self.log = HTTPLog()
        
        # DIRTY PATCH (Turning off 'urllib3' and 'requests' logger)
        import logging
        logging.getLogger('urllib3').setLevel(logging.CRITICAL)
        logging.getLogger('requets').setLevel(logging.CRITICAL)


    # docs
    # --------------------------------------------------------------------------
    def configure(self, name: str, config: dict, data_handler: Callable[[MQItem], None]) -> ERC:
        self.__config = Configuration(config, name)        # may raise exception

        self.__data_handler = data_handler
        self.__poller = Thread(
            target = self.__poll_data, 
            name = f"http.{self.__config.get_client_id()}.poller")
        
        if self.__config.is_logging_enabled():
            self.log.configure(
                self.__config.get_client_id(),
                self.__config.logging_level())

        return ERC.SUCCESS
    
    # docs
    # --------------------------------------------------------------------------
    def start(self) -> ERC:
        self.log.info("running")
        self.__poller.start()
        return ERC.SUCCESS if self.__poller.is_alive() else ERC.FAILURE

    # docs
    # --------------------------------------------------------------------------
    def stop(self) -> ERC:
        self.__is_polling = False
        self.log.info("stopping")
        self.__poller.join()
        return ERC.SUCCESS

    # docs
    # --------------------------------------------------------------------------
    def is_running(self):
        return self.__is_polling
    
    # docs
    # --------------------------------------------------------------------------
    def __poll_data(self):

        # utility vars (use nonlocal to modify these in nested functions)
        config = self.__config
        poll_fail_count = 0
        prev_data = ""

        # utility functions
        def make_request() -> Union[http.Response, None]:
            try:
                response: http.Response = http.request(
                    url = config.url(), 
                    data = config.data(), 
                    method = config.method(), 
                    params = config.params(), 
                    headers = config.headers(), 
                    timeout = config.timeout_s())
                return response.status_code, response

            except Exception as e:
                self.log.error(f"error '{e}' while making HTTP request")
                nonlocal poll_fail_count
                poll_fail_count = poll_fail_count + 1
                return None, None
        
        def process_failed_status(res: http.Response):
            self.log.warn(f"request failed with HTTP code {status} {res.reason}")
            nonlocal poll_fail_count
            poll_fail_count = poll_fail_count + 1

        def get_content(res: http.Response) -> Union[str, None]:
            nonlocal prev_data
            new_data = decode_content(res)
            if config.allow_duplicates() or prev_data != new_data:
                if  (
                        config.max_content_length() == 0
                        or
                        len(new_data) <= config.max_content_length()
                    ):
                    prev_data = new_data
                    return new_data
                else:
                    self.log.warn(f"response dumped! content length = {len(new_data)} exceeds specified limit of {config.max_content_size()}")
                    return None

        def decode_content(res: http.Response) -> str:
            if config.content_decoder() == "auto": return res.text
            elif config.content_decoder() == "raw": return res.content
            else: return res.content.decode(config.content_decoder())
        
        def get_sleep_time() -> int:
            return config.poll_rate_s() + uniform(
                -1 * config.poll_variance_s(), config.poll_variance_s())
        
        # we do not require to use nonlocal to access self.<variable> since instance
        # variables can be accessed / modified inside nested functions just fine
        def can_poll() -> bool:
            if self.__is_polling:
                if poll_fail_count > config.max_poll_attempts():
                    self.log.warn(f"polling stopped! Fail count exceeded specified threshold of = {config.max_poll_attempts()}")
                    self.__is_polling = False
            return self.__is_polling

        # Actual poller. We kickstart the poller for first iteration by setting
        # is_polling flag as true
        self.__is_polling = True
        while can_poll():
            status, response = make_request()
            if status in config.success_codes():
                content = get_content(response)
                if content is not None:
                    self.__data_handler(MQItem(content, config.tag()))
                    poll_fail_count = 0
            elif response is not None:
                process_failed_status(response)

            # we sleep irrespective of request status because we do not want
            # numb the server with inifinte requests if we fail
            sleep(get_sleep_time())