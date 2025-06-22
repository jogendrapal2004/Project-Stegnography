from PIL import Image
import stepic
import os
import base64

# --- Text <-> Binary ---
def text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bin_to_text(bin_str):
    chars = [bin_str[i:i+8] for i in range(0, len(bin_str), 8)]
    return ''.join([chr(int(b, 2)) for b in chars if len(b) == 8])

# --- LSB Encode/Decode for Text ---
def encode_text_in_image(image_path, message, output_path):
    """Encode text message into an image using LSB steganography."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        img = Image.open(image_path)
        
        # Check if image is in a supported format
        if img.format not in ['PNG', 'BMP']:
            raise ValueError(f"Unsupported image format: {img.format}. Please use PNG or BMP.")
        
        # Check if message is not empty
        if not message:
            raise ValueError("Message cannot be empty")
        
        # Check if image is large enough for the message
        img_size = img.size[0] * img.size[1]
        message_size = len(message.encode('utf-8'))
        if message_size > img_size // 8:  # Rough estimate
            raise ValueError("Message too large for this image. Try a larger image or shorter message.")
        
        encoded = stepic.encode(img, message.encode('utf-8'))
        encoded.save(output_path)
        
    except Exception as e:
        raise Exception(f"Failed to encode text: {str(e)}")

def decode_text_from_image(image_path):
    """Decode text message from an image using LSB steganography."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        img = Image.open(image_path)
        message = stepic.decode(img)
        
        if not message:
            raise ValueError("No hidden message found in this image")
        
        # stepic.decode may return str or bytes depending on version
        if isinstance(message, bytes):
            return message.decode('utf-8')
        else:
            return message
        
    except Exception as e:
        raise Exception(f"Failed to decode text: {str(e)}")

# --- LSB Encode/Decode for Files ---
def encode_file_in_image(image_path, file_path, output_path):
    """Encode a file into an image using LSB steganography (base64)."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File to hide not found: {file_path}")
        
        # Read the file to hide
        with open(file_path, 'rb') as f:
            data = f.read()
        
        if not data:
            raise ValueError("File to hide is empty")
        
        # Encode data as base64 string
        b64_data = base64.b64encode(data)
        
        img = Image.open(image_path)
        
        # Check if image is in a supported format
        if img.format not in ['PNG', 'BMP']:
            raise ValueError(f"Unsupported image format: {img.format}. Please use PNG or BMP.")
        
        # Check if image is large enough for the file
        img_size = img.size[0] * img.size[1]
        file_size = len(b64_data)
        if file_size > img_size // 8:  # Rough estimate
            raise ValueError("File too large for this image. Try a larger image or smaller file.")
        
        encoded = stepic.encode(img, b64_data)
        encoded.save(output_path)
        
    except Exception as e:
        raise Exception(f"Failed to encode file: {str(e)}")

def decode_file_from_image(image_path, output_file):
    """Decode a file from an image using LSB steganography (base64)."""
    try:
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        img = Image.open(image_path)
        b64_data = stepic.decode(img)
        
        if not b64_data:
            raise ValueError("No hidden file found in this image")
        
        # Decode from base64
        if isinstance(b64_data, str):
            b64_data = b64_data.encode('utf-8')
        data = base64.b64decode(b64_data)
        
        with open(output_file, 'wb') as f:
            f.write(data)
            
    except Exception as e:
        raise Exception(f"Failed to decode file: {str(e)}")

# --- Optional: Encryption/Decryption Placeholder ---
def encrypt_message(message, password):
    # Placeholder for encryption logic
    return message

def decrypt_message(message, password):
    # Placeholder for decryption logic
    return message 
