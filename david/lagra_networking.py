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

def request_input(s, message):
    try:
        send_data(s, "REQUEST_INPUT")
        if receive_data(s) == "RECEIPT":
            send_data(s, message)
            user_input = receive_data(s)
            return user_input
    except Exception as e:
        print(f"Error receiving data: {e}")

def return_input(s):
    try:
        if (receive_data(s) == "REQUEST_INPUT"):
            send_data(s, "RECEIPT")
            user_input = str(input(receive_data(s)))
            send_data(s, user_input)
    except Exception as e:
        print(f"Error receiving data: {e}")