# description of this module in 50 words
# ..


# standard imports
from threading import Event, Thread, Lock
from time import sleep

# internal imports
# ..

# module imports
# ..

# thirdparty imports
# ..



class Base_Polling_Agent:
    def __init__(self):
        self.__runtime = Thread(target = self.__runtime)
        self.__is_requested_stop = True
        self.__cycle_time = 0

    def configure(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def pause(self):
        pass

    def resume(self):
        pass

    def is_running(self):
        pass

    def job(self):
        pass

    def __runtime(self):
        while not self.__is_requested_stop:
            self.job()
            sleep(self.__cycle_time)