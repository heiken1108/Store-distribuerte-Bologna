from threading import Semaphore, Thread, Lock, get_ident
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from random import random
from time import sleep
import sys
import json
from shared import Data


class Consumer:
    def __init__(self, buffer_size):
        self.buffer = Queue()
        self.empty = Semaphore(buffer_size)
        self.full = Semaphore(0)
        self.mutex = Lock()
        self.consumed = 0

    def produce_1(self):
        serversocket = socket(AF_INET, SOCK_STREAM)
        serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serversocket.bind(("", 4449))
        serversocket.listen(1)
        while True:
            self.empty.acquire()
            (conn, address) = serversocket.accept()
            print(f"Connection from {address} has been established!")
            item = conn.recv(1024).decode()
            print(f"Received data: {item} \n")
            with self.mutex:
                print("Thread %d aquired mutex" % get_ident())
                self.buffer.put(item)
            conn.send(f"Item {item} received".encode())
            conn.close()
            self.full.release()

    def produce_2(self):
        serversocket = socket(AF_INET, SOCK_STREAM)
        serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        serversocket.bind(("", 4448))
        serversocket.listen(1)
        while True:
            self.empty.acquire()
            (conn, address) = serversocket.accept()
            print(f"Connection from {address} has been established!")
            item = conn.recv(1024).decode()
            print(f"Received data: {item} \n")
            with self.mutex:
                print("Thread %d aquired mutex" % get_ident())
                self.buffer.put(item)
            conn.send(f"Item {item} received".encode())
            conn.close()
            self.full.release()

    def consume(self):
        while True:
            self.full.acquire()
            with self.mutex:
                print("Thread %d aquired mutex" % get_ident())
                item = self.buffer.get()
            item_dict = json.loads(item)
            item = Data(
                item_dict["n"],
                item_dict["created_by"],
                item_dict["created_at"],
            )
            print("Consuming item:", item)
            sleep(random())  # Simulate time to consume
            self.consumed += 1
            print(f"Total amount consumed: {self.consumed} items\n")
            self.empty.release()

    def run(self):
        try:
            p_1 = Thread(target=self.produce_1, daemon=True)
            p_2 = Thread(target=self.produce_2, daemon=True)
            c = Thread(target=self.consume, daemon=True)
            p_1.start()
            p_2.start()
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
