import socket
from lagra_networking import send_data, receive_data, return_input

def create_user(s):
    """
    want to fix logic later, but keeping it like this for now
    """
    while True:
        return_input(s)
        data = receive_data(s)
        print(data)
        if data == "User created":
            break

def login(s):
    while True:
        return_input(s)
        data = receive_data(s)
        print(data)
        if data == "Logged in":
            break
    in_session(s) # as long as player is logged in this will be the active function
    return # as soon as in_session() returns everything goes back to the main() function

def in_session(s):
    print("In session")
    bIsSession = True
    while bIsSession:
        print("Sessioning")


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
                login(s)
            elif user_input == '2':
                send_data(s, "CREATE_USER")
                create_user(s)


if __name__ == "__main__":
    main()


