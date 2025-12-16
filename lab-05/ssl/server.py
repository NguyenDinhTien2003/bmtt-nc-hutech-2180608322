import socket
import ssl
import threading

# Cấu hình Server
server_address = ('localhost', 12345)

def handle_client(client_socket):
    try:
        print(f"Đã kết nối với: {client_socket.getpeername()}")
        while True:
            # Nhận dữ liệu
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Nhận: {data.decode('utf-8')}")
            
            # Phản hồi lại cho client
            client_socket.send(data)
    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        client_socket.close()

def main():
    # Tạo socket TCP thông thường
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f"Server đang chờ kết nối tại {server_address}...")

    # Tạo SSL Context
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # Lưu ý đường dẫn trỏ vào thư mục certificates bạn vừa tạo
    context.load_cert_chain(certfile='./certificates/server-cert.crt', 
                            keyfile='./certificates/server-key.key')

    while True:
        try:
            client_sock, addr = server_socket.accept()
            # Bọc socket bằng SSL
            ssl_socket = context.wrap_socket(client_sock, server_side=True)
            
            # Tạo luồng xử lý riêng cho client
            client_thread = threading.Thread(target=handle_client, args=(ssl_socket,))
            client_thread.start()
        except Exception as e:
            print(f"Lỗi chấp nhận kết nối: {e}")

if __name__ == "__main__":
    main()