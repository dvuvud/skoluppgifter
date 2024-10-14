"""
Fil för att definiera alla klasser som ska användas i servern
"""

class User():
    def __init__(self, username, password):
        self.username = username
        self.password = password