import socketserver
import server_backend

HOST, PORT = 'localhost', 8585


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self): # den här funktionen körs en gång när servern blivit kopplad till en klient
        print(f"Connection from {self.client_address}")
        while True:
            try:
                # Receive data
                data = self.request.recv(1024)
                if not data:
                    print(f"Client {self.client_address} disconnected.")
                    break

                # Response
                print(f"Received from {self.client_address}: {data.decode()}")
                self.request.sendall(b"Message received!")
            except ConnectionResetError:
                print(f"Connection with {self.client_address} lost.")
                break
            except Exception as e:
                print(f"Error occured: {e}")

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, *args, **kwargs): # called when the server is initialized
        print("Server is initialized")
        super().__init__(*args, **kwargs)

    def server_activate(self): # called on server startup, can accept new connections (inherited from TCPServer)
        super().server_activate() 
        print("Server is now active and ready for connections.")

    def finish_request(self, request, client_address): # called when a client connection is accepted (inherited from TCPServer)
        print(f"Client connected: {client_address}")  
        super().finish_request(request, client_address)  


def start_server():
    with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        print(f"Server is listening on {HOST} : {PORT}")
        server.serve_forever()


if __name__ == "__main__":
    start_server()