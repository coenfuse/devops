# description in 50 words
# ..



# standard imports
from queue import Queue
from threading import Lock

# internal imports
# ..

# module imports
# ..

# third-party imports
# ..



class MemBuff:
    def __init__(self):
        self.__dblck = Lock()
        self.__state = {}

    def make_buffer(self, name: str, size: int = 0):
        with self.__dblck:
            self.__state[name] = Queue(maxsize = size)

    def push(self, buffer: str, value: any):
        if buffer in self.__state:
            Queue(self.__state[buffer]).put(
                item = value, block = True, timeout = None)

    def pop(self, buffer: str):
        if buffer in self.__state:
            Queue(self.__state[buffer]).get(block = True, timeout = None)

    