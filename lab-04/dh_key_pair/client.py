from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives import serialization

def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key

def derive_shared_secret(private_key, server_public_key):
    shared_key = private_key.exchange(server_public_key)
    return shared_key

def main():
    # Bước 1: Đọc Public Key của Server từ file
    try:
        with open("server_public_key.pem", "rb") as f:
            server_public_key = serialization.load_pem_public_key(f.read())
    except FileNotFoundError:
        print("Không tìm thấy file khóa của server. Hãy chạy server.py trước!")
        return

    # Bước 2: Lấy tham số DH từ khóa của server
    parameters = server_public_key.parameters()

    # Bước 3: Tạo cặp khóa cho Client dựa trên tham số đó
    private_key, public_key = generate_client_key_pair(parameters)
    
    # Bước 4: Tính toán bí mật chung (Shared Secret)
    shared_secret = derive_shared_secret(private_key, server_public_key)
    
    print("Shared Secret created successfully!")
    print(f"Shared Secret (Hex): {shared_secret.hex()}")

if __name__ == "__main__":
    main()