from job_queue import *
from interfaces import Job
import random


CHANCE_OF_IO_REQUEST = 10
CHANCE_OF_IO_COMPLETE = 4


def read_jobs():
    with open('scheduling_data.txt') as file:
        # pid, arrival_time, burst_time, priority
        return list(map(int, file.read().replace(":", "").split()))


def io_request():
    return random.random() % CHANCE_OF_IO_REQUEST == 0


def io_complete():
    return random.random() % CHANCE_OF_IO_COMPLETE == 0


def run_coordinator():
    clock = 0
    random_seed = random.seed(None)
    job_list = read_jobs()
    queue = Queue()  # Comes from Queue class in job_queue.py

    # Places jobs (processes) in a queue
    for i in range(0, len(job_list), 4):
        job = Job()  # Comes from Job class in interfaces.py
        job.pid = job_list[i]
        job.arrival_time = job_list[i + 1]
        job.burst_time = job_list[i + 2]
        job.priority = job_list[i + 3]
        job.state = "ready"
        queue.enqueue(job)


if __name__ == '__main__':
    run_coordinator()
    # print("Hello world")

# Unfinished as of this commit
