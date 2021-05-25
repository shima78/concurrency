from threading import Condition, Lock, Thread
from time import sleep


class ReadersWriters:
    def __init__(self):
        self.readersCount = 0
        self.writersCount = 0
        self.waitingReaders = 0
        self.waitingWriters = 0
        self.ok_to_read = Condition()
        self.ok_to_write = Condition()
        self.file = []

    def beginRead(self):
        while self.writersCount == 1 or self.waitingWriters > 0:
            self.waitingReaders += 1
            with self.ok_to_read:
                self.ok_to_read.wait()
            self.waitingReaders -= 1
        self.readersCount += 1
        with self.ok_to_read:
            self.ok_to_read.notify()

    def endRead(self):
        self.readersCount -= 1
        if self.readersCount == 0:
            with self.ok_to_write:
                self.ok_to_write.notify()


    def reader(self, reader_id):
        self.beginRead()
        print(f"Reader {reader_id}: {self.file}")
        self.endRead()

    def beginWrite(self):
        while self.readersCount > 0 or self.writersCount == 1:
            self.waitingWriters += 1
            with self.ok_to_write:
                self.ok_to_write.wait()
            self.waitingWriters -= 1
        self.writersCount = 1

    def endWrite(self):
        self.writersCount = 0
        if self.waitingReaders:
            with self.ok_to_read:
                self.ok_to_read.notify()
        else:
            with self.ok_to_write:
                self.ok_to_write.notify()

    def writer(self, writer_id):
        self.beginWrite()
        self.file.clear()
        for i in range(10):
            self.file.append(writer_id)
        self.endWrite()


if __name__ == "__main__":
    problem = ReadersWriters()
    writers = []
    readers = []

    for i in range(5):
        readers.append(Thread(target=problem.reader, args=[i]))
        writers.append(Thread(target=problem.writer, args=[i]))
        writers[-1].start()
        readers[-1].start()


    for thread in readers:
        thread.join()

    for thread in writers:
        thread.join()

    # test.join()

    # test.join()
