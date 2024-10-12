import socket
from lagra_networking import send_data, receive_data, return_input

def waiting_for_response(s):
    """
    want to fix logic later, but keeping it like this for now
    """
    while True:
        return_input(s)
        data = receive_data(s)
        if (data == "RETURN"):
            return

def main():
    HOST, PORT = "localhost", 8585
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        while True:
            user_input = input("('1') log in, ('2') create an account (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            elif user_input == '1':
                send_data(s, "LOGIN")
                waiting_for_response(s)
            elif user_input == '2':
                send_data(s, "CREATE_USER")
                waiting_for_response(s)


if __name__ == "__main__":
    main()


