job_list = []


def read_jobs():
    with open('scheduling_data.txt') as file:
        # pid, arrival_time, service_time, priority
        job_list = list(map(str, file.read().replace(":", "").split()))
