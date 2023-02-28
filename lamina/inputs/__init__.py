# description of this module in 50 words
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



class Base_Input_Agent:
    pass



class Base_Polling_Agent(Base_Input_Agent):
    def __init__(self):
        self.__runtime: Thread = Thread(target = self.__runtime)
        self.__is_requested_stop: bool = True
        self.__cycle_time: int = 0

    def configure(self) -> ERC:
        pass

    def start(self) -> ERC:
        self.__is_requested_stop = False
        self.__runtime.start()
        return ERC.SUCCESS if self.__runtime.is_alive() else ERC.FAILURE

    def stop(self, force = False) -> ERC:
        self.__is_requested_stop = True
        self.__runtime.join(timeout = 1 if force == True else None)             # Thread will block if not forced
        return ERC.WARNING if self.__runtime.is_alive() else ERC.SUCCESS        # If thread is still alive, it means timeout has occured, and thread now might be orphan

    # def pause(self):
    #     pass

    # def resume(self):
    #     pass

    def is_running(self) -> bool:
        pass

    def job(self):
        pass

    def __runtime(self) -> None:
        while not self.__is_requested_stop:
            self.job()
            sleep(self.__cycle_time)




class Base_Waiting_Agent(Base_Input_Agent):
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




class Base_Pipe_Agent(Base_Input_Agent):
    def __init__(self):
        pass