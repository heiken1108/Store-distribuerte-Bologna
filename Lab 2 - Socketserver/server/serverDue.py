from socket import *

class Server:
  def __init__(self, port = 4450, host = ''):
    self.port = port
    self.host = host
    self.serversocket = socket(AF_INET, SOCK_STREAM)
    self.serversocket.bind(('', port))
    self.serversocket.listen(1)
  
  def handle_client(self, client_socket: socket, client_address):
    print(f"We have connected to {client_address}:{client_socket}")
    while True:
      message = client_socket.recv(1024).decode()

      if message is not None:
        filepath = message.split()[1]
        print(filepath)
        f = open(f"serverFiles/{filepath[1:]}")
        outputdata = f.read()
        client_socket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
        response = outputdata + "\r\n"
        client_socket.send(response.encode()) 
        client_socket.close()

  def run_server(self):
    print('Starting server')
    while True:
      client_socket, address = self.serversocket.accept()
      client_socket.send("Connection established\r\n\r\n".encode())
      try:
        self.handle_client(client_socket, address)
      except(IOError, IndexError):
        client_socket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        client_socket.send("<html><head></head><body><h1>404 Not Found</h1></body></html>\r\n".encode())
      client_socket.close()
  
  def close_server(self):
    self.serversocket.close()

if __name__ == "__main__":
  server = Server()
  print('Starting server')
  try:
    server.run_server()
  except KeyboardInterrupt:
    server.close_server()

