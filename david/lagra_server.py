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
    shared_storage = ["potato", "apple", "juice", "orange"]
    def __init__(self):
        self.storage = ["pineapple", "rectangle", "square", "apron"]
    def transfer_to_personal(self, item):
        item = item.lower()
        if item not in Storage.shared_storage:
            return 1
        elif item in Storage.shared_storage and item not in self.storage:
            Storage.shared_storage.remove(item)
            self.storage.append(item)
            return 0
        elif item in self.storage:
            return 3
    def transfer_to_shared(self, item):
        item = item.lower()
        if item not in self.storage:
            return 1
        elif item in self.storage and item not in Storage.shared_storage:
            self.storage.remove(item)
            Storage.shared_storage.append(item)
            return 0
        elif item in Storage.shared_storage:
            return 3
        

def in_session(request_handler, user_object):
    while True:
        try:
            data = receive_data(request_handler.request)
            if data == None :
                return
            elif data == "FETCH_SS":
                print(f"{user_object.username} is fetching shared storage")
                send_data(request_handler.request, f"The shared storage contains the following {Storage.shared_storage}")
            elif data == "FETCH_PS":
                print(f"{user_object.username} fetching personal storage")
                send_data(request_handler.request, f"{user_object.username}, you have {user_object.personal_storage.storage} in your personal storage")
            elif data == "TAKE_SS":
                send_data(request_handler.request, f"The shared storage contains the following {Storage.shared_storage}")
                user_input = request_input(request_handler.request, "What item would you like to take? ")
                w = user_object.personal_storage.transfer_to_personal(user_input)
                if w == 0:
                    print(f"{user_object.username} moved {user_input} from shared storage to personal storage")
                    send_data(request_handler.request, f"You moved {user_input} to your personal storage")
                elif w == 1:
                    print(f"{user_object.username} tried to move an item from shared storage, but failed")
                    send_data(request_handler.request, f"{user_input} does not exist in the shared storage")
                elif w == 3:
                    print(f"{user_object.username} tried to move an item to personal storage, but personal storage already contains it")
                    send_data(request_handler.request, f"{user_input} already exists in your personal storage")
            elif data == "MOVE_PS":
                send_data(request_handler.request, f"Your personal storage contains the following {user_object.personal_storage.storage}")
                user_input = request_input(request_handler.request, "What item would you like to move? ")
                w = user_object.personal_storage.transfer_to_shared(user_input)
                if w == 0:
                    print(f"{user_object.username} moved {user_input} from personal storage to shared storage")
                    send_data(request_handler.request, f"You moved {user_input} to the shared storage")
                elif w == 1:
                    print(f"{user_object.username} tried to move an item from personal storage, but failed")
                    send_data(request_handler.request, f"{user_input} does not exist in your personal storage")
                elif w == 3:
                    print(f"{user_object.username} tried to move an item to shared storage, but shared storage already contains it")
                    send_data(request_handler.request, f"{user_input} already exists in the shared storage")
        except Exception as e:
            print(f"ERROR: {e}")
            
                


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
            data = receive_data(self.request, 1024)
            if data:
                print(f"Received: {data}")
                self.process_request(data)
            elif data == None:
                print("Client disconnected")
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
            if data == None:
                return
            if data == "EMPTY_STRING":
                raise EmptyStringError()
            user_id = hash(data)
            if user_id in Storage.user_objects:
                user_object = Storage.user_objects[user_id]

                send_data(request_handler.request, "Accepted")
                data = request_input(request_handler.request, "Enter password: ")
                if data == None:
                    return
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


def start_server(host, port):
    with socketserver.TCPServer((host, port), RequestHandler) as server:
        print("Server is listening on port", port)
        server.serve_forever()


def input_handling(context, input = None, request_handler = None):
    if context == InputTYPE.INPT_USERNAME:
        while True:
            try:
                data = request_input(request_handler.request, "Choose a username between 3-12 characters: ")
                if data == None:
                    return
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
                if data == None or data.lower() == "exit":
                    return
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


