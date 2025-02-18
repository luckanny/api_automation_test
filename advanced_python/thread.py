from threading import Thread
from queue import Queue
import time


# def print_count(n):
#     for i in range(n):
#         print(i)
#
#
# t1 = Thread(target=print_count, args=(100,))
# t2 = Thread(target=print_count, args=(200,))
# t1.start()
# t2.start()
# t1.join()
# t2.join()

class MyThread(Thread):
    def __init__(self, name: str, count: int):
        super(MyThread, self).__init__()
        self.name = name
        self.count = count
        self.daemon = True



    def run(self) -> None:
        for n in range(self.count):
            print(f"{self.name} - {n}\n", end="")
            time.sleep(0.01)


t1 = MyThread("A", 10)
t2 = MyThread("B", 10)
# t2.daemon = True
# t1.daemon = True

# t1.start()
# t2.start()
# t1.join()
# t2.join()


class MsgProducer(Thread):
    def __init__(self, name: str, count: int, queue: Queue):
        super(MsgProducer, self).__init__()
        self.name = name
        self.count = count
        self.queue = queue

    def run(self) -> None:
        for n in range(self.count):
            msg = f"{self.name} - {n}"
            self.queue.put(msg, block=True)


class MsgConsumer(Thread):
    def __init__(self, name: str, queue: Queue):
        super(MsgConsumer, self).__init__()

        self.name = name
        self.daemon = True
        self.queue = queue

    def run(self) -> None:
        while True:
            msg = self.queue.get(block=True)
            print(f"{self.name} - {msg}\n", end="")


queue = Queue(3)
threads = list()
threads.append(MsgProducer("PA", 10, queue))
threads.append(MsgProducer("PB", 10, queue))
threads.append(MsgProducer("PC", 10, queue))

threads.append(MsgConsumer("CA", queue))
threads.append(MsgConsumer("CB", queue))

for t in threads:
    t.start()

# for t in threads:
#     t.join()

