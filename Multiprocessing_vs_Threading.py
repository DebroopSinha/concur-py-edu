#import threading
import time
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from multiprocessing import Pool, cpu_count

"""
Python has a Global Interpreter Lock(GIL) which restricts the interpreter to only one thread 
multiprocessing.pool on the other hand bypasses the GIL and creates separate independent processes with their own GIL's
Below is a CPU intensive task . So, threading does not bring performance boost as threads are blocked by the GIL
In I/O intensive tasks however , threading will yield performance boost and multiprocessing module will have overheads

Time is calculated by time.process_time() as it gives the total actual CPU time . (user time+system time)
time.perf_counter() can be used for a thread intensive program. 
Results(in seconds) for calling 'fib' 10000 times with the argument size growing linearly to 10000:

CPU Cores :  8
fib_serial :  17.390625
thread_pool_executor :  14.28125
Process_Pool_executor :  6.453125
multiprocessing_pool :  0.03125

"""


def fib(n):
    arr = [0]*(n+1)
    arr[0] = 0
    arr[1] = 1
    for m in range(2, n):
        arr[m] = arr[m-1]+arr[m-2]
    #print("executed by {}".format(threading.current_thread()))
    return arr[n-1]


if __name__ == "__main__":
    n = int(input())
    ns = [n+i for i in range(10000)]
    print("CPU Cores : ", cpu_count())
    start = time.process_time()
    for i in range(len(ns)):
        x = fib(ns[i])
    end = time.process_time()
    print('fib_serial : ', end-start)

    start = time.process_time()
    with ThreadPoolExecutor(max_workers=10) as t_pool:
        y = t_pool.map(fib, ns)
    end = time.process_time()
    print('thread_pool_executor : ', end-start)

    start = time.process_time()
    with ProcessPoolExecutor(max_workers=10) as p_pool:
        for n, p in zip(ns, p_pool.map(fib, ns)):
            #print('%d fibonacci is : %s' % (n, p))
            pass
    end = time.process_time()
    print("Process_Pool_executor : ", end-start)

    start = time.process_time()
    with Pool(10) as m_pool:
        y = m_pool.map(fib, ns)
    end = time.process_time()
    print('multiprocessing.pool : ', end - start)


