import random
import time
import multiprocessing


def addition(numbers, results):
    while True:
        if numbers:
            number = numbers.pop(0)
            result = number + 10
            results.append(result)
            print(f"Addition Consumer: {number} + 10 = {result}")
        else:
            break


def subtraction(numbers, results):
    while True:
        if numbers:
            number = numbers.pop(0)
            result = number - 5
            results.append(result)
            print(f"Subtraction Consumer: {number} - 5 = {result}")
        else:
            break


def multiplication(numbers, results):
    while True:
        if numbers:
            number = numbers.pop(0)
            result = number * 2
            results.append(result)
            print(f"Multiplication Consumer: {number} * 2 = {result}")
        else:
            break


if __name__ == "__main__":
    manager = multiprocessing.Manager()
    numbers = manager.list(range(10))
    results = manager.list()

    addition_process = multiprocessing.Process(target=addition, args=(numbers, results))
    subtraction_process = multiprocessing.Process(target=subtraction, args=(numbers, results))
    multiplication_process = multiprocessing.Process(target=multiplication, args=(numbers, results))

    addition_process.start()
    subtraction_process.start()
    multiplication_process.start()

    addition_process.join()
    subtraction_process.join()
    multiplication_process.join()

    print("All items processed")
    print("Results:", results)
