from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.backends import default_backend
import hashlib
import os

# Step 1: User Registration Phase
def user_registration(password):
    print("User Registration Phase:")
    # Generate ECC key pair
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()

    # Derive master key using Honey Encryption
    id = input("Enter your identity (username): ")
    hashed_id = hashlib.sha256(id.encode()).digest()
    master_key = generate_master_key(id, password)

    print("User registration completed.")
    return (private_key, public_key, hashed_id, master_key)

def generate_master_key(id, password):
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=id.encode(),
        backend=default_backend()
    )
    return hkdf.derive(password.encode())

# Step 2: Authentication Phase
def authenticate(server_data, user_private_key, master_key):
    print("\nAuthentication Phase:")
    # Extract server data
    B_i, hashed_id = server_data

    # Generate a random challenge
    c = os.urandom(16)
    print("Generated Challenge:", c.hex())

    # Encrypt the challenge using Honey Encryption
    encrypted_challenge = encrypt_challenge(c, user_private_key, master_key)

    print("Challenge sent to server.")
    return (encrypted_challenge, c)

def encrypt_challenge(challenge, private_key, master_key):
    # Placeholder for encryption using Honey Encryption
    return challenge

def decrypt_challenge(encrypted_challenge, private_key, master_key):
    # Placeholder for decryption using Honey Encryption
    return encrypted_challenge

# Step 3: Password Change Phase
def change_password(password, user_id):
    print("\nPassword Change Phase:")
    # Derive new master key using Honey Encryption
    new_master_key = generate_master_key(user_id, password)

    print("Password changed successfully.")
    return new_master_key

# Placeholder function for response generation
def generate_response(decrypted_challenge):
    # Placeholder for response generation
    return decrypted_challenge[::-1]  # Just a dummy response for demonstration

# Placeholder function for server-side verification
def verify_response(response, expected_challenge):
    # Placeholder for server-side verification
    return response == expected_challenge

# Example usage
# User Registration Phase
password = "password123"
user_private_key, user_public_key, hashed_id, master_key = user_registration(password)

# Server stores user data (public key and hashed id)
server_data = (user_public_key, hashed_id)

# Authentication Phase
encrypted_challenge, challenge = authenticate(server_data, user_private_key, master_key)

# User decrypts the challenge and responds with a fuzzy response
decrypted_challenge = decrypt_challenge(encrypted_challenge, user_private_key, master_key)
response = generate_response(decrypted_challenge)  # Placeholder for response generation
print("Decrypted Challenge:", decrypted_challenge.hex())
print("Generated Response:", response.hex())

# Server verifies the response and grants authentication
if verify_response(response, challenge):
    print("Authentication successful.")
else:
    print("Authentication failed.")

# Password Change Phase
new_password = "newpassword456"
new_master_key = change_password(new_password, hashed_id)
print("New Master Key:", new_master_key.hex())
# Server updates the stored master key for the user with the new one
master_key = new_master_key
_