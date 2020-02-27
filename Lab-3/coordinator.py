from job_queue import Queue
from interfaces import Job
from schedulers import NonAggressivePreemptiveScheduler, AggressivePreemptiveScheduler
from prettytable import PrettyTable
import random
import sys


CHANCE_OF_IO_REQUEST = 10
CHANCE_OF_IO_COMPLETE = 4


def read_jobs():
    with open('scheduling_data.txt') as file:
        # pid, arrival_time, burst_time, priority
        return list(map(int, file.read().replace(":", "").split()))


def io_request():
    return round(random.random() * 100000) % CHANCE_OF_IO_REQUEST == 0


def io_complete():
    return round(random.random() * 100000) % CHANCE_OF_IO_COMPLETE == 0


def run_coordinator(schedule_type=NonAggressivePreemptiveScheduler()):
    clock = 0
    job_list = read_jobs()  # Holds a list of read-in job data
    queue = Queue()  # Holds jobs
    io_wait_queue = Queue()  # Holds jobs requesting I/O
    completed_queue = []  # Holds completed jobs

    for i in range(0, len(job_list), 4):
        job = Job()
        job.pid = job_list[i]
        job.arrival_time = job_list[i + 1]
        job.burst_time = job_list[i + 2]
        job.priority = job_list[i + 3]
        job.state = "ready"
        queue.enqueue(job)

    scheduler = schedule_type

    # Makes initial call to add jobs to the scheduler
    scheduler.add_jobs(queue, clock)

    # While there are jobs in the system
    while scheduler.has_jobs(queue):
        current_job = scheduler.schedule()  # Choose job to execute
        if current_job is None:  # Are we running an idle process
            clock += 1
            # Add jobs to ready queue based on arrival time
            scheduler.add_jobs(queue, clock)
            # Update jobs' time spent in ready state
            scheduler.update_ready_time(queue)
            continue
        while 1:
            if not io_wait_queue.is_empty():
                # Holds jobs to delete from io_wait_queue, so as not to
                # mess with code in line 63
                jobs_to_delete = []
                # Runs through io_wait_queue once
                for i in range(io_wait_queue.size()):
                    io_job = io_wait_queue.peek(i)
                    io_job.io_block = io_complete()
                    # Update job's time spent in I/O state
                    io_job.total_time_in_io_state += 1
                    if not io_job.io_block:  # Checks if job's I/O is complete
                        scheduler.reschedule(io_job)
                        jobs_to_delete.append(i)

                # Next, we delete jobs from io_wait_queue
                jobs_to_delete.sort(reverse=True)  # Helps delete without issue
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
                # Has this job been on the CPU for an entire timeslice?
                elif current_job.quanta_remaining == 1:
                    current_job.swapped_out = True
                    current_job.state = "end_of_time_slice"

            current_job.burst_time -= 1
            current_job.quanta_remaining -= 1
            clock += 1
            # Add jobs to ready queue based on arrival time
            scheduler.add_jobs(queue, clock)
            # Update jobs' time spent in ready state
            scheduler.update_ready_time(queue)

            if current_job.swapped_out:
                if current_job.state == "sleeping":
                    io_wait_queue.enqueue(current_job)
                elif current_job.state == "preempted":
                    scheduler.reschedule(current_job)
                elif current_job.state == "end_of_time_slice":
                    scheduler.reschedule(current_job)
                elif current_job.state == "terminated":
                    current_job.total_time_in_system = \
                        current_job.total_time_in_ready_state + \
                        current_job.total_time_in_io_state
                    completed_queue.append(current_job)
                break
    print_stats(completed_queue, clock)


def print_stats(jobs, total_time):
    # Creates a PrettyTable object with "headers"
    table = PrettyTable(["Job#", "Total time in ready to run state",
                         "Total time in sleeping on I/O state",
                         "Total time in system"])

    jobs.sort(key=lambda x: x.pid)  # Sorts list by pid in ascending order
    for i in jobs:  # Fills the table with data
        table.add_row([f"pid{i.pid}", i.total_time_in_ready_state,
                       i.total_time_in_io_state,
                       i.total_time_in_ready_state + i.total_time_in_io_state])

    print(table)
    print(f"Total simulation run time: {total_time}")
    print(f"Total number of jobs: {len(jobs)}")
    print(f"Shortest job completion time: "
          f"{min(jobs, key=lambda x: x.total_time_in_system).total_time_in_system}")
    print(f"Longest job completion time: "
          f"{max(jobs, key=lambda x: x.total_time_in_system).total_time_in_system}")
    print(f"Average job completion time: "
          f"{sum(i.total_time_in_system for i in jobs) / len(jobs)}")
    print(f"Average time in ready queue: "
          f"{sum(i.total_time_in_ready_state for i in jobs) / len(jobs)}")
    print(f"Average time sleeping on I/O state: "
          f"{sum(i.total_time_in_io_state for i in jobs) / len(jobs)}")


if __name__ == '__main__':
    if len(sys.argv) == 1:
        run_coordinator(NonAggressivePreemptiveScheduler())
    elif sys.argv[1] == "-A":
        print("Running multi-level aggressive scheduling")
        print("NOTE: At present, this scheduler is half working, following "
              "only rule (2)'")
        print()
        run_coordinator(AggressivePreemptiveScheduler())
    elif sys.argv[1] == "-N":
        print("Running multi-level non-aggressive scheduling (default)")
        print()
        run_coordinator(NonAggressivePreemptiveScheduler())
    elif sys.argv[1] == "-S":
        print("Running preemptive shortest job first (PSJF) scheduling")
        print("NOTE: At present, this scheduler type has yet to be implemented")
        print("Exiting...")
        sys.exit(0)
    elif sys.argv[1] == "-h":
        print("options:")
        print("\t-A   Runs multi-level aggressive scheduler")
        print("\t-N   Runs multi-level non-aggressive scheduler (default)")
        print("\t-S   Runs preemptive shortest job first scheduler")
    else:
        print("invalid argument")
        print("Type -h for help")
        print()
