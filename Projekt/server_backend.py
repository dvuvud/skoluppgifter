from collections import namedtuple
from datetime import datetime
from network_calls import request_input

"""
Fil för att definiera alla klasser och datatyper som ska användas på server/klienten
"""

class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password
        users[self.username] = self

users = {}
request_handlers = {}

now = datetime.now()

current_minute = now.minute
current_second = now.second
# chatmessage ska egentligen flyttas till klientens sida, men fixar det sen
ChatMessage = namedtuple('ChatMessage', ['sender', 'message', 'timestamp']) # timestamp fylls i hos klienten och därav sorterar server meddelanderna efter tidsordning
ServerResponse = namedtuple('ServerResponse', ['outcome', 'message'])


"""
Har ännu inte bestämt, men det verkar som att det inte går att serializa namedtuples så vi kanske får använda dictionaries istället
Återigen kanske create_chat_message borde ligga på klientens sida, men vi löser det sen
"""
def create_chat_message(p_sender, p_message):
    return {
        'sender' : p_sender,
        'message' : p_message,
        'timestamp' : datetime.now().isoformat()
    }

def create_server_response(p_outcome, p_message):
    return {
        'outcome' : p_outcome,
        'message' : p_message
    }