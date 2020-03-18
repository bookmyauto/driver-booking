from __future__ import print_function
from time import sleep

def callback_a(i, result):
    print("Items processed: {}. Running result: {}.".format(i, result))

def square(i):
    return i * i

def processor(process, times, report_interval, callback):
    # Can also use callback.__name__ instead of callback.func_name in line above.
    result = 0
    print("Processing data ...")
    for i in range(1, times + 1):
        result += process(i)
        sleep(1)
        if i % report_interval == 0:
            callback(i, result)
d   = processor(square, 20, 5, callback_a)
print("end")
