import queue
import threading
import copy

shared_queue = queue.Queue()
result_queue = queue.Queue()

for i in range(10):
    shared_queue.put(i)

def add_consumer():
    while True:
        try:
            item = shared_queue.get(block=False)
            item_copy = copy.deepcopy(item)
            result = item_copy + 10
            result_queue.put(result)
            shared_queue.task_done()
            print("Addition Consumer: {} + 10 = {}".format(item, result))
        except queue.Empty:
            break

def multiply_consumer():
    while True:
        try:
            item = shared_queue.get(block=False)
            item_copy = copy.deepcopy(item)
            result = item_copy * 10
            result_queue.put(result)
            shared_queue.task_done()
            print("Multiplication Consumer: {} * 10 = {}".format(item, result))
        except queue.Empty:
            break

def subtract_consumer():
    while True:
        try:
            item = shared_queue.get(block=False)
            item_copy = copy.deepcopy(item)
            result = item_copy - 5
            result_queue.put(result)
            shared_queue.task_done()
            print("Subtraction Consumer: {} - 5 = {}".format(item, result))
        except queue.Empty:
            break

add_thread = threading.Thread(target=add_consumer)
multiply_thread = threading.Thread(target=multiply_consumer)
subtract_thread = threading.Thread(target=subtract_consumer)

add_thread.start()
multiply_thread.start()
subtract_thread.start()

add_thread.join()
multiply_thread.join()
subtract_thread.join()

shared_queue.join()

print("All items processed")