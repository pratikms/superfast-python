import time
import math
import datetime
import concurrent.futures
import threading
from wait_group import WaitGroup

MAX_INT = 10000000
# MAX_INT = 1000000
# MAX_INT = 1000
CONCURRENCY = 10
total_prime_numbers = 0

def check_prime(num, mutex, wg):
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
    # wg.done()
    # print(f"Done. Wait count: {wg.wait_count}")

def do_batch(name, n_start, n_end, mutex, wg):
    start = time.time()
    for i in range(n_start, n_end):
        # wg.add(1)
        check_prime(i, mutex, wg)

    wg.done()
    print(f"Done. Wait count: {wg.wait_count}")
    end = time.time()
    print(f"Thread {name} [{n_start, n_end}] completed in { datetime.timedelta(seconds=(end - start)) }")

def main():
    
    start_time = time.time()
    wg = WaitGroup()

    n_start = 1
    batch_size = int(MAX_INT / CONCURRENCY)
    args_list = []
    threads = []
    mutex = threading.Lock()

    for i in range(CONCURRENCY - 1):
        args_list.append((i, n_start, n_start + batch_size, mutex, wg))
        n_start += batch_size
    args_list.append((CONCURRENCY - 1, n_start, MAX_INT, mutex, wg))


    for args in args_list:
        t = threading.Thread(target=do_batch, args=args)
        wg.add(1)
        print(f"Adding. wait_count: {wg.wait_count}")
        t.start()
        threads.append(t)

    # for thread in threads:
    #     thread.join()

    wg.wait()

    print(f"Finished in {datetime.timedelta(time.perf_counter())} seconds")


    print(f"Total prime numbers between 1 to {MAX_INT}: {total_prime_numbers}")

    end_time = time.time()
    print(f"Time taken: {datetime.timedelta(seconds=(end_time - start_time))}")


if __name__ == "__main__":
    main()
