from enum import Enum
import socketserver
from lagra_networking import send_data, receive_data

class NameTakenError(Exception):
    print("Name is already in use")

class StringLengthError(Exception):
    print("String is out of scope")

class InputTYPE(Enum):
    INPT_USERNAME = 1
    INPT_PASSWORD = 2


class Storage():
    user_objects = {}
    shared_storage = []
    def __init__(self):
        self.storage = []


class User():
    def __init__(self, usrname, pswd, usrid):
        self.username = usrname
        self.password = pswd
        self.user_id = usrid
        self.personal_storage = Storage(self)
        Storage.user_objects[self.user_id] = self


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        print("A client connected")
        
        while True:
            data = receive_data(self.request)
            if data:
                print(f"Received: {data}")
                response = self.process_request(data)
                send_data(self.request, response)
            else:
                break  # Exit loop if data is null

    def process_request(self, data):
        # Request responses
        if data == "CREATE_USER":
            return "User created successfully!"
        return "Unknown request"

def start_server(host, port):
    with socketserver.TCPServer((host, port), RequestHandler) as server:
        print("Server is listening on port", port)
        server.serve_forever()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8585
    start_server(HOST, PORT)
