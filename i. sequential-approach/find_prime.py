import time
import math
import datetime

MAX_INT = 10000000
# MAX_INT = 1000000
# MAX_INT = 1000001
total_prime_numbers = 0

def check_prime(num):
    global total_prime_numbers

    # print(f"NUM: {num}")
    if num <= 1:
        return
    
    max_factors = math.floor(math.sqrt(num))
    # print(f"MF: {max_factors}")
    for i in range(2, 1 + max_factors):
        if num % i == 0:
            return


    # if num & 1 == 0:
    #     return
    
    # for i in range(3, int(math.sqrt(num)) + 1):
    #     if num % i == 0:
    #         return
        
    total_prime_numbers += 1


if __name__ == "__main__":

    start_time = time.time()
    for num in range(1, MAX_INT):
        check_prime(num)

    print(f"Total prime numbers between 1 to {MAX_INT}: {total_prime_numbers}")

    end_time = time.time()
    print(f"Time taken: {datetime.timedelta(seconds=(end_time - start_time))}")