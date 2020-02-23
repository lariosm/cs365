from job_queue import PriorityQueue


class NonAgressivePreemptiveScheduler:
    def __init__(self, queue):
        self.queues = PriorityQueue(queue)

    def schedule(self):
        switcher = {
            0: self.queues.queue_zero,
            1: self.queues.queue_one,
            2: self.queues.queue_two,
            3: self.queues.queue_three,
            4: self.queues.queue_four,
            5: self.queues.queue_five,
            6: self.queues.queue_six,
            7: self.queues.queue_seven
        }

        for i in range(len(switcher)):
            current_queue = switcher.get(i)
            if not current_queue.is_empty():
                job = current_queue.dequeue()
                job.priority = 0  # Marks current job with priority 0
                job.state = "running"

                # Assigns a number of quanta to the job
                if i == 0:
                    job.quanta_remaining = 1
                else:
                    job.quanta_remaining = 2 * i
                return job

        return None

    def reschedule(self):
        pass

    def has_jobs(self):
        # Our last "line of defense" in deciding if there are jobs left
        return self.queues.queue_seven.is_empty()

    def peek_next(self):
        pass
