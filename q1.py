from threading import Thread, Semaphore
from time import sleep

storage = []
STORAGE_LIMIT = 5

empty = Semaphore(STORAGE_LIMIT)
mutex = Semaphore(1)
full = Semaphore(0)


def producer(products, thread_id):
    for product in products:
        empty.acquire()
        mutex.acquire()
        storage.append(f"\nProducer {thread_id} Produced {product}")  # add product
        mutex.release()
        # sleep(0.5)
        full.release()
        print(f"\nLength is {len(storage)}")
    empty.acquire()
    mutex.acquire()
    storage.append(None)  # add product
    mutex.release()
    full.release()

def consumer(consumer_id):
    # sleep(1)
    full.acquire()
    mutex.acquire()
    data = storage.pop(0)
    mutex.release()
    empty.release()
    while data is not None:
        print(data)
        full.acquire()
        mutex.acquire()
        data = storage.pop(0)
        mutex.release()
        empty.release()

    print(f"\nconsumer {consumer_id} terminated")













if __name__ == "__main__":
    data = [
        [x for x in range(5)]
        for _ in range(8)
    ]
    producers = []
    consumers = []

    for i in range(8):
        producers.append(Thread(target=producer, args=[data[i], i]))
        producers[-1].start()

    for i in range(8):
        consumers.append(Thread(target=consumer, args=[i]))
        consumers[-1].start()

    for thread in producers:
        thread.join()

    for thread in consumers:
        thread.join()
