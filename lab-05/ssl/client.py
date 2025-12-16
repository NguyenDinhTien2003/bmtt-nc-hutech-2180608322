import socket
import ssl

def main():
    # Tạo socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Tạo SSL Context
    # Vì dùng chứng chỉ tự ký (self-signed) nên ta tắt chế độ xác thực (verify)
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    # Bọc socket
    ssl_socket = context.wrap_socket(client_socket, server_hostname='localhost')

    try:
        ssl_socket.connect(('localhost', 12345))
        print("Đã kết nối an toàn tới Server!")

        while True:
            message = input("Nhập tin nhắn: ")
            if message == 'exit':
                break
            
            ssl_socket.send(message.encode('utf-8'))
            
            # Nhận phản hồi
            data = ssl_socket.recv(1024)
            print(f"Server phản hồi: {data.decode('utf-8')}")

    except Exception as e:
        print(f"Lỗi: {e}")
    finally:
        ssl_socket.close()

if __name__ == "__main__":
    main()