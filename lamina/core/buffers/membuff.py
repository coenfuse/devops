# description in 50 words
# ..



# standard imports
from copy import deepcopy
from queue import Queue
from threading import Lock
from typing import Dict
import time

# internal imports
# ..

# module imports
# ..

# third-party imports
# ..



# TODO : MemQueueManage (handles all blocking initialization, enforces MQItem creation
# etc)
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
class MemQueue:

    # TODO : Create a queue as a default init, this removes the user from having
    # to create a new named queue manually. The default queue will be used for
    # basic usage.

    # initializes the MemQueue instance, here we create a empty dict instance
    # that will contain an index of unique queues. Here I also initialize a lock
    # that will be used only when we are altering the index itself (not its 
    # contents)
    # --------------------------------------------------------------------------
    def __init__(self):
        self.__db: Dict[str, Queue] = {}
        self.__db_lock = Lock()


    # add a new unique queue to the index if it doesn't exist. Specify max-size
    # of queue (optional) 
    # --------------------------------------------------------------------------
    def add_queue(self, qname: str, size: int = 0) -> None:
        if qname not in self.__db:
            with self.__db_lock:
                self.__db[qname] = Queue(maxsize = size)


    # remove a queue from the index if it exists
    # --------------------------------------------------------------------------
    def del_queue(self, qname: str) -> None:
        if qname in self.__db:
            with self.__db_lock:
                del self.__db[qname]


    # push / add new value to a end of queue in the index (if queue exist), else 
    # KeyError exception is thrown. Block the push requesting thread indefinitely
    # if the queue is full, or wait utill timeout. Once the push is successful
    # we notify all the waiters that may be waiting on the queue using peek() by
    # aquiring lock on not_empty cv of Queue class.
    # --------------------------------------------------------------------------
    def push(self, qname: str, value: any, block_thread: bool = True, timeout_s: float = None) -> None:
        self.__db[qname].put(value, block_thread, timeout_s)
        
        with self.__db[qname].not_empty:
            self.__db[qname].not_empty.notify()


    # pop / renmove a value from the front of the queue (if queue exist), else
    # a KeyError is thrown. Block / wait to get an element from queue indefinitely
    # or until timeout or until item arrives, whichever faster
    # --------------------------------------------------------------------------
    def pop(self, qname: str, block_thread: bool = True, timeout_s: float = None) -> any:
        return self.__db[qname].get(block_thread, timeout_s)
    

    # Gives you a copy of the item at the front of the queue. 
    # If the queue is empty and call is non-blocking the IndexError is thrown
    # If the queue is empty and call is blocking with timeout_s = None, thread is
    # blocked until the queue is non-empty. If timeout_s is not None, then IndexError
    # after timeout has passed. If the queue doesn't exist, KeyError is raised.
    # --------------------------------------------------------------------------
    def peek(self, qname: str, block_thread: bool = True, timeout_s: float = None):
        return self.peek_at(qname, 0, block_thread, timeout_s)
        

    # Gives you a copy of the item at a specific index in a queue.
    # - If queue is empty, unblocked then IndexError is thrown
    # - If queue is empty, blocked & timeout_s = None, thread is blocked until the queue is non-empty. 
    # - If queue is empty, blocked & timeout_s != None, then IndexError after timeout
    # - If queue is not_empty, blocked, then value is returned
    # - If the queue doesn't exist, KeyError is raised
    # --------------------------------------------------------------------------
    def peek_at(self, qname: str, index: int, block_thread: bool = True, timeout_s: float = None):
        if not block_thread:
            return deepcopy(self.__db[qname].queue[index])
        
        # only wait if the queue is empty, else the program may block indefinitely
        elif len(self.__db[qname].queue) == 0:
            with self.__db[qname].not_empty:
                self.__db[qname].not_empty.wait(timeout_s)            # blocking
        
        # the flow eventually reach here once the thread resumes execution, 
        # whether or not it was blocked.
        return deepcopy(self.__db[qname].queue[index])
    


# docs
# ------------------------------------------------------------------------------
class MQItem:

    # initializes a new MQItem with value of any type and optional tag
    # --------------------------------------------------------------------------
    def __init__(self, val: any, tag: str = ""):
        self.__init_time: float = time.time()
        self.__tag: str = tag
        self.__val: any = val

    # returns creation time for this MQItem instance in float since epoch
    # --------------------------------------------------------------------------
    def get_time(self) -> float:
        return self.__init_time
    
    # returns string formatted creation time for this MQItem in GMT
    # --------------------------------------------------------------------------
    def get_ftime(self, time_fmt: str) -> str:
        return time.strftime(time_fmt, time.gmtime(self.__init_time))

    # returns the tag attached to this MQItem instance (if any)
    # -------------------------------------------------------------------------- 
    def get_tag(self) -> str:
        return self.__tag
    
    # assign a tag to this MQItem instance
    # --------------------------------------------------------------------------
    def set_tag(self, tag: str) -> None:
        self.__tag = tag

    # get the value stored in this MQItem instance
    # --------------------------------------------------------------------------
    def get_value(self) -> any:
        return self.__val
    
    # update the held value in this MQItem instance
    # --------------------------------------------------------------------------
    def set_value(self, value: any) -> None:
        self.__val = value