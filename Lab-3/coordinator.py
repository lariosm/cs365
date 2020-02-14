import random

job_list = []


def read_jobs():
    with open('scheduling_data.txt') as file:
        # pid, arrival_time, service_time, priority
        job_list = list(map(str, file.read().replace(":", "").split()))


def io_request(change_of_io_request):
    if random.random() % change_of_io_request == 0:
        return 1
    else:
        return 0


def io_complete(change_of_io_complete):
    if random.random() % change_of_io_complete == 0:
        return 1
    else:
        return 0


clock = 0
rand_val = random.random()

# Unfinished as of this commit
