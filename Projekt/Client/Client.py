import socket, threading
import threading


SERVER_HOST = 'server ip'
SERVER_PORT = 8585

def start_client():
    # set up connection to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, SERVER_PORT))

    print("Connected to the server.")


if __name__ == "__main__":
    start_client()