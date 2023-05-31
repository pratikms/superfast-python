import time
import math
import datetime
import concurrent.futures
import threading

MAX_INT = 10000000
# MAX_INT = 1000000
CONCURRENCY = 10
total_prime_numbers = 0

def check_prime(num, mutex):
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
    # end = time.time()

def thread_check_prime(num):
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

def do_batch(name, n_start, n_end, mutex):
    start = time.time()
    for i in range(n_start, n_end):
        check_prime(i, mutex)

    end = time.time()
    print(f"Thread {name} [{n_start, n_end}] completed in { datetime.timedelta(seconds=(end - start)) }")

if __name__ == "__main__":

    start_time = time.time()

    n_start = 1
    batch_size = int(MAX_INT / CONCURRENCY)
    args_list = []
    threads = []
    mutex = threading.Lock()

    for i in range(CONCURRENCY - 1):
        args_list.append((i, n_start, n_start + batch_size, mutex))
        n_start += batch_size
    args_list.append((CONCURRENCY - 1, n_start, MAX_INT, mutex))


    for args in args_list:
        t = threading.Thread(target=do_batch, args=args)
        t.start()
        threads.append(t)

    for thread in threads:
        thread.join()

    print(f"Finished in {datetime.timedelta(time.perf_counter())} seconds")


    # print(args_list)

    # with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENCY) as executor:

    #     # args_list = [(i, n_start, n_start + batch_size) or n_start += batch_size for i in range(CONCURRENCY - 1)]
    #     # for i in range(CONCURRENCY - 1):
    #     #     args_list.append((i, n_start, n_start + batch_size))
    #     #     n_start += batch_size
    #     # args_list.append((CONCURRENCY - 1, n_start, MAX_INT))

        

    #     tasks = [executor.submit(do_batch, *args) for args in args_list]
    #     # tasks = [executor.submit(check_prime(i)) for i in range(1, MAX_INT)]
    #     while tasks:
    #         completed, pending = concurrent.futures.wait(
    #             tasks, return_when=concurrent.futures.FIRST_COMPLETED
    #         )

    #         for futures in completed:
    #             result = futures.result()

    #         tasks = pending




    #     # tasks = [executor.submit(do_batch, *args) for args in args_list]

    #     # for future in concurrent.futures.as_completed(tasks):
    #     #     result = future.result()





    #     # results = [executor.submit(do_batch, *args) for args in args_list]


    #     # results = executor.map(lambda args: do_batch(*args), args_list)

    #     # for result in results:
    #     #     pass
    #     #     # print(result)




    #     # for i in range(CONCURRENCY - 1):
    #     #     # do_batch(i, n_start, n_start + batch_size)
    #     #     executor.map(do_batch, i, n_start, n_start + batch_size)
    #     #     n_start += batch_size

    #     # # do_batch(CONCURRENCY - 1, n_start, MAX_INT)
    #     # executor.map(do_batch, CONCURRENCY - 1, n_start, MAX_INT)

    #     # executor.map(do_batch, '9', '9000001', '10000000')
    #     # executor.map(do_batch, name=9, n_start=9000001, n_end=10000000)
    #     # executor.map(do_batch, zip(name=9, n_start=9000001, n_end=10000000))

    # # for num in range(1, MAX_INT):
    # #     check_prime(num)




    print(f"Total prime numbers between 1 to {MAX_INT}: {total_prime_numbers}")

    end_time = time.time()
    print(f"Time taken: {datetime.timedelta(seconds=(end_time - start_time))}")