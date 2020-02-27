from collections import deque


class Queue:
    def __init__(self):
        self.queue = deque()  # Initializes deque object

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return self.queue.popleft()

    def delete(self, at_index):
        self.queue.__delitem__(at_index)

    def peek(self, peek_to=0):
        return self.queue[peek_to]

    def peek_next(self):
        return self.queue[1]

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def clear(self):
        self.queue.clear()


class PriorityQueue:
    def __init__(self):
        self.queue_zero = Queue()
        self.queue_one = Queue()
        self.queue_two = Queue()
        self.queue_three = Queue()
        self.queue_four = Queue()
        self.queue_five = Queue()
        self.queue_six = Queue()
        self.queue_seven = Queue()
