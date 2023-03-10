# THIS MESS IS WIP
# ..


# standard imports
from threading import Event, Thread, Lock
from time import sleep

# internal imports
# ..

# module imports
from lamina.core.utils.error import ERC

# thirdparty imports
# ..



# ==============================================================================
# TODO : docs
# ==============================================================================
class Base_Input_Service:

    # docs
    # --------------------------------------------------------------------------
    def __init__(self, service_name: str):
        self.__CNAME = f"INPUT   : [{service_name}] "
        self.__driver = None


    # docs
    # --------------------------------------------------------------------------
    def configure(self, driver) -> ERC:
        self.__driver = driver


    # TODO : docs
    # --------------------------------------------------------------------------
    def start(self) -> ERC:
        self.__driver.activate()


    # TODO : docs
    # --------------------------------------------------------------------------
    def stop(self) -> ERC:
        self.__driver.deactivate()


    # TODO : docs
    # --------------------------------------------------------------------------
    def is_running(self) -> bool:
        return self.__driver.is_active()



# ==============================================================================
# TODO : docs
# ==============================================================================
class Active_Input_Service(Base_Input_Service):
    
    # TODO : docs
    # --------------------------------------------------------------------------
    def __init__(self, service_name: str):
        super.__init__(service_name)

        self.__runtime: Thread = Thread(target = self.__runtime)
        self.__is_requested_stop: bool = True
        self.__cycle_time: int = 0


    def start(self) -> ERC:
        self.__is_requested_stop = False
        self.__runtime.start()
        return ERC.SUCCESS if self.__runtime.is_alive() else ERC.FAILURE

    def stop(self, force = False) -> ERC:
        self.__is_requested_stop = True
        self.__runtime.join(timeout = 1 if force == True else None)             # Thread will block if not forced
        return ERC.WARNING if self.__runtime.is_alive() else ERC.SUCCESS        # If thread is still alive, it means timeout has occured, and thread now might be orphan

    def is_running(self) -> bool:
        pass

    def job(self):
        pass

    def __runtime(self) -> None:
        while not self.__is_requested_stop:
            self.job()
            sleep(self.__cycle_time)




class Passive_Input_Service(Base_Input_Service):
    def __init__(self):
        pass

    def configure(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def is_active(self):
        pass

    def __event_handler(self):
        pass




class Base_Pipe_Service(Base_Input_Service):
    def __init__(self):
        pass