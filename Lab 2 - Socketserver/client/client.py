from socket import * 
import time
import os

def get_all_files():
  all_files = []
  all_files.append(os.listdir("clientFiles"))
  

print("Starting client")

try:
  s = socket(AF_INET, SOCK_STREAM)
  # Connect to the server
  s.connect(("127.0.0.1", 4449))

except:
  print("Couldn't connect to the server.")
  exit()

while True:
  choice = input("Which operation would you like to perform? (R: Read a file, Q: Quit) ")
  if choice.lower() == "q":
    s.close()
    print("Connection closed.")
    break
  file_name = input("Enter the name of the file you want to read (including extension): ")
  try:
    s.send(f"{file_name}".encode())
    server_response = s.recv(1024)
    print(server_response.decode())
    #break
  except:
    print("Something wrong happened.")
    time.sleep(5)