from socket import *

def run_server(serversocket: socket = None, port = 4449):
  try:
    serversocket.bind(('', port))
  except:
    print('Server is fucked')

  serversocket.listen(1)



  while True:
    print('We are ready')

    connectionSocket, address = serversocket.accept()
    
    try:
      message = connectionSocket.recv(1024).decode()
      print("Message:", message)
      if message is not None:
        filepath = message
        print(filepath)
        f = open(f"serverFiles/{filepath}", "r")
        outputdata = f.read()
        connectionSocket.send(outputdata.encode()) 
        connectionSocket.close()
    except(IOError, IndexError):
      connectionSocket.send("Filen ble ikke funnet".encode())

    connectionSocket.close()
    

  serversocket.close()

if __name__ == "__main__":
  serversocket = socket(AF_INET, SOCK_STREAM)
  try:
    run_server(serversocket)
  except KeyboardInterrupt:
    print('closing server')
    serversocket.close()
    print('Sevrer was closed')