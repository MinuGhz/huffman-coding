import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import txtfile_creator

def compress():
    messagebox.showinfo("Compress", "Compression finished successfully")


def decompress():
    messagebox.showinfo("Decompress", "Decompression finished successfully")


def open_generate_file_window():
    txtfile_creator.create_large_text_file(10)
    messagebox.showinfo("File Generated", "File Generated successfully. Size: 10MB")
def open_decoding_window():
    dec_win = ctk.CTkToplevel(root)
    dec_win.title("Show Decoding")
    dec_win.geometry("450x350")
    ctk.CTkLabel(dec_win, text="Decoding Output:", font=("Arial", 14)).pack(pady=10)
    text_box = scrolledtext.ScrolledText(dec_win, width=50, height=10)
    text_box.pack(pady=5)
    text_box.insert("end", "Decoding output placeholder")


def setup_main_window():
    global root
    ctk.set_appearance_mode("dark")  # Modern dark mode
    ctk.set_default_color_theme("blue")
    root = ctk.CTk()
    root.title("Huffman Coded File Compressor")
    root.geometry("600x500")

    ctk.CTkLabel(root, text="File Processing Tool", font=("Arial", 18, "bold")).pack(pady=20)

    btn_frame = ctk.CTkFrame(root)
    btn_frame.pack(pady=20, padx=20, fill="both", expand=True)

    ctk.CTkButton(btn_frame, text="Compress", fg_color="#2196F3", command=compress).pack(fill='x', pady=5, padx=20)
    ctk.CTkButton(btn_frame, text="Decompress", fg_color="#FF9800", command=decompress).pack(fill='x', pady=5, padx=20)
    ctk.CTkButton(btn_frame, text="Generate a File", fg_color="#4CAF50", command=open_generate_file_window).pack(
        fill='x', pady=5, padx=20)
    ctk.CTkButton(btn_frame, text="Show the Decoding", fg_color="#E91E63", command=open_decoding_window).pack(fill='x',
                                                                                                              pady=5,
                                                                                                              padx=20)

    root.mainloop()


setup_main_window()