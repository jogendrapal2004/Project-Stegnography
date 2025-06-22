# Project-Stegnography Tool for Image/File Hiding
A Python GUI tool to hide and extract text or files inside images using steganography (LSB method).

Features
Hide text or files inside PNG/BMP images
Extract hidden data from images
Optional message encryption
Drag-and-drop GUI (Tkinter)
Supports PNG, BMP formats
Requirements
Python 3.x
Pillow
stepic
tkinter (usually included with Python)
Setup
pip install -r requirements.txt
Usage
Run the tool:
python main.py
Use the GUI to:
Load an image (drag-and-drop or file dialog)
Enter a message or select a file to hide
Embed the message/file into the image
Extract hidden data from a stego image
Project Structure
main.py        # Entry point
stegano.py     # Steganography logic
gui.py         # GUI code
requirements.txt
README.md
assets/        # (Optional) Sample images
License
MIT
