import time
import threading
import math
import datetime
import multiprocessing
from multiprocessing import Process
import concurrent.futures

MAX_INT = 10000000
# MAX_INT = 1000000
CONCURRENCY = 10
total_prime_numbers = 0
mutex =threading.Lock()

def check_prime(num):
    global total_prime_numbers

    if num <= 1:
        return
    
    max_factors = math.floor(math.sqrt(num))
    for i in range(2, 1 + max_factors):
        if num % i == 0:
            return

    mutex.acquire()
    total_prime_numbers += 1
    mutex.release()
    end = time.time()

def do_batch(name, n_start, n_end):
    start = time.time()
    for i in range(n_start, n_end):
        check_prime(i)

    end = time.time()
    print(f"Thread {name} [{n_start, n_end}] completed in { datetime.timedelta(seconds=(end - start)) }")


if __name__ == "__main__":
    start = time.perf_counter()

    n_start = 1
    batch_size = int(MAX_INT / CONCURRENCY)
    args_list = []
    processes = []

    for i in range(CONCURRENCY - 1):
        args_list.append((i, n_start, n_start + batch_size))
        n_start += batch_size
    args_list.append((CONCURRENCY - 1, n_start, MAX_INT))

    args_list.reverse()
    # print(args_list)

    for args in args_list:
        # print(args)
        p = Process(target=do_batch, args=args)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print(f"Total prime numbers between 1 to {MAX_INT}: {total_prime_numbers}")

    finish = time.perf_counter()

    print(f"Finished in {round(finish - start, 2)} seconds")