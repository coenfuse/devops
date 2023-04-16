# define about this module in 50 words
# ..


# standard imports
import argparse
import logging
import os
import sys
import threading

# internal imports
import lamina.metadata as meta

# module imports
from lamina.core.configurators.basic import Configurator
from lamina.core.streams.stream import Stream
from lamina.utils import stdlog
from lamina.utils.error import ERC

# thirdparty imports
# ..



# ==============================================================================
# TODO : docs
# ==============================================================================
class Lamina:

    # TODO : docs
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__config_file = None
        self.__config: Configurator = None 
        self.__stop_event = threading.Condition()
        self.__stream = Stream()

    # TODO : docs
    # --------------------------------------------------------------------------
    def start(self) -> ERC:
        status = self.__process_commandline_input()

        if status == ERC.SUCCESS:
            self.__config = Configurator()
            status = self.__config.parse(self.__config_file)

        if status == ERC.SUCCESS:
            status = self.__setup_logging()

        if status == ERC.SUCCESS:
            stdlog.info(f"starting {self.__config.get_app_config()['instance']} v{meta.VERS}")
            status = self.__stream.configure(self.__config)

        if status == ERC.SUCCESS:
            status = self.__stream.start()

        if status == ERC.SUCCESS:
            stdlog.info(f"running")
            
            with self.__stop_event:
                self.__stop_event.wait()

            stdlog.info(f"stopping")
            status = self.__stream.stop()

        stdlog.info(f"stopped")
        return status


    # TODO - docs
    # --------------------------------------------------------------------------
    def stop(self) -> None:
        with self.__stop_event:
            self.__stop_event.notify()


    # docs
    # --------------------------------------------------------------------------
    def __process_commandline_input(self) -> ERC:
        status = ERC.SUCCESS
        parser = argparse.ArgumentParser()

        parser.add_argument("--config", type=str,
            help='path to json file with application configurations')

        # argv[0] is the name of program and thus len(argv) is always 1
        # So, when argv[0] < 2, it means the passed cmdline input is incomplete
        if len(sys.argv) < 2:
            parser.print_help()
            status = ERC.FAILURE

        if status == ERC.SUCCESS:
            self.__config_file = parser.parse_args().config

        return status


    # NOTE : Keeping both styles of logging level assignment as the if-else
    # pattern is not scalable as the match one. If we were required to add a
    # level below DEBUG. It won't be possible with level * 10
    # --------------------------------------------------------------------------
    def __setup_logging(self) -> ERC:
        status = ERC.SUCCESS

        # setup basics and fetch config
        config = self.__config.get_app_config().get("log")
        log_fmt = logging.Formatter(
            datefmt = "%Y-%m-%d %H:%M:%S",
            fmt = "%(asctime)s.%(msecs)03d [%(levelname).1s] : LAMINA : %(message)s")
        
        # setup root logger and add custom level
        logging.addLevelName(5, "TRACE")
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.NOTSET)
         
        # setup console logger (if req.)
        if "stdout" in config:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(log_fmt)
            
            level = config["stdout"]["level"]
            if level in [0,1,2,3,4,5]:
                console_handler.setLevel(level * 10)        # log levels are in multiples of 10
            else:
                print(f"LAMINA : INVALID stdout.level = {level}. Defaulting to INFO")
                console_handler.setLevel(logging.INFO)

            root_logger.addHandler(console_handler)

        # setup file logger (if req.)
        if "fileout" in config:
            logdir = os.path.abspath(config["fileout"]["path"])
            loglvl = config["fileout"]["level"]

            if not os.path.exists(logdir):
                try: os.makedirs(logdir)
                except Exception as e:
                    print(f"LAMINA : log directory create failure at - {logdir} with error: {e}")
                    status = ERC.EXCEPTION

            file_handler = logging.FileHandler(f'{logdir}/{meta.NAME.lower()}.log')
            file_handler.setFormatter(log_fmt)
            match loglvl:
                case 0: file_handler.setLevel(5)    # TRACE
                case 1: file_handler.setLevel(logging.DEBUG)
                case 2: file_handler.setLevel(logging.INFO)
                case 3: file_handler.setLevel(logging.WARN)
                case 4: file_handler.setLevel(logging.ERROR)
                case 5: file_handler.setLevel(logging.CRITICAL)
                case _:
                    file_handler.setLevel(logging.DEBUG)
                    print(f"LAMINA : INVALID fileout.level = {loglvl}. Defaulting to DEBUG")

            root_logger.addHandler(file_handler)

        # else, no logging is done
        return status