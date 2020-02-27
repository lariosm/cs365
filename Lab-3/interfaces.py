class Job:
    def __init__(self):
        self.pid = None
        self.arrival_time = None
        self.burst_time = None
        self.priority = None
        self.prev_priority = None
        self.quanta_remaining = None
        self.total_time_in_io_state = 0
        self.total_time_in_ready_state = 0
        self.total_time_in_system = 0
        self.state = "new"
        self.io_block = False
        self.swapped_out = False


'''
    NOTE: The following job states are accepted in Job class in string form
    new, ready, preempted, still_running, sleeping, idling, terminated
'''
