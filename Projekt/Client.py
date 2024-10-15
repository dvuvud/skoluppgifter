import socket
import threading
from My_cryptography.my_cryptography import load_keys, encrypt_message, decrypt_message
from network_calls import send_data, receive_data, send_input

class UndefinedInputError(Exception):
    pass


SERVER_HOST = 'localhost'
SERVER_PORT = 8585

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
        


def on_connect(s): # this function is called after the client connects to the server
    while True:
        try:
            user_input = input("'1' to create a new account, '2' to login to an existing account (or 'exit' to quit): ")
            if user_input == '1':
                if create_account(s) == 0: # if function is successful, return 0, else continue until user exits or function is successful
                    return 0
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


if __name__ == "__main__":
    start_client()