from collections import deque


queue = deque()


def enqueue(job):
    queue.append(job)


def dequeue():
    return queue.popleft()


def peek():
    return queue[0]


def peek_next(n):
    return queue[n + 1]


def is_empty():
    return len(queue) < 1
