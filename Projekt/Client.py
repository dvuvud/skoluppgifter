import socket
import threading
from Cryptography.cryptography import load_keys, encrypt_message, decrypt_message
from network_calls import send_data, receive_data

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
        


if __name__ == "__main__":
    start_client()


def on_connect(s): # this function is called after the client connects to the server
    while True:
        try:
            user_input = input("'1' to create a new account, '2' to login to an existing account (or 'exit' to quit)")
            if user_input == '1':
                return create_account(s)
            elif user_input == '2':
                return login(s)
            elif user_input == 'exit':
                return 1
            else:
                raise UndefinedInputError()
        except UndefinedInputError:
            print("Input is undefined")
        except Exception as e:
            print("ERROR: {e}")


def create_account(s):
    """
    logic for creating an account, return 0 for success, 1 for failure
    """
    send_data(s, "CREAT_ACCOUNT")


def login(s):
    """
    logic for logging in, return 0 for success, 1 for failure
    """
    send_data(s, "LOGIN")