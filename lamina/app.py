# define about this module in 50 words
# ..


# standard imports
import argparse
import logging
import os
import sys
from time import sleep

# internal imports
import lamina.metadata as meta

# module imports
from lamina.core.streams.stream import Stream
from lamina.core.utils import stdlog
from lamina.core.utils.error import ERC

# thirdparty imports
# ..


class Configurator:
    def __init__(self):
        pass

    def parse(self, config) -> ERC:
        return ERC.SUCCESS

    def get_logdir(self) -> str:
        return "out/log"

    def get_log_level(self) -> int:
        return 0

    def get_input_mqtt(self) -> dict:
        return {
            "client_id" : "lamina_recv",
            "is_clean_session" : True,
            "host" : "localhost",
            "port" : 1883,
            "keep_alive_s" : 60,
            "username" : "coenfuse",
            "password" : "noobmaster69",
            "subscriptions" : [
                {
                    "topic" : "lamina/recv",
                    "mid" : 12,
                    "qos" : 0
                }
            ]
        }

    def get_output_mqtt(self) -> dict:
        return {
            "client_id" : "lamina_send",
            "is_clean_session" : True,
            "host" : "localhost",
            "port" : 1883,
            "keep_alive_s" : 60,
            "username" : "coenfuse",
            "password" : "noobmaster69",
            "publish_to" : "lamina/send",
            "publish_rate_s" : 4,
            "reconnect_on_fail" : True,
            "reconnect_threshold" : 10
        }


# ------------------------------------------------------------------------------
class Lamina:

    def __init__(self):
        self.__NAME = "LAMINA  "
        self.__cfgfile = None
        self.__stdout = False
        self.__config = Configurator()
        self.__stream = Stream()
        self.__is_requested_stop = False

    def start(self) -> ERC:
        status = self.__process_commandline_input()

        if status == ERC.SUCCESS:
            status = self.__config.parse(self.__cfgfile)

        if status == ERC.SUCCESS:
            status = self.__setup_logging()

        if status == ERC.SUCCESS:
            stdlog.info(f"{self.__NAME} : starting {meta.NAME} {meta.VERS}")
            status = self.__stream.configure(self.__config)

        if status == ERC.SUCCESS:
            status = self.__stream.start()

        if status == ERC.SUCCESS:
            self.__is_requested_stop = False
            stdlog.info(f"{self.__NAME} : running")

            while not self.__is_requested_stop: sleep(2)        # blocking

            stdlog.info(f"{self.__NAME} : stopping")
            # status = self.stop()

        stdlog.info(f"{self.__NAME} : stopped")
        return status


    def stop(self) -> ERC:
        self.__is_requested_stop = True
        return self.__stream.stop()


    def is_running(self) -> bool:
        return self.__stream.is_running()


    # docs
    # --------------------------------------------------------------------------
    def __process_commandline_input(self) -> ERC:
        status = ERC.SUCCESS
        parser = argparse.ArgumentParser()

        parser.add_argument("--config", type=str,
                            help='path to json file with application configurations')
        parser.add_argument("--stdout", action='store_true',
                            help="whether to diplay logs on standard output")

        # argv[0] is the name of program and thus len(argv) is always 1
        # So, when argv[0] < 2, it means the passed cmdline input is incomplete
        if len(sys.argv) < 2:
            parser.print_help()
            status = ERC.FAILURE

        if status == ERC.SUCCESS:
            self.__cfgfile = parser.parse_args().config
            self.__stdout = parser.parse_args().stdout

        return status


    # docs
    # --------------------------------------------------------------------------

    def __setup_logging(self) -> ERC:
        status = ERC.SUCCESS
        logdir = os.path.abspath(self.__config.get_logdir())

        if not os.path.exists(logdir):
            try:
                os.makedirs(logdir)
            except Exception as e:
                print(f"log directory create FAILURE at: {logdir} with error: {e}")
                status = ERC.EXCEPTION

        if status is ERC.SUCCESS:
            log_handles = [logging.FileHandler(f'{logdir}/{meta.NAME.lower()}.log')]
            log_format = '%(asctime)s.%(msecs)03d [%(levelname).1s] : %(message)s'
            log_datefmt = '%Y-%m-%d %H:%M:%S'

            if self.__stdout:
                log_handles.append(logging.StreamHandler(sys.stdout))

            logging.basicConfig(
                format=log_format,
                datefmt=log_datefmt,
                handlers=log_handles)

            log_level = self.__config.get_log_level()
            if log_level in [0,1,2,3,4,5]:
                logging.getLogger().setLevel(log_level * 10)                    # because logging levels are in multiples of 10
            else:
                raise ValueError(f"log_level = {log_level} OUT OF BOUNDS!")

            return status

            '''
            # This is only Python 3.10+ compatible

            match self.__config.get_log_level():
                case 0: logging.getLogger().setLevel(5)    # TRACE
                case 1: logging.getLogger().setLevel(logging.DEBUG)
                case 2: logging.getLogger().setLevel(logging.INFO)
                case 3: logging.getLogger().setLevel(logging.WARN)
                case 4: logging.getLogger().setLevel(logging.ERROR)
                case 5: logging.getLogger().setLevel(logging.FATAL)
                case _: 
                    raise ValueError(f"log_level = {self.__config.get_log_level()} OUT OF BOUNDS!")
            '''
                    