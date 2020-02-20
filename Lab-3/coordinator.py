from job_queue import *
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


if __name__ == '__main__':
    # run_coordinator()
    print("Hello world")

# Unfinished as of this commit
