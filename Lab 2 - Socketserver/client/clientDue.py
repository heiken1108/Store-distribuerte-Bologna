from socket import socket, AF_INET, SOCK_STREAM
import os

class MyClient:
  def __init__(self, host="127.0.0.1", port=4449):
    self.socket = None
    try:
      self.socket = socket(AF_INET, SOCK_STREAM)
      self.socket.connect((host, port))
    except Exception as e:
      print(e)
      exit()
      
  def get_client_files(self):
    return os.listdir("./clientFiles")
  
  def get_all_files(self):
    print("Getting all files")
    all_files = set()
    all_files.update(self.get_client_files())

    self.socket.send('ls'.encode())
    response = self.socket.recv(1024)
    
    files = eval(response.decode())
    all_files.update(files)
    print(all_files)
    return list(all_files)

  def read_file(self, file_name):
    with open(f"clientFiles/{file_name}", 'r') as file:
      print(file.read())

  def run(self):
    while True:
      choice = input("Which operation would you like to perform? (R: Read a file, Q: Quit) ")
      if choice == 'Q':
        break
      elif choice == 'R':
        files = self.get_all_files()
        print("Files available: ")
        for i, file in enumerate(files):
          print(f"{i+1}. {file}")
        file_name = input("Enter the filename of the file you want to read (including extension): ")
        if file_name in self.get_client_files():
          self.read_file(file_name)
        else: 
          print("File not found in client files, requesting from server...") 
          self.socket.send(file_name.encode())
          response = self.socket.recv(1024)
          print(response.decode())

if __name__ == '__main__':
  client = MyClient(port=4449)
  client.run()
  
  