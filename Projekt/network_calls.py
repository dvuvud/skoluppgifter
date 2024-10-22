import socket
import json

def send_data(socket, message):
    """
    Sending data between client and server
    """
    try:
        if type(message) is str and message == "":
            socket.sendall(json.dumps('EMPTY_STRING').encode('utf-8'))
            return
        socket.sendall(json.dumps(message).encode('utf-8')) # encrypt after the json dump
    except Exception as e:
        print(f"Error sending data: {e}")


def receive_data(socket, buffer_size=1024):
    """
    Receiving data between client and server
    """
    try:
        data = json.loads(socket.recv(buffer_size).decode('utf-8')) # return to original format
        if type(data) is str and data == "":
            return 'EMPTY_STRING'
        elif not data:
            return None
        return data
    except Exception as e:
        print(f"Error receiving data: {e}")


def request_input(socket, message, buffer_size=1024):
    """
    Requesting input from the client, only sent by the server
    """
    try:
        send_data(socket, 'INPUT_REQUEST')
        if receive_data(socket, buffer_size) != 'RECEIPT': # receipt used to ensure the client doesnt read both the message and INPUT_REQUEST at once
            print("Failed to get receipt")
            return
        send_data(socket, message)
        client_input = receive_data(socket, buffer_size)
        return client_input
    except Exception as e:
        print(f"Error receiving input: {e}")


def send_input(socket, buffer_size=1024):
    """
    Sending input to server, always needs to be combined with 'request_input() from the server
    """
    try:
        if receive_data(socket, buffer_size) != 'INPUT_REQUEST':
            print("Failure sending input")
            return
        send_data(socket, 'RECEIPT')
        input_message = input(receive_data(socket))
        send_data(socket, input_message)
    except Exception as e:
        print(f"Error sending input: {e}")


def receive_chat(s, buffer_size=1024):
    """
    receiving chats from the server
    """
    data = receive_data(s, buffer_size)
    if data == None:
        return data
    if type(data) != dict:
        return 'WRONG_TYPE'
    return data