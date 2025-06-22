import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import ImageTk, Image
import os
import stegano

class SteganoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('Steganography Tool')
        self.root.geometry('600x500')
        self.image_path = None
        self.create_widgets()

    def create_widgets(self):
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=20, pady=20, fill='both', expand=True)
        
        # Title
        title_label = tk.Label(main_frame, text='Steganography Tool', font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # Image display area
        self.img_label = tk.Label(main_frame, text='Click to load image\n(PNG/BMP formats)', 
                                 width=40, height=10, relief='sunken', bg='lightgray')
        self.img_label.pack(pady=10)
        self.img_label.bind('<Button-1>', self.load_image)

        # Load image button
        load_btn = tk.Button(main_frame, text='Load Image', command=self.load_image)
        load_btn.pack(pady=5)

        # Message area
        msg_frame = tk.Frame(main_frame)
        msg_frame.pack(pady=10, fill='x')
        
        msg_label = tk.Label(msg_frame, text='Message to hide:')
        msg_label.pack(anchor='w')
        
        self.message_entry = tk.Text(msg_frame, height=4, width=50)
        self.message_entry.pack(pady=5, fill='x')
        self.message_entry.insert('1.0', 'Enter message to hide...')

        # Buttons frame
        btn_frame = tk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        self.embed_btn = tk.Button(btn_frame, text='Embed Text', command=self.embed_text, width=15)
        self.embed_btn.pack(side='left', padx=5)

        self.extract_btn = tk.Button(btn_frame, text='Extract Text', command=self.extract_text, width=15)
        self.extract_btn.pack(side='left', padx=5)

        # File buttons frame
        file_btn_frame = tk.Frame(main_frame)
        file_btn_frame.pack(pady=5)
        
        self.file_btn = tk.Button(file_btn_frame, text='Embed File', command=self.embed_file, width=15)
        self.file_btn.pack(side='left', padx=5)

        self.extract_file_btn = tk.Button(file_btn_frame, text='Extract File', command=self.extract_file, width=15)
        self.extract_file_btn.pack(side='left', padx=5)

    def load_image(self, event=None):
        path = filedialog.askopenfilename(
            title='Select Image',
            filetypes=[('Image Files', '*.png *.bmp'), ('All Files', '*.*')]
        )
        if path:
            try:
                self.image_path = path
                img = Image.open(path)
                img.thumbnail((200, 200))
                self.tk_img = ImageTk.PhotoImage(img)
                self.img_label.config(image=self.tk_img, text='')
            except Exception as e:
                messagebox.showerror('Error', f'Failed to load image: {str(e)}')

    def embed_text(self):
        if not self.image_path:
            messagebox.showerror('Error', 'No image loaded!')
            return
        message = self.message_entry.get('1.0', 'end').strip()
        if not message or message == 'Enter message to hide...':
            messagebox.showerror('Error', 'No message to embed!')
            return
        out_path = filedialog.asksaveasfilename(
            defaultextension='.png', 
            filetypes=[('PNG', '*.png'), ('BMP', '*.bmp')],
            title='Save stego image as'
        )
        if out_path:
            try:
                stegano.encode_text_in_image(self.image_path, message, out_path)
                messagebox.showinfo('Success', f'Message embedded and saved to {out_path}')
            except Exception as e:
                messagebox.showerror('Error', str(e))

    def extract_text(self):
        if not self.image_path:
            messagebox.showerror('Error', 'No image loaded!')
            return
        try:
            message = stegano.decode_text_from_image(self.image_path)
            self.message_entry.delete('1.0', 'end')
            self.message_entry.insert('1.0', message)
            messagebox.showinfo('Success', 'Message extracted!')
        except Exception as e:
            messagebox.showerror('Error', str(e))

    def embed_file(self):
        if not self.image_path:
            messagebox.showerror('Error', 'No image loaded!')
            return
        file_path = filedialog.askopenfilename(title='Select file to hide')
        if not file_path:
            return
        out_path = filedialog.asksaveasfilename(
            defaultextension='.png', 
            filetypes=[('PNG', '*.png'), ('BMP', '*.bmp')],
            title='Save stego image as'
        )
        if out_path:
            try:
                stegano.encode_file_in_image(self.image_path, file_path, out_path)
                messagebox.showinfo('Success', f'File embedded and saved to {out_path}')
            except Exception as e:
                messagebox.showerror('Error', str(e))

    def extract_file(self):
        if not self.image_path:
            messagebox.showerror('Error', 'No image loaded!')
            return
        out_file = filedialog.asksaveasfilename(title='Save extracted file as')
        if out_file:
            try:
                stegano.decode_file_from_image(self.image_path, out_file)
                messagebox.showinfo('Success', f'File extracted and saved to {out_file}')
            except Exception as e:
                messagebox.showerror('Error', str(e))

if __name__ == '__main__':
    root = tk.Tk()
    app = SteganoGUI(root)
    root.mainloop() 
