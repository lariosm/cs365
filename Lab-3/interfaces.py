# NOTE: Not sure if I'll keep this class around.
class JobState:
    def __init__(self, job_state):
        self.state = job_state


class Job:
    def __init__(self):
        self.pid = None
        self.arrival_time = None
        self.burst_time = None
        self.priority = None
        self.quanta_remaining = None
        self.total_time_in_io_state = None
        self.state = None


'''
    NOTE: The following job states are accepted in Job class in string form
    new, ready, preempted, still_running, sleeping, idling, terminated
'''
