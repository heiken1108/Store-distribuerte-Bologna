from socket import *

class Server:
    def __init__(self, host='', port=4449):
        self.host = host
        self.port = port
        self.server_socket = socket(AF_INET, SOCK_STREAM)
        self.server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

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
    
            if message is not None:
                filepath = message
                try:
                    with open(f"serverFiles/{filepath}", "r") as file:
                        output_data = file.read()

                    connection_socket.send(output_data.encode())
                except FileNotFoundError:
                    connection_socket.send("File was not found".encode())

        except (IOError, IndexError):
            connection_socket.send("An error occurred when handling the request".encode())
        finally:
            connection_socket.close()

    def start(self):
        try:
            while True:
                connection_socket, address = self.server_socket.accept()
                print(f"Connection established with {address}")

                self.handle_client_request(connection_socket, address)
        
        except KeyboardInterrupt:
            print("\nServer interrupted. Shutting down...")
        finally:
            self.server_socket.close()
            print("Server closed.")

if __name__ == "__main__":
    server = Server(port=4449)
    server.start()
