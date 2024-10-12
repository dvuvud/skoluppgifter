from enum import Enum
import socketserver
from lagra_networking import send_data, receive_data, request_input

class NameTakenError(Exception):
    pass

class StringLengthError(Exception):
    pass

class IllegalCharacterError(Exception):
    pass

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
        self.personal_storage = Storage()
        Storage.user_objects[self.user_id] = self


class RequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        self.currentuser = None
        super().__init__(*args, **kwargs)
    def handle(self):
        print("A client connected")
        
        while True:
            data = receive_data(self.request)
            if data:
                print(f"Received: {data}")
                response = self.process_request(data)
                send_data(self.request, response)

    def process_request(self, data):
        # request responses
        if data == "CREATE_USER":
            username = input_handling(InputTYPE.INPT_USERNAME, None, self)
            password = input_handling(InputTYPE.INPT_PASSWORD, None, self)
            user_id = hash(username) # the user id is dependant on the username through the hash function
            new_user = User(username,password,user_id)
            Storage.user_objects[user_id] = new_user
            send_data(self.request, "User Created")
        elif data == "LOGIN":
            """
            logic for assigning the current user to the session
            hard to understand gotta rewrite if I have time
            """
            send_data(self.request, "REQUEST_INPUT")
            if receive_data(self.request) != "RECEIPT":
                    return
            send_data(self.request, "Enter username: ")
            user_id = hash(receive_data(self.request))
            if user_id in Storage.user_objects:
                send_data(self.request, "REQUEST_INPUT")
                if receive_data(self.request) != "RECEIPT":
                    return
                send_data(self.request, "Enter password: ")
                if Storage.user_objects[user_id].password == receive_data(self.request):
                    self.currentuser = Storage.user_objects[user_id]
                    print(f"Client now logged in as {self.currentuser.username}")
                    send_data(self.request, f"Now logged in as {self.currentuser.username}")
                else:
                    send_data(self.request, "Incorrect password, try again")
            else:
                send_data(self.request, "User doesn't exist")

def start_server(host, port):
    with socketserver.TCPServer((host, port), RequestHandler) as server:
        print("Server is listening on port", port)
        server.serve_forever()


def input_handling(context, input = None, request_handler = None):
    if context == InputTYPE.INPT_USERNAME:
        while True:
            try:
                data = request_input(request_handler.request, "Choose a username between 3-12 characters: ")
                if hash(data) in Storage.user_objects: # if the user id already exists the name is also already taken
                    raise NameTakenError()
                elif len(data) < 3 or len(data) > 12:
                    raise StringLengthError()
                elif ' ' in data:
                    IllegalCharacterError()
                return data
            except NameTakenError:
                send_data(request_handler.request, "ERROR: Username is already taken")
                print("ERROR: Username is already taken")
                continue
            except StringLengthError:
                send_data(request_handler.request, "ERROR: The length of the input is out of scope")
                print("ERROR: Length of input out of scope")
                continue
            except IllegalCharacterError:
                send_data(request_handler.request, "ERROR: String contains illegal character(s)")
                print("ERROR: String contains illegal character(s)")
                continue
    
    elif context == InputTYPE.INPT_PASSWORD:
        while True:
            try:
                request_input(request_handler.request, "Choose a password between 3-12 character: ")
                data = receive_data(request_handler.request)
                if len(data) < 3 or len(data) > 12:
                    raise StringLengthError()
                elif ' ' in data:
                    raise IllegalCharacterError()
                return data
            except StringLengthError:
                send_data(request_handler.request, "ERROR: The length of the input is out of scope")
                print ("ERROR: Length of input out of scope")
                continue
            except IllegalCharacterError:
                send_data(request_handler.request, "ERROR: String contains illegal character(s)")
                print("ERROR: String contains illegal character(s)")
                continue
            
            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8585
    start_server(HOST, PORT)


