import base64

def main():
    try:
        # Đọc nội dung đã mã hóa từ file
        with open("data.txt", "r") as file:
            encoded_string = file.read().strip()
        
        # Giải mã từ Base64 về bytes rồi về chuỗi
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')

        print("Chuỗi sau khi giải mã:", decoded_string)
    except Exception as e:
        print(f"Lỗi: {e}")

if __name__ == "__main__":
    main()