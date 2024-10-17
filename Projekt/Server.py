import socketserver
import server_backend
from network_calls import send_data, receive_data, request_input, receive_chat
from datetime import datetime

HOST, PORT = 'localhost', 8585

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, *args, **kwargs):
        self.currentuser = None
        super().__init__(*args, **kwargs)
    def handle(self): # den här funktionen körs en gång när servern blivit kopplad till en klient
        print(f"Connection from {self.client_address}")
        while True:
            try:
                # Receive data
                data = receive_data(self.request)
                if not data:
                    print(f"Client {self.client_address} disconnected.")
                    break
                elif data == 'LOGIN':
                    login(self)
                    continue
                elif data == 'CREATE_ACCOUNT':
                    create_account(self)
                    continue
                elif data == 'JOIN_CHAT':
                    """
                    Logic to send user to chatroom
                    """
                    chatroom(self)
                
            except ConnectionResetError:
                print(f"Connection with {self.client_address} lost.")
                break
            except Exception as e:
                print(f"Error occured: {e}")


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    def __init__(self, *args, **kwargs): # called when the server is initialized
        print("Server is initialized")
        super().__init__(*args, **kwargs)

    def server_activate(self): # called on server startup, can accept new connections (inherited from TCPServer)
        super().server_activate() 
        print("Server is now active and ready for connections.")

    def finish_request(self, request, client_address): # called when a client connection is accepted (inherited from TCPServer)
        print(f"Client connected: {client_address}")  
        super().finish_request(request, client_address)  


def start_server():
    with ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler) as server:
        print(f"Server is listening on {HOST} : {PORT}")
        server.serve_forever()


def create_account(s):
    """
    Choosing username
    """
    username = request_input(s.request, "Enter username (3-12 characters): ")
    if username == 'EMPTY_STRING':
        send_data(s.request, server_backend.create_server_response('FAILURE', "Username cannot be an empty string"))
        print("Client tried choosing an empty string as a username")
        return
    elif username in server_backend.users:
        send_data(s.request, server_backend.create_server_response('FAILURE', "Username already in user"))
        print("Client tried choosing a username already in use")
        return
    elif " " in username:
        send_data(s.request, server_backend.create_server_response('FAILURE', "Username cannot contain spaces"))
        print("Client tried choosing a username containing spaces")
        return
    elif len(username) > 12 or len(username) < 3:
        send_data(s.request, server_backend.create_server_response('FAILURE', "Username length is out of scope"))
        print("Client tried choosing a username out of scope")
        return
    send_data(s.request, server_backend.create_server_response('SUCCESS', 'Username accepted'))

    """
    Choosing password
    """
    password = request_input(s.request, "Enter password (3-12 characters): ")
    if password == 'EMPTY_STRING':
        send_data(s.request, server_backend.create_server_response('FAILURE', "password cannot be an empty string"))
        print("Client tried choosing an empty string as a password")
        return
    elif password == username:
        send_data(s.request, server_backend.create_server_response('FAILURE', "Password can't be same as username"))
        print("Client tried choosing a password that was the same as their username")
        return
    elif " " in password:
        send_data(s.request, server_backend.create_server_response('FAILURE', "password cannot contain spaces"))
        print("Client tried choosing a password containing spaces")
        return
    elif len(password) > 12 or len(password) < 3:
        send_data(s.request, server_backend.create_server_response('FAILURE', "password length is out of scope"))
        print("Client tried choosing a username out of scope")
        return
    new_user = server_backend.User(username, password)
    send_data(s.request, server_backend.create_server_response('SUCCESS', 'Account created'))
    print(f"User {username} created by client {s.client_address}")


def login(s):
    username = request_input(s.request, "Enter username: ")
    password = request_input(s.request, "Enter password: ")
    if username not in server_backend.users or server_backend.users[username].password != password:
        send_data(s.request, server_backend.create_server_response('FAILURE', "Username and password combination doesn't exist"))
        return
    s.currentuser = server_backend.users[username]
    send_data(s.request, server_backend.create_server_response('SUCCESS', f"Successfully logged in as {username}"))
    print(f"Client {s.client_address} logged in as {username}")
    return

"""
Whenever player joins chatroom
"""
def chatroom(s):
    server_backend.request_handlers[s.currentuser.username] = s
    print(f"{s.currentuser.username} entered the chatroom")
    send_data(s.request, "You entered the chatroom")
    while True:
        send_data(s.request, 'RECEIVING_CHAT')
        receipt = receive_data(s.request)
        if receipt != 'SENDING_CHAT':
            continue
        elif receipt == None:
            return
        send_data(s.request, "Enter a chat: ")
        chat_message = receive_chat(s.request)
        if chat_message == None:
            print("Couldn't receive chat message as None")
            continue
        chat_message['sender'] = s.currentuser.username
        now = datetime.now()
        chat_message['timestamp'] = str(now.strftime("%H:%M"))
        for username, request_handler in server_backend.request_handlers.items():
            # print(f"{chat_message['timestamp']} > {chat_message['sender']}: {chat_message['message']}") 
            send_data(request_handler.request, chat_message)




if __name__ == "__main__":
    start_server()