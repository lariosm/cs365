from job_queue import Queue
from interfaces import Job
from schedulers import NonAgressivePreemptiveScheduler
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
    queue = Queue()

    for i in range(0, len(job_list), 4):
        job = Job()
        job.pid = job_list[i]
        job.arrival_time = job_list[i + 1]
        job.burst_time = job_list[i + 2]
        job.priority = job_list[i + 3]
        job.state = "ready"
        queue.enqueue(job)
    print("STATUS: Jobs read in.... OK")

    scheduler = NonAgressivePreemptiveScheduler(queue)
    print("STATUS: Jobs processed into scheduler.... OK")

    while scheduler.has_jobs():
        current_job = scheduler.schedule()
        io_wait_queue = Queue()
        while 1:
            while not io_wait_queue.is_empty():
                status = io_complete()
                if status:
                    pass
            if current_job.quanta_remaining == 1:
                pass  # Mark current_job as swapped out
            elif scheduler.has_jobs():
                pass  # Mark current_job as swapped out (preempted)
            elif current_job.quanta_remaining > 1:
                status = io_request()
                if status:
                    pass  # Mark current_job as swapped out (sleeping on I/O)
                elif current_job.has_jobs():
                    pass  # Mark current_job as swapped out (end of timeslice)

            # Do bookkeeping and statistics
            clock += 1

            if current_job.state == "swapped_out":
                # Move job to appropriate queue
                break



if __name__ == '__main__':
    run_coordinator()

