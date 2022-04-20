import threading
from threading import Lock


# Creating a queue class with the following operations:
#   * Enqueue - Adds an element to the rear of the queue
#   * Dequeue - Removes an element from the front of the queue
class ThreadingQueue:
    # Initializes the queue and sets its max capacity to 10 unless
    # specified otherwise.
    # NOTE: We are using semaphores, threading, and locks to resolve the
    # producer-consumer problem.
    def __init__(self, max_capacity = 10):
        self.queue = []
        self.capacity = max_capacity
        self.semaphoreCapacity = threading.Semaphore(max_capacity)
        self.semaphoreUsed = threading.Semaphore(0)
        self.mutex = Lock()

    # Function that will allow us to add an element to the rear
    # of the queue. This is done by acquiring the mutex lock,
    # appending our item to the queue, and releasing the lock
    # and semaphores used.
    def enqueue(self, item):
        self.semaphoreCapacity.acquire()
        self.mutex.acquire()
        self.queue.append(item)
        self.mutex.release()
        self.semaphoreUsed.release()

    # Function that will allow us to remove an element from the
    # front of the queue. This is done by obtaining the lock,
    # popping the item at the 0th index (front of queue) and then
    # releasing the lock and semaphores used.
    def dequeue(self):
        self.semaphoreUsed.acquire()
        self.mutex.acquire()
        item = self.queue.pop(0)
        self.mutex.release()
        self.semaphoreCapacity.release()
        return item
