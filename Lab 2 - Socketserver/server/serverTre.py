from socket import *

class SimpleSocketServer:
    def __init__(self, host='', port=4449):
        self.host = host  # Host can be '' to listen on all available interfaces
        self.port = port
        self.server_socket = socket(AF_INET, SOCK_STREAM)

        # Try to bind the socket to the specified port
        try:
            self.server_socket.bind((self.host, self.port))
            print(f"Server started on port {self.port}")
        except OSError:
            print("Port already in use")
            raise  # Optionally raise the exception to stop the server

        # Start listening for incoming connections
        self.server_socket.listen(1)
        print(f"Listening for connections on port {self.port}...")

    def handle_client(self, connection_socket, address):
        try:
            # Receive the message from the client
            message = connection_socket.recv(1024).decode()
            print("Message received from client:", message)

            if message:
                filepath = message
                print(f"Requested file: {filepath}")

                try:
                    # Open and read the requested file
                    with open(f"serverFiles/{filepath}", "r") as file:
                        output_data = file.read()

                    # Send the file content to the client
                    connection_socket.send(output_data.encode())
                except FileNotFoundError:
                    # Send error message if file is not found
                    connection_socket.send("File not found".encode())
        except (IOError, IndexError) as e:
            # Handle any other errors that occur during communication
            print(f"Error occurred: {e}")
            connection_socket.send("An error occurred".encode())
        finally:
            # Close the client connection
            connection_socket.close()

    def start(self):
        # Main loop to accept and handle clients
        try:
            while True:
                print("Waiting for a connection...")
                connection_socket, address = self.server_socket.accept()
                print(f"Connection from {address}")

                # Handle the client connection
                self.handle_client(connection_socket, address)

        except KeyboardInterrupt:
            print("Server interrupted. Shutting down...")

        finally:
            # Close the server socket on shutdown
            self.server_socket.close()
            print("Server socket closed.")

# Usage of the class
if __name__ == "__main__":
    server = SimpleSocketServer(port=4449)  # You can set a different port if needed
    server.start()
