from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import socket
import threading

# Initialize server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 12345))
server_socket.listen(5)

# Generate RSA key pair (Server doesn't strictly use this for handshake in this logic but good to have)
server_key = RSA.generate(2048)

# List of connected clients
clients = []

# Function to encrypt message (AES)
def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext

# Function to decrypt message (AES)
def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()

# Function to handle client connection
def handle_client(client_socket, client_address):
    print(f"Connected with {client_address}")
    
    # Send server's public key to client (Optional in this flow, but client expects handshake)
    # Receive client's public RSA key
    client_received_key = RSA.import_key(client_socket.recv(2048))
    
    # Generate AES key for this session
    aes_key = get_random_bytes(16)
    
    # Encrypt the AES key using the client's public RSA key
    cipher_rsa = PKCS1_OAEP.new(client_received_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    client_socket.send(encrypted_aes_key)
    
    # Add client to list
    clients.append(client_socket)
    
    while True:
        try:
            # Receive encrypted message from client
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                break
                
            # Decrypt to show on server console
            decrypted_message = decrypt_message(aes_key, encrypted_message)
            print(f"Received from {client_address}: {decrypted_message}")
            
            # Broadcast message to other clients
            # (Lưu ý: Trong ảnh Lab, server gửi thẳng encrypted_message. 
            # Nếu các client có key khác nhau thì code này chỉ demo luồng tin, 
            # client khác nhận sẽ không giải mã được nếu không dùng chung AES key)
            for client in clients:
                if client != client_socket:
                    client.send(encrypted_message)
                    
        except:
            break
            
    clients.remove(client_socket)
    client_socket.close()
    print(f"Connection with {client_address} closed")

# Main loop to accept clients
print("Server is listening...")
while True:
    client_packet, client_address = server_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(client_packet, client_address))
    client_thread.start()