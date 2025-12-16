import sys
from PIL import Image

def decode_image(encoded_image_path):
    img = Image.open(encoded_image_path)
    width, height = img.size
    
    binary_message = ""
    
    for pixel in list(img.getdata()):
        r, g, b = pixel
        
        # Lấy bit cuối cùng của từng màu
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)
        
    # Chuyển đổi từ nhị phân sang ký tự
    message = ""
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) < 8:
            break
        
        char = chr(int(byte, 2))
        
        # Nếu gặp ký tự kết thúc '\0' thì dừng lại
        if char == '\0':
            break
            
        message += char
        
    return message

def main():
    if len(sys.argv) < 2:
        print("Usage: python decrypt.py <encoded_image_path>")
        return
        
    encoded_image_path = sys.argv[1]
    decoded_message = decode_image(encoded_image_path)
    
    print(f"Decoded message: {decoded_message}")

if __name__ == "__main__":
    main()