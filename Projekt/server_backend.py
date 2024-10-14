from collections import namedtuple
from datetime import datetime

"""
Fil för att definiera alla klasser och datatyper som ska användas på server/klienten
"""

class User():
    def __init__(self, username, password, public_key):
        self.username = username
        self.password = password
        self.public_key = public_key
        users[self.username] = self

users = {}


now = datetime.now()

current_minute = now.minute
current_second = now.second

ChatMessage = namedtuple('ChatMessage', ['sender', 'message', 'timestamp']) # timestamp fylls i hos klienten och därav sorterar server meddelanderna efter tidsordning