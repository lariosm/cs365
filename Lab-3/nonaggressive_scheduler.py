from collections import deque


class NonAgressivePreemptiveScheduler:
    def __init__(self, job_list):
        self.job_queue = deque()
        for i in range(0, len(job_list), 4):
            self.job_queue.append((job_list[i], job_list[i + 1], job_list[i + 2], job_list[i + 3]))

    def schedule_job(self):
        pass

# Unfinished as of this commit
