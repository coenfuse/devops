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
from lamina.core.configurators.basic import Configurator
from lamina.core.streams.stream import Stream
from lamina.core.utils import stdlog
from lamina.core.utils.error import ERC

# thirdparty imports
# ..



# ==============================================================================
# TODO : docs
# ==============================================================================
class Lamina:

    # TODO : docs
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__CNAME = "LAMINA  "
        self.__config_file = None
        self.__config: Configurator = None 
        self.__stream = Stream()
        self.__is_requested_stop = False

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
            stdlog.info(f"{self.__CNAME} : starting {self.__config.get_app_config()['instance']} v{meta.VERS}")
            status = self.__stream.configure(self.__config)

        if status == ERC.SUCCESS:
            status = self.__stream.start()

        if status == ERC.SUCCESS:
            self.__is_requested_stop = False
            stdlog.info(f"{self.__CNAME} : running")

            while not self.__is_requested_stop: sleep(2)        # blocking

            stdlog.info(f"{self.__CNAME} : stopping")
            # status = self.stop()

        stdlog.info(f"{self.__CNAME} : stopped")
        return status

    # TODO - docs
    # --------------------------------------------------------------------------
    def stop(self) -> ERC:
        self.__is_requested_stop = True
        return self.__stream.stop()

    # TODO - docs
    # --------------------------------------------------------------------------
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
            self.__config_file = parser.parse_args().config

        return status


    # TODO : docs, add a way to have different logging controllers for stdlog
    # and filelog
    # --------------------------------------------------------------------------

    def __setup_logging(self) -> ERC:
        status = ERC.SUCCESS

        stdlog_config = self.__config.get_app_config()["log"]["std"]
        filelog_config= self.__config.get_app_config()["log"]["file"]
        
        log_handles = []
        log_format  = '%(asctime)s.%(msecs)03d [%(levelname).1s] : %(message)s'
        log_datefmt = '%Y-%m-%d %H:%M:%S'
        
        if stdlog_config["enabled"]:
            log_handles.append(logging.StreamHandler(sys.stdout))

        if filelog_config["enabled"]:
            logdir = os.path.abspath(filelog_config["path"])

            if not os.path.exists(logdir):
                try: os.makedirs(logdir)
                except Exception as e:
                    print(f"{self.__CNAME} : log directory create failure at - {logdir} with error: {e}")
                    status = ERC.EXCEPTION

            log_handles.append(logging.FileHandler(f'{logdir}/{meta.NAME.lower()}.log'))

        logging.addLevelName(5, "TRACE")
        logging.basicConfig(
            format   = log_format,
            datefmt  = log_datefmt,
            handlers = log_handles)

        match stdlog_config["level"]:
            case 0: logging.getLogger().setLevel(5)    # TRACE
            case 1: logging.getLogger().setLevel(logging.DEBUG)
            case 2: logging.getLogger().setLevel(logging.INFO)
            case 3: logging.getLogger().setLevel(logging.WARN)
            case 4: logging.getLogger().setLevel(logging.ERROR)
            case 5: logging.getLogger().setLevel(logging.FATAL)
            case _: 
                print(f"{self.__CNAME} : INVALID log level = {stdlog_config['level']}. Defaulting to INFO")
                logging.getLogger().setLevel(logging.INFO)
                status = ERC.WARNING

        return status