import socket
import json

def send_data(socket, message):
    """
    Sending data between client and server
    """
    try:
        if message == "":
            print("Can't send empty string")
            return
        socket.sendall(json.dump(message)) # encrypt after the json dump
    except Exception as e:
        print("Error sending data: {e}")


def receive_data(socket, buffer_size=1024):
    """
    Receiving data between client and server
    """
    try:
        data = s.recv(buffer_size) # decryption
        return json.load(data) # return to original format
    except Exception as e:
        print("Error receiving data: {e}")