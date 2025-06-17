from PIL import Image
from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_message(key, message):
    cipher = Fernet(key)
    encrypted = cipher.encrypt(message.encode())
    return encrypted

def decrypt_message(key, encrypted_message):
    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted_message).decode()
    return decrypted

def embed_message_in_image(image, message_bytes):
    data = list(image.getdata())
    binary_message = ''.join(format(byte, '08b') for byte in message_bytes) + '1111111111111110'  # EOF marker

    if len(binary_message) > len(data) * 3:
        raise ValueError("Message too long to hide in this image.")

    new_data = []
    bit_index = 0

    for pixel in data:
        r, g, b = pixel
        if bit_index < len(binary_message):
            r = (r & ~1) | int(binary_message[bit_index])
            bit_index += 1
        if bit_index < len(binary_message):
            g = (g & ~1) | int(binary_message[bit_index])
            bit_index += 1
        if bit_index < len(binary_message):
            b = (b & ~1) | int(binary_message[bit_index])
            bit_index += 1
        new_data.append((r, g, b))

    new_data.extend(data[len(new_data):])
    stego_image = Image.new(image.mode, image.size)
    stego_image.putdata(new_data)
    return stego_image

def extract_message_from_image(image):
    data = list(image.getdata())
    binary_data = ''
    for pixel in data:
        for color in pixel[:3]:
            binary_data += str(color & 1)

    all_bytes = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    message_bytes = bytearray()
    for byte in all_bytes:
        if byte == '11111110':  # EOF marker
            break
        message_bytes.append(int(byte, 2))
    return bytes(message_bytes)

def main():
    print("=== Secure Image Steganography ===")

    choice = input("Do you want to (E)mbed or (D)ecrypt a message? ").strip().upper()

    if choice == 'E':
        # Embed message
        key = generate_key()
        print(f"Encryption Key (Save this to decrypt message): {key.decode()}")

        image_path = input("Enter path to cover image (PNG recommended): ").strip()
        image = Image.open(image_path).convert('RGB')

        secret_message = input("Enter the secret message to hide: ").strip()
        encrypted_message = encrypt_message(key, secret_message)

        stego_image = embed_message_in_image(image, encrypted_message)
        output_path = input("Enter output image filename (e.g. stego.png): ").strip()
        stego_image.save(output_path)
        print(f"Message embedded and saved to {output_path}")

    elif choice == 'D':
        # Decrypt message
        image_path = input("Enter path to stego image: ").strip()
        image = Image.open(image_path).convert('RGB')

        key_input = input("Enter the encryption key: ").strip().encode()
        encrypted_message = extract_message_from_image(image)

        try:
            decrypted_message = decrypt_message(key_input, encrypted_message)
            print(f"Decrypted message: {decrypted_message}")
        except Exception as e:
            print("Decryption failed. Check the key and image.")

    else:
        print("Invalid choice. Please enter E or D.")

if __name__ == "__main__":
    main()
