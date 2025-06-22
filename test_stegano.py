#!/usr/bin/env python3
"""
Test script for the steganography tool
"""

import os
from PIL import Image, ImageDraw, ImageFont
import stegano

def create_test_image(filename="test_image.png", size=(400, 300)):
    """Create a simple test image for steganography testing."""
    # Create a new image with a white background
    img = Image.new('RGB', size, color='white')
    draw = ImageDraw.Draw(img)
    
    # Add some text to make it more interesting
    try:
        # Try to use a default font
        font = ImageFont.load_default()
    except:
        font = None
    
    # Draw some shapes and text
    draw.rectangle([50, 50, 350, 250], outline='blue', width=3)
    draw.ellipse([100, 100, 300, 200], fill='lightblue')
    draw.text((150, 150), "Test Image", fill='black', font=font)
    
    # Save the image
    img.save(filename, 'PNG')
    print(f"Created test image: {filename}")
    return filename

def test_text_steganography():
    """Test text encoding and decoding."""
    print("\n=== Testing Text Steganography ===")
    
    # Create test image
    test_img = create_test_image()
    test_message = "Hello, this is a secret message! 🎉"
    
    try:
        # Encode text
        print(f"Encoding message: '{test_message}'")
        stegano.encode_text_in_image(test_img, test_message, "encoded_text.png")
        print("✓ Text encoded successfully")
        
        # Decode text
        decoded_message = stegano.decode_text_from_image("encoded_text.png")
        print(f"Decoded message: '{decoded_message}'")
        
        # Verify
        if decoded_message == test_message:
            print("✓ Text steganography test PASSED")
        else:
            print("✗ Text steganography test FAILED")
            
    except Exception as e:
        print(f"✗ Text steganography test FAILED: {e}")
    
    finally:
        # Clean up
        for file in [test_img, "encoded_text.png"]:
            if os.path.exists(file):
                os.remove(file)

def test_file_steganography():
    """Test file encoding and decoding."""
    print("\n=== Testing File Steganography ===")
    
    # Create test file
    test_file = "test_file.txt"
    test_content = "This is a test file content.\nIt has multiple lines.\nAnd some special chars: !@#$%^&*()"
    
    with open(test_file, 'w') as f:
        f.write(test_content)
    
    # Create test image
    test_img = create_test_image("test_img_file.png")
    
    try:
        # Encode file
        print(f"Encoding file: {test_file}")
        stegano.encode_file_in_image(test_img, test_file, "encoded_file.png")
        print("✓ File encoded successfully")
        
        # Decode file
        decoded_file = "decoded_file.txt"
        stegano.decode_file_from_image("encoded_file.png", decoded_file)
        print("✓ File decoded successfully")
        
        # Verify
        with open(decoded_file, 'rb') as f:
            decoded_content = f.read()
        orig_bytes = test_content.encode()
        print(f"Original bytes length: {len(orig_bytes)}")
        print(f"Decoded bytes length: {len(decoded_content)}")
        print(f"Original bytes (first 60): {orig_bytes[:60]}")
        print(f"Decoded bytes (first 60): {decoded_content[:60]}")
        # Normalize line endings for comparison
        orig_norm = orig_bytes.replace(b'\n', b'\r\n')
        if decoded_content == orig_bytes or decoded_content == orig_norm:
            print("✓ File steganography test PASSED")
        else:
            print("✗ File steganography test FAILED")
            
    except Exception as e:
        print(f"✗ File steganography test FAILED: {e}")
    
    finally:
        # Clean up
        for file in [test_file, test_img, "encoded_file.png", decoded_file]:
            if os.path.exists(file):
                os.remove(file)

def main():
    """Run all tests."""
    print("Starting Steganography Tool Tests...")
    
    test_text_steganography()
    test_file_steganography()
    
    print("\n=== Test Summary ===")
    print("All tests completed!")

if __name__ == "__main__":
    main() 
