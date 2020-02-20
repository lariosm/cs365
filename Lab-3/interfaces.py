class JobState:
    def __init__(self, job_state):
        self.state = job_state


class Job:
    def __init__(self):
        self.pid = 0
        self.arrival_time = 0
        self.burst_time = 0
        self.priority = 0
        self.quanta_remaining = 0
        self.total_time_in_io_state = 0
