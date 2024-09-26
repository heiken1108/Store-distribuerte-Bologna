from socket import *
import os

class Server:
    def __init__(self, host='', port=4449):
        self.host = host
        self.port = port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socketIsSet = False

        try:
            self.server_socket.bind((self.host, self.port))
            print(f"Server started on port {self.port}")
        except OSError:
            print("Port already in use")
            raise

        self.server_socket.listen(1)

    def handle_client_request(self, connection_socket: socket, address):
        print(f"Handle request from {address}")
        try:
            message = connection_socket.recv(1024).decode()
            print("Message received from client:", message)
            if message is not None:
                if message == 'ls':
                    file_response = self.fetch_all_filenames()
                else:
                    file_response = self.fetch_file_content(filename=message)
                connection_socket.send(file_response.encode())
            else:
                connection_socket.send("No message received".encode())

        except (IOError, IndexError):
            connection_socket.send("An error occurred when handling the request".encode())
        finally:
            connection_socket.close()
            
    def fetch_all_filenames(self):
        return str(os.listdir("files"))

    def fetch_file_content(self, filename):
        try:
            with open(f"files/{filename}", "r") as file:
                output_data = file.read()
                return output_data
        except FileNotFoundError:
            return "File not found"

    def start(self):
        try:
            while True:
                connection_socket, address = self.server_socket.accept()
                print(f"Connection established with {address}")
                self.handle_client_request(connection_socket, address)
        
        except KeyboardInterrupt:
            print("\nServer interrupted. Shutting down")
            self.server_socket.close()
            print("Server closed.")
            

if __name__ == "__main__":
    server = Server(port=4449)
    server.start()