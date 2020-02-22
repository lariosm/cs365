from collections import deque


class Queue:
    def __init__(self):
        self.queue = deque()

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        return self.queue.popleft()

    def peek(self, peek_to=0):
        return self.queue[peek_to]

    def peek_next(self):
        return self.queue[1]

    def is_empty(self):
        return len(self.queue) == 0


class PriorityQueue:
    def __init__(self, queue):
        self.queue_zero = Queue()
        self.queue_one = Queue()
        self.queue_two = Queue()
        self.queue_three = Queue()
        self.queue_four = Queue()
        self.queue_five = Queue()
        self.queue_six = Queue()
        self.queue_seven = Queue()

        for i in range(len(queue)):
            current_job = queue.peek(i)
            if current_job.priority == 0:
                self.queue_zero.enqueue(current_job)

        for i in range(len(queue)):
            current_job = queue.peek(i)
            if current_job.priority == 1:
                self.queue_one.enqueue(current_job)

        for i in range(len(queue)):
            current_job = queue.peek(i)
            if current_job.priority == 2:
                self.queue_two.enqueue(current_job)

        for i in range(len(queue)):
            current_job = queue.peek(i)
            if current_job.priority == 3:
                self.queue_three.enqueue(current_job)

        for i in range(len(queue)):
            current_job = queue.peek(i)
            if current_job.priority == 4:
                self.queue_four.enqueue(current_job)

        for i in range(len(queue)):
            current_job = queue.peek(i)
            if current_job.priority == 5:
                self.queue_five.enqueue(current_job)

        for i in range(len(queue)):
            current_job = queue.peek(i)
            if current_job.priority == 6:
                self.queue_six.enqueue(current_job)

        for i in range(len(queue)):
            current_job = queue.peek(i)
            if current_job.priority == 7:
                self.queue_seven.enqueue(current_job)

        # Empty out the original queue
        while not queue.is_empty():
            queue.dequeue()
