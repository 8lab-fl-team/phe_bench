import contextlib
import multiprocessing
import multiprocessing.dummy 
import os
import time
from typing import Callable, NoReturn, Optional

import gmpy2  # ensure gmpy2 available
from phe import paillier


@contextlib.contextmanager
def timeit(name=None,
           callback: Optional[Callable[[float], NoReturn]] = None,
           round=None):
    start_time = time.time()
    try:
        yield

    finally:
        elapsed = time.time() - start_time
        if callback:
            callback(elapsed)
        else:
            round_msg = ""
            if round:
                round_msg = f", average={elapsed / round}"
            print(f"{name} cost {elapsed} for {round} {round_msg}")


SMALL = 42
BIG = 1 << 256


def generate_key(n=2048):
    return paillier.generate_paillier_keypair(n_length=n)


def generate_data(size=1000, batch=1, value=SMALL):

    return [[value for _ in range(size // batch)] for _ in range(batch)]


def bench_single_process(key_size=2048, size=1000,value=SMALL):
    data = generate_data(size, 1,value)[0]
    pub, *_ = generate_key(key_size)
    with timeit(name=f"1 thread n={key_size} size={size}", round=size):
        for i in data:
            pub.encrypt(i)


def multiprocess_encryptor(args):
    data, pub = args
    for i in data:
        pub.encrypt(i)


def bench_multiprocesses(key_size=2048,
                         size=1000,
                         process_count=os.cpu_count() - 1 or 4,
                         value=SMALL,
                         ):
    assert size % process_count == 0, f"数据不能平均分成{process_count}等分"

    pub, *_ = generate_key(key_size)

    datasets = generate_data(size, process_count,value)
    pool = multiprocessing.Pool(process_count)
    with timeit(name=f"{process_count} Processes n={key_size} size={size} Encrypt", round=size):
        pool.map(multiprocess_encryptor, zip(datasets, [pub] * len(datasets)))
        pool.close()


def bench_multithreads(key_size=2048,
                         size=1000,
                         process_count=os.cpu_count() - 1 or 4,
                         value=SMALL,
                         ):
    assert size % process_count == 0, f"数据不能平均分成{process_count}等分"

    pub, *_ = generate_key(key_size)

    datasets = generate_data(size, process_count,value)
    pool = multiprocessing.dummy.Pool(process_count)
    with timeit(name=f"f{process_count} Thread n={key_size} size={size} Encrypt", round=size):
        pool.map(multiprocess_encryptor, zip(datasets, [pub] * len(datasets)))
        pool.close()


def main():
    process_count = os.cpu_count() - 1
    bacth_size = 100
    size = process_count * bacth_size
    print("single thread")
    bench_single_process(2048, size)

    print("multi process")
    bench_multiprocesses(2048, size, process_count)

    print("multi thread")
    bench_multithreads(2048, size, process_count)


if __name__ == "__main__":
    main()
