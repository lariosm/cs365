from job_queue import Queue
from interfaces import Job
from schedulers import NonAggressivePreemptiveScheduler
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
    # random_seed = random.seed(None)
    job_list = read_jobs()  # Holds a list of read-in job data
    queue = Queue()  # Holds jobs
    io_wait_queue = Queue()  # Holds jobs requesting I/O
    completed_queue = Queue()

    for i in range(0, len(job_list), 4):
        job = Job()
        job.pid = job_list[i]
        job.arrival_time = job_list[i + 1]
        job.burst_time = job_list[i + 2]
        job.priority = job_list[i + 3]
        job.state = "ready"
        queue.enqueue(job)
    print("STATUS: Jobs read in.... OK")  # Just for me...

    scheduler = NonAggressivePreemptiveScheduler()
    print("STATUS: Jobs processed into scheduler.... OK")  # Just for me...

    # While there are jobs in the system
    while scheduler.has_jobs(queue):
        scheduler.add_jobs(queue, clock)
        current_job = scheduler.schedule()  # Choose job to execute
        while 1:
            if not io_wait_queue.is_empty():
                # Holds jobs to delete from io_wait_queue, so as not to
                # mess with code in line 56
                jobs_to_delete = []
                # Runs through io_wait_queue once
                for i in range(len(io_wait_queue.size())):
                    io_job = io_wait_queue.peek(i)
                    io_job.io_block = io_complete()
                    if current_job.status:  # Checks if job's I/O is complete
                        scheduler.reschedule(io_job)
                        jobs_to_delete.append(i)

                # Next, we delete jobs from io_wait_queue
                for i in jobs_to_delete:
                    io_wait_queue.delete(i)

            if current_job.burst_time == 1:  # Is this job finished?
                current_job.swapped_out = True
                current_job.state = "terminated"
            # Check if there are now higher priority jobs on the ready to run state.
            elif scheduler.check_priority_queues(current_job):
                current_job.swapped_out = True
                current_job.state = "preempted"
            elif current_job.burst_time > 1:  # Does this job still have a while to go?
                current_job.io_block = io_request()
                if current_job.io_block:  # Do we need to do I/O for this job?
                    current_job.swapped_out = True
                    current_job.state = "sleeping"
                elif current_job.quanta_remaining == 1:  # Has this job been on the CPU for an entire timeslice?
                    current_job.swapped_out = True
                    current_job.state = "end_of_timeslice"

            # Do bookkeeping and statistics
            current_job.burst_time -= 1
            current_job.quanta_remaining -= 1
            clock += 1

            if current_job.swapped_out:
                if current_job.state == "sleeping":
                    io_wait_queue.enqueue(current_job)
                elif current_job.state == "preempted":
                    scheduler.reschedule(current_job)
                elif current_job.state == "end_of_time_slice":
                    scheduler.reschedule(current_job)
                elif current_job.state == "terminated":
                    completed_queue.enqueue(current_job)
                continue


if __name__ == '__main__':
    run_coordinator()
