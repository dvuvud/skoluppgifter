import socket
from lagra_networking import send_data, receive_data

def main():
    HOST, PORT = "localhost", 8585
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        
        while True:
            user_input = input("Enter a command (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break

            send_data(s, user_input)
            response = receive_data(s)
            if response:
                print(f"Server response: {response}")

if __name__ == "__main__":
    main()
