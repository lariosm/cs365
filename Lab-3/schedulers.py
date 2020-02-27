from job_queue import PriorityQueue


class NonAggressivePreemptiveScheduler:
    def __init__(self):
        self.queues = PriorityQueue()
        self.switcher = {
            0: self.queues.queue_zero,
            1: self.queues.queue_one,
            2: self.queues.queue_two,
            3: self.queues.queue_three,
            4: self.queues.queue_four,
            5: self.queues.queue_five,
            6: self.queues.queue_six,
            7: self.queues.queue_seven
        }

    def schedule(self):
        for i in range(len(self.switcher)):
            current_queue = self.switcher.get(i)
            if not current_queue.is_empty():
                job = current_queue.dequeue()
                job.prev_priority = i  # Current job's previous priority
                job.priority = 0  # Marks current job with priority 0
                job.state = "running"

                # Assigns a number of quanta to the job
                if i == 0:
                    job.quanta_remaining = 1
                else:
                    job.quanta_remaining = 2 * i
                return job

        return None

    def reschedule(self, job):
        if job.state == "sleeping" or job.state == "preempted":
            job.state = "ready"
            job.swapped_out = False
            job.prev_priority = None  # Sets previous job priority to null
            self.queues.queue_zero.enqueue(job)
        elif job.state == "end_of_time_slice":
            if job.prev_priority == 7:
                job.priority = 7
                job.prev_priority = None  # Sets previous job priority to null
                job.state = "ready"
                job.swapped_out = False
                self.queues.queue_seven.enqueue(job)
            else:
                job.priority = job.prev_priority + 1  # Lowers job's priority
                job.prev_priority = None  # Sets previous job priority to null
                job.state = "ready"
                job.swapped_out = False
                self.switcher.get(job.priority).enqueue(job)

    # Checks if there are jobs in priority queue or job queue in coordinator.py
    def has_jobs(self, queue):
        for i in range(len(self.switcher)):
            if not self.switcher.get(i).is_empty():
                return True
        if not queue.is_empty():
            return True
        return False

    # Adds jobs to their respective priority queues by arrival time
    def add_jobs(self, jobs_queue, clock):
        # Holds jobs to delete from job_queue, so as not to
        # mess with code in line 70
        jobs_to_delete = []
        for i in range(len(self.switcher)):
            for j in range(jobs_queue.size()):
                current_job = jobs_queue.peek(j)
                if current_job.priority == i and current_job.arrival_time == clock:
                    self.switcher.get(i).enqueue(current_job)
                    jobs_to_delete.append(j)

        # Next, we delete jobs from jobs_queue
        jobs_to_delete.sort(reverse=True)
        for i in jobs_to_delete:
            jobs_queue.delete(i)

    # Checks if there's a higher priority job that needs to be run
    def check_priority_queues(self, current_job):
        for i in range(len(self.switcher)):
            # Checks if current priority queue (i.e. queue_three) is empty
            if not self.switcher.get(i).is_empty():
                # Is the current job's priority higher than the priority queue
                if i < current_job.priority:
                    return True
        return False

    def update_ready_time(self, jobs_queue):
        # Updates ready time in each job in original job queue
        for i in range(jobs_queue.size()):
            jobs_queue.peek(i).total_time_in_ready_state += 1

        # Updates ready time in each job in priority queues
        for i in range(len(self.switcher)):
            for j in range(self.switcher.get(i).size()):
                self.switcher.get(i).peek(j).total_time_in_ready_state += 1


# NOTE: This class inherits from class NonAggressivePreemptiveScheduler
class AggressivePreemptiveScheduler(NonAggressivePreemptiveScheduler):
    def reschedule(self, job):
        if job.state == "sleeping":
            if job.prev_priority == 0:
                job.priority = 0
            else:
                job.priority = job.prev_priority - 1
            job.prev_priority = None  # Sets previous job priority to null
            job.state = "ready"
            job.swapped_out = False
            self.switcher.get(job.priority).enqueue(job)
        if job.state == "preempted":
            job.state = "ready"
            job.swapped_out = False
            job.prev_priority = None  # Sets previous job priority to null
            self.queues.queue_zero.enqueue(job)
        elif job.state == "end_of_time_slice":
            if job.prev_priority == 7:
                job.priority = 7
                job.prev_priority = None  # Sets previous job priority to null
                job.state = "ready"
                job.swapped_out = False
                self.queues.queue_seven.enqueue(job)
            else:
                job.priority = job.prev_priority + 1  # Lowers job's priority
                job.prev_priority = None  # Sets previous job priority to null
                job.state = "ready"
                job.swapped_out = False
                self.switcher.get(job.priority).enqueue(job)