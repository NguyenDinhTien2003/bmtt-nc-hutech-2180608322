import sys
from PIL import Image

def encode_image(image_path, message):
    img = Image.open(image_path)
    img = img.convert('RGB') 
    width, height = img.size
    
    # Thêm ký tự kết thúc chuỗi để biết khi nào dừng giải mã
    message += '\0'
    
    # Chuyển tin nhắn sang dạng nhị phân (binary)
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    
    data_index = 0
    img_data = list(img.getdata())
    
    new_img_data = []
    
    for pixel in img_data:
        # Nếu đã giấu hết tin nhắn thì giữ nguyên pixel còn lại
        if data_index >= len(binary_message):
            new_img_data.append(pixel)
            continue
            
        r, g, b = pixel # Lấy giá trị màu Red, Green, Blue
        
        # Giấu bit tin nhắn vào bit cuối cùng của màu Red
        if data_index < len(binary_message):
            r = (r & ~1) | int(binary_message[data_index])
            data_index += 1
            
        # Giấu bit tin nhắn vào bit cuối cùng của màu Green
        if data_index < len(binary_message):
            g = (g & ~1) | int(binary_message[data_index])
            data_index += 1
            
        # Giấu bit tin nhắn vào bit cuối cùng của màu Blue
        if data_index < len(binary_message):
            b = (b & ~1) | int(binary_message[data_index])
            data_index += 1
            
        new_img_data.append((r, g, b))
        
    # Tạo ảnh mới từ dữ liệu đã chỉnh sửa
    new_img = Image.new(img.mode, img.size)
    new_img.putdata(new_img_data)
    
    encoded_image_path = "encoded_image.png"
    new_img.save(encoded_image_path)
    print(f"Steganography complete. Encoded image saved as: {encoded_image_path}")

def main():
    if len(sys.argv) < 3:
        print("Usage: python encrypt.py <image_path> <message>")
        return
        
    image_path = sys.argv[1]
    message = sys.argv[2] # Tin nhắn lấy từ tham số dòng lệnh
    
    encode_image(image_path, message)

if __name__ == "__main__":
    main()
