from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key

def generate_keys():
    # generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    # serialize private key in .PEM format, so that it can be stored to file
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption() # private key will not be encrypted locally for now, so no password is required
    )

    with open('keys\\private_key.pem', 'wb') as f:
        f.write(private_pem)

        public_key = private_key.public_key()

    # generate public key and store to file in PEM-format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('keys\\public_key.pem', 'wb') as f:
        f.write(public_pem)

    return private_key, public_pem

def load_keys():
    with open('keys\\private_key.pem', 'rb') as f:
        private_pem = f.read()

    with open('keys\\public_key.pem', 'rb') as f:
        public_pem = f.read()

    # convert from PEM to object
    private_key = load_pem_private_key(
        private_pem, 
        password=None,
        backend=default_backend()
    )

    # convert from PEM to object
    public_key = load_pem_public_key(public_pem)

    return private_key, public_key

def encrypt_message(message, public_key):
    # encrypt message using given public key
    encrypted_message = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            # these settings should be default / best practice
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
        
    return encrypted_message

def decrypt_message(encrypted_message, private_key):
    decrypted_message = private_key.decrypt(
        encrypted_message,
        padding.OAEP(
            # these settings should be default / best practice
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    return decrypted_message.decode('utf-8')

def test():
    private_key, public_key = load_keys()

    encrypted_message = encrypt_message("Hejsan", public_key)
    decrypted_message = decrypt_message(encrypted_message, private_key)

    print(decrypted_message)