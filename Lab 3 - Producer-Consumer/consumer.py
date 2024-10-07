from threading import Semaphore, Thread
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from random import random
from time import sleep
import sys


class Consumer:
    def __init__(self, buffer_size):
        self.buffer = Queue()
        self.empty = Semaphore(buffer_size)
        self.full = Semaphore(0)
        self.mutex = Semaphore(1)
        self.consumed = []
        self.serversocket = socket(AF_INET, SOCK_STREAM)
        self.serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serversocket.bind(("", 4449))
        self.serversocket.listen(1)

    def produce(self):
        while True:
            self.empty.acquire()
            self.mutex.acquire()
            print("%s aquired mutex" % Thread.name)
            (conn, address) = self.serversocket.accept()
            print(f"Connection from {address} has been established!")
            item = conn.recv(1024).decode()
            print(f"Received data: {item} \n\n")
            self.buffer.put(item)
            conn.send(f"Item {item} received".encode())
            conn.close()
            self.mutex.release()
            self.full.release()

    def consume(self):
        while True:
            self.full.acquire()
            self.mutex.acquire()
            print("%s aquired mutex" % Thread.name)
            item = self.buffer.get()
            print("Consuming item:", item)
            self.consumed.append(item)
            sleep(random())  # Simulate time to consume
            print(f"Total amount consumed: {len(self.consumed)} items \n\n")
            self.mutex.release()
            self.empty.release()

    def run(self):
        try:
            p = Thread(target=self.produce)
            c = Thread(target=self.consume)
            p.daemon = True
            c.daemon = True
            p.start()
            c.start()
            while True:
                sleep(1)
        except (KeyboardInterrupt, SystemExit):
            print("Exiting program in run method")
            sys.exit()


if __name__ == "__main__":
    print("Create PCProblem")
    pc = Consumer(10)
    pc.run()
