import socket
import threading


class UndefinedInputError(Exception):
    pass


SERVER_HOST = 'localhost'
SERVER_PORT = 8585

def start_client(): # den hör funktionen körs en gång när man kopplas till servern
    # set up connection to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))

    print("Connected to the server.")
    bHasConnection = True
    while bHasConnection:
        if on_connect(s) == 1: # 0 -> success, 1 -> failure
            print("Connection lost to host")
            break



if __name__ == "__main__":
    start_client()


def on_connect(s): # första funktionen som körs när klienten kopplats till servern
    while True:
        try:
            user_input = input("'1' to create a new account, '2' to login to an existing account (or 'exit' to quit)")
            if user_input == '1':
                create_account(s)
                return 0
            elif user_input == '2':
                login(s)
                return 0
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
    logic for creating an account
    """


def login(s):
    """
    logic for logging in
    """