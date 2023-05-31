import time
import threading
import math
import datetime
import multiprocessing
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
    return f"Thread {name} [{n_start, n_end}] completed in { datetime.timedelta(seconds=(end - start)) }"


if __name__ == "__main__":
    start = time.perf_counter()

    n_start = 1
    batch_size = int(MAX_INT / CONCURRENCY)
    args_list = []
    threads = []

    for i in range(CONCURRENCY - 1):
        args_list.append((i, n_start, n_start + batch_size))
        n_start += batch_size
    args_list.append((CONCURRENCY - 1, n_start, MAX_INT))

    print(args_list)


    with concurrent.futures.ProcessPoolExecutor() as pool_exec:
        # results = pool_exec.map(do_batch, args_list)
        results = pool_exec.map(do_batch, [args for args in args_list])
        # results = pool_exec.map(lambda args: do_batch(*args), args_list)

        for result in results:
            print(result)

    # process_pool = multiprocessing.Process(processes=4)

    # for args in args_list:
    #     process_pool.apply_async(do_batch, args=args)

    # process_pool.close()
    # process_pool.join()

    finish = time.perf_counter()

    print(f"Finished in {round(finish - start, 2)} seconds")