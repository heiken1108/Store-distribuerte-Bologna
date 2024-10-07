from socket import socket, AF_INET, SOCK_STREAM
import threading, json
from shared import Data

class Producer():
  def __init__(self, even: bool, lock: threading.Lock, host="Bibbebaby", port=4449):
    self.host = host
    self.port = port
    self.even = even
    self.lock = lock

  def send_data(self):
    i = 0
    while True:
      n = Data(2*i if self.even else 2*i + 1, threading.get_ident())
      with self.lock:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.send(json.dumps(n, default=lambda o: o.__dict__).encode())
        response = sock.recv(1024)
        print(response.decode())
      i += 1

def run_threads():
  lock = threading.Lock() 

  producerEven = Producer(even=True, lock=lock)
  producerOdd = Producer(even=False, lock=lock)

  threadEven = threading.Thread(target=producerEven.send_data)
  threadOdd = threading.Thread(target=producerOdd.send_data)
  threadEven.start()
  threadOdd.start()

if __name__ == "__main__":
  run_threads()