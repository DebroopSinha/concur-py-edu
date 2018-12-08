import threading
from queue import Queue
import time
"""
This is a classic producer-consumer problem , where the consumer computes fibonacci numbers
The Queue class in this module implements all the required locking semantics
It is especially useful in threaded programming when information must be exchanged safely between multiple threads

40
Starting queue_task...
Notifying fibonacci task threads that the queue is ready to consume...
Tasks completed, time taken :  11.084780901

Performance is better than serial and thread_pool_executor versions but lags behind the multiprocessing.Pool module
"""

fibo_dict = {}
shared_queue = Queue()
n = int(input())
input_list = [n+i for i in range(10000)]
queue_condition = threading.Condition()


def fibonacci_task(condition):
    with condition:

        while shared_queue.empty():
            #print("[{}] - waiting for elements in queue..".format(threading.current_thread().name))
            condition.wait()

        else:
            value = shared_queue.get()
            a, b = 0, 1
            for item in range(value):
                a, b = b, a + b
                fibo_dict[value] = a

        shared_queue.task_done()
        """print("[{}] fibonacci of key [{}] with result [{}]".
              format(threading.current_thread().name, value, fibo_dict[value]))"""


def queue_task(condition):
    print('Starting queue_task...')
    with condition:
        for item in input_list:
            shared_queue.put(item)

        print("Notifying fibonacci task threads that the queue is ready to consume...")
        condition.notifyAll()


start = time.perf_counter()
threads = []
for i in range(len(input_list)):
    thread = threading.Thread(target=fibonacci_task, args=(queue_condition,))
    thread.daemon = True
    threads.append(thread)

[thread.start() for thread in threads]

prod = threading.Thread(name='queue_task_thread', target=queue_task, args=(queue_condition,))
prod.daemon = True
prod.start()

[thread.join() for thread in threads]

#print("Result {}".format(fibo_dict[5039]))
end = time.perf_counter()
print('Tasks completed, time taken : ', end-start)
