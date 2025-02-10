import customtkinter as ctk
from tkinter import messagebox, scrolledtext
import txtfile_creator
import Huffman_Code_Final as huffman

huffman_instance = None
def compress():
    # Open file dialog to select the input file for compression
    file_path = ctk.filedialog.askopenfilename(
        title="Select File to Compress",
        filetypes=[("All Files", "*.*")]  # You can specify file types if needed
    )
    if not file_path:  # User canceled the dialog
        return
    try:
        # Initialize HuffmanCode with the selected file and compress
        huffman_instance = huffman.HuffmanCode(file_path)
        huffman_instance.compress()
        output = huffman.print_huffman_codes(huffman_instance)
        open_decoding_window(output)
        messagebox.showinfo("Compress", "Compression finished successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Compression failed: {str(e)}")

def decompress():
    # Open file dialog to select the input file for decompression
    file_path = ctk.filedialog.askopenfilename(
        title="Select File to Decompress",
        filetypes=[("All Files", "*.*")]  # Adjust file types if needed (e.g., "*.huff")
    )
    if not file_path:  # User canceled the dialog
        return
    try:
        huffman_instance = huffman.HuffmanCode(file_path)
        huffman_instance.decompress(file_path)  # Assumes decompress() uses the input path
        messagebox.showinfo("Decompress", "Decompression finished successfully")
    except Exception as e:
        messagebox.showerror("Error", f"Decompression failed: {str(e)}")

def open_generate_file_window():
    txtfile_creator.create_large_text_file(10)
    messagebox.showinfo("File Generated", "File Generated successfully. Size: 10MB")
def open_decoding_window(output = ""):
    dec_win = ctk.CTkToplevel(root)
    dec_win.title("Show Decoding")
    dec_win.geometry("450x350")
    ctk.CTkLabel(dec_win, text="Decoding Output:", font=("Arial", 14)).pack(pady=10)
    text_box = scrolledtext.ScrolledText(dec_win, width=50, height=10)
    text_box.pack(pady=5)
    text_box.insert("end", output)


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