import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 8585

def start_client(): # den hör funktionen körs en gång när man kopplas till servern
    # set up connection to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))

    print("Connected to the server.")
    bHasConnection = True
    while bHasConnection:
        print("Is connected")



if __name__ == "__main__":
    start_client()