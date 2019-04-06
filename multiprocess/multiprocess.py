from multiprocessing import Queue, Process
import os
import psutil
import threading
import time


def function(number, indicator):
    new_number = number ** indicator
    return "Done"


class Pool():
    def __init__(self, min_workers=2, max_workers=10, max_memory=512):
        self.min_workers = min_workers
        self.max_workers = max_workers
        self.max_memory = max_memory
        self.max_process_memory = 0
        self.input_q = Queue()
        self.output_q = Queue()
        self.workers = []
        self.workers_count = 0
        self.working_status = True

    def get_proc_memory(self):
        while self.working_status:
            for worker in self.workers:
                try:
                    process = psutil.Process(worker.pid)
                    memory_usage = process.memory_info().rss / 2 ** 20
                    self.max_process_memory = max(memory_usage, self.max_process_memory)
                    print("Process " + str(worker.pid) + " uses " + str(memory_usage) + "Mb")
                except Exception:
                    pass
            print("")
            time.sleep(0.5)

    def map(self, func, arguments):
        for arg in arguments:
            self.input_q.put(arg)

        self.start_first_worker(func)

        for i in range(self.workers_count):
            self.init_worker(func)

        for worker in self.workers:
            worker.join()
        self.working_status = False
        return [self.output_q.get() for _ in range(self.output_q.qsize())]

    def check_workers_count(self, proc_count):
        if proc_count < self.min_workers:
            raise Exception("Memory is not enough for " + str(self.min_workers) + " workers")
        else:
            return min(proc_count, self.max_workers)

    def start_first_worker(self, func):
        first_worker = Process(target=self.first_worker_func, args=(func, ))
        self.workers.append(first_worker)
        get_proc_max_memory = threading.Thread(target=self.get_proc_memory, args=())
        first_worker.start()

        get_proc_max_memory.start()
        first_worker.join()
        self.workers.clear()

        try:
            count = self.max_memory // self.max_process_memory
        except ZeroDivisionError:
            count = self.max_workers
        self.workers_count = self.check_workers_count(count)

        print("Testing first worker finished")
        print("Process memory = " + str(self.max_process_memory))
        print("Workers count = " + str(self.workers_count) + "\r\r\n")

    def init_worker(self, func):
        new_worker = Process(target=self.worker_func, args=(func, ))
        self.workers.append(new_worker)
        new_worker.start()

    def first_worker_func(self, func):
        attr = self.input_q.get()
        self.output_q.put(str(func(attr[0], attr[1])) + " by worker " + str(os.getpid()))

    def worker_func(self, func):
        while self.input_q.qsize() > 0:
            attr = self.input_q.get()
            self.output_q.put(str(func(attr[0], attr[1])) + " by worker " + str(os.getpid()))


if __name__ == "__main__":
    start_time = time.time()
    pool = Pool()
    array = [(1000, 1000000) for _ in range(10)]
    results = pool.map(function, array)
    print("Results:", results)
    print("Spent time:", time.time() - start_time)
    start_time = time.time()
    new_array = [function(args[0], args[1]) for args in array]
    print("Spent time:", time.time() - start_time)
