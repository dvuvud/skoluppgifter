import socket

def send_data(s, message):
    """
    send data to server
    """
    try:
        s.sendall(message.encode("utf-8"))
    except Exception as e:
        print(f"Error sending data: {e}")

def receive_data(s, buffer_size=1024):
    """
    receive data from the server
    """
    try:
        data = s.recv(buffer_size)
        return data.decode("utf-8")
    except Exception as e:
        print(f"Error receiving data: {e}")
        return None
