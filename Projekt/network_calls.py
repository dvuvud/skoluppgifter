import socket

def send_data(socket, message):
    """
    Sending data between client and server
    """
    try:
        if message == "":
            print("Can't send empty string")
            return
        socket.sendall(message) # antaget att datan krypteras i en annan funktion därav skickar jag utan att kryptera
    except Exception as e:
        print("Error sending data: {e}")


def receive_data(socket, buffer_size=1024):
    """
    Receiving data between client and server
    """
    try:
        return s.recv(buffer_size)
    except Exception as e:
        print("Error receiving data: {e}")