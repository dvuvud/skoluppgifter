import socket
import threading
from My_cryptography.my_cryptography import load_keys, encrypt_message, decrypt_message
from network_calls import send_data, receive_data, send_input, receive_chat
from record_inputs import take_input, pressed_keys
import time
from server_backend import create_chat_message

class UndefinedInputError(Exception):
    pass


SERVER_HOST = 'localhost'
SERVER_PORT = 8585
bShouldLog = True
lock = threading.Lock()
input_prompt = ''

def start_client(): # function is called when client connects to server
    # set up connection to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))

    print("Connected to the server.")
    
    bHasConnection = True
    while bHasConnection:
        if on_connect(s) == 1: # 0 -> success, 1 -> failure
            print("Connection to host lost")
            break
        """
        Logic to join chat room
        """
        logged_in(s)
            
        


def on_connect(s): # this function is called after the client connects to the server
    while True:
        try:
            user_input = input("'1' to create a new account, '2' to login to an existing account (or 'exit' to quit): ")
            if user_input == '1':
                if create_account(s) == 0: # if function is successful, return 0, else continue until user exits or function is successful
                    continue
            elif user_input == '2':
                if login(s) == 0: # if function is successful, return 0, else continue until user exits or function is successful
                    return 0
                continue 
            elif user_input == 'exit':
                return 1
            else:
                raise UndefinedInputError()
        except UndefinedInputError:
            print("Input is undefined")
        except Exception as e:
            print(f"ERROR: {e}")


def create_account(s):
    """
    logic for creating an account, return 0 for success, 1 for failure
    """
    send_data(s, "CREATE_ACCOUNT")
    send_input(s)
    ServerResponse = receive_data(s)
    if ServerResponse['outcome'] == 'FAILURE':
        print(ServerResponse['message'])
        return 1
    print(ServerResponse['message'])
    send_input(s)
    ServerResponse = receive_data(s)
    if ServerResponse['outcome'] == 'FAILURE':
        print(ServerResponse['message'])
        return 1
    print(ServerResponse['message'])
    return 0


def login(s):
    """
    logic for logging in, return 0 for success, 1 for failure
    """
    send_data(s, "LOGIN")
    send_input(s)
    send_input(s)
    ServerResponse = receive_data(s)
    if ServerResponse['outcome'] == 'FAILURE':
        print(ServerResponse['message'])
        return 1
    print(ServerResponse['message'])
    return 0



"""
While in the chatroom
"""
def chatroom(s):
    try:
        user_input = str(input("Enter '1' to join chatroom or 'return' to log out (or 'exit' to quit): "))
        if user_input.lower() == 'return':
            send_data('LOG_OUT')
            print(receive_data(s))
            return -1
        elif user_input.lower() == 'exit':
            return 0
        elif user_input != '1':
            print("Input wasn't recognized")
            return 1
    except Exception as e:
        print("ERROR: {e}")
        return 1

    """
    Logic for joining, and being in the chatroom
    """

    send_data(s, 'JOIN_CHAT')
    data = receive_data(s) # message returned from server confirming we successfully joined the chatroom
    if data != "You entered the chatroom":
        return 1
    print(data)
    bShouldLog = True
    chatlog_thread = threading.Thread(target=chatlogging, args=(s,))
    chatlog_thread.daemon = True
    chatlog_thread.start()

    """
    sending chat messages
    """
    while True:
        
        if send_chat(s) == 1:
            print("Failure sending messages, leaving chatroom")
            bShouldLog = False
            return 1


"""
Sending chat messages and recording input
"""
def send_chat(s):
    with lock:
        if receive_data(s) != 'RECEIVING_CHAT':
            return 1
        send_data(s, 'SENDING_CHAT')
        input_prompt = receive_data(s)
    try:
        print(input_prompt, end='')
        chat_message = take_input() # recording inputs
        send_data(s, create_chat_message(None, chat_message))
    except Exception as e:
        print(f"Failure sending chat messages: {e}")
    

"""
Logging all incoming chat messages
"""
def chatlogging(s):
    while bShouldLog:
        time.sleep(1)
        with lock:  # threading.Lock() locks all other threads of using certain resource at the same time 
            chat_message = receive_chat(s)
            if chat_message == None:
                continue
            """
            Process chat message
            """
            print('\r', end='')
            print("\033[K", end='')
            print(f"{chat_message['timestamp']} - {chat_message['sender']}: {chat_message['message']}")
            print(input_prompt, ''.join(pressed_keys), end='')
            
            


"""
called after logging in to account
"""
def logged_in(s):
    while True:
        outcome = chatroom(s)
        if outcome == 0: # User exiting application
            break
        elif outcome == -1: # User logged out of account
            return
        elif outcome == 1: # Error caused user to leave chatroom
            continue

if __name__ == "__main__":
    start_client()