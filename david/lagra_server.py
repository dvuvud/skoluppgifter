from enum import Enum
import socketserver
from lagra_networking import send_data, receive_data, request_input

class NameTakenError(Exception):
    pass

class StringLengthError(Exception):
    pass

class IllegalCharacterError(Exception):
    pass

class EmptyStringError(Exception):
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
                self.process_request(data)
            elif not data:
                break

    def process_request(self, data):
        # request responses
        if data == "CREATE_USER":
            username = input_handling(InputTYPE.INPT_USERNAME, None, self)
            password = input_handling(InputTYPE.INPT_PASSWORD, None, self)
            user_id = hash(username) # the user id is dependant on the username through the hash function
            if username is None or password is None:
                return
            new_user = User(username,password,user_id)
            Storage.user_objects[user_id] = new_user
            send_data(self.request, "User created")
            print("User created")
        elif data == "LOGIN":
            login(self)
            return

def login(request_handler):
    """
logic for assigning the current user to the session
hard to understand gotta rewrite if I have time
    """
    user_object = None
    while True:
        try:
            data = request_input(request_handler.request, "Enter username: ")

            if data == "EMPTY_STRING":
                raise EmptyStringError()
            user_id = hash(data)
            if user_id in Storage.user_objects:
                user_object = Storage.user_objects[user_id]

                send_data(request_handler.request, "Accepted")
                data = request_input(request_handler.request, "Enter password: ")

                if data == "EMPTY_STRING":
                    raise EmptyStringError()
                if Storage.user_objects[user_id].password == data:
                    request_handler.currentuser = Storage.user_objects[user_id]
                    print(f"Client now logged in as {request_handler.currentuser.username}")
                    send_data(request_handler.request, "Logged in")
                    in_session(request_handler, user_object)
                    return
                else:
                    send_data(request_handler.request, "Incorrect password, try again")
                    continue
            else:
                send_data(request_handler.request, "User doesn't exist")
                continue
        except EmptyStringError:
            send_data(request_handler.request, "ERROR: input cannot be empty")
            continue

def in_session(request_handler, user_object):
    print("Sessioning")

def start_server(host, port):
    with socketserver.TCPServer((host, port), RequestHandler) as server:
        print("Server is listening on port", port)
        server.serve_forever()


def input_handling(context, input = None, request_handler = None):
    if context == InputTYPE.INPT_USERNAME:
        while True:
            try:
                data = request_input(request_handler.request, "Choose a username between 3-12 characters: ")

                if data == "EMPTY_STRING":
                    raise EmptyStringError()
                elif hash(data) in Storage.user_objects: # if the user id already exists the name is also already taken
                    raise NameTakenError()
                elif len(data) < 3 or len(data) > 12:
                    raise StringLengthError()
                elif ' ' in data:
                    raise IllegalCharacterError()
                print(f"Username chosen: {data}")
                send_data(request_handler.request, (f"Username chosen: {data}"))
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
            except EmptyStringError:
                send_data(request_handler.request, "ERROR: input cannot be empty")
                continue
            except TypeError:
                return
    
    elif context == InputTYPE.INPT_PASSWORD:
        while True:
            try:
                data = request_input(request_handler.request, "Choose a password between 3-12 character: ")

                if data == "EMPTY_STRING":
                    raise EmptyStringError()
                elif len(data) < 3 or len(data) > 12:
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
            except EmptyStringError:
                send_data(request_handler.request, "ERROR: input cannot be empty")
                continue
            except TypeError:
                return
            
            

if __name__ == "__main__":
    HOST, PORT = "localhost", 8585
    start_server(HOST, PORT)


