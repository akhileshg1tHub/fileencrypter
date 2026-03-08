import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import hashlib, base64, os

# -------- Generate Key --------
def generate_key(password):
    return base64.urlsafe_b64encode(
        hashlib.sha256(password.encode()).digest()
    )

# -------- Encrypt File --------
def encrypt_file():
    file_path = filedialog.askopenfilename(title="Select File to Encrypt")
    password = password_entry.get()

    if not file_path or not password:
        messagebox.showwarning("Warning", "Select file and enter password")
        return

    try:
        key = generate_key(password)
        fernet = Fernet(key)

        with open(file_path, "rb") as f:
            data = f.read()

        encrypted_data = fernet.encrypt(data)
        encrypted_file = file_path + ".enc"

        with open(encrypted_file, "wb") as f:
            f.write(encrypted_data)

        os.remove(file_path)  # 🔥 delete original file

        messagebox.showinfo(
            "Success",
            "File Encrypted Successfully!\nOriginal file removed."
        )

    except Exception as e:
        messagebox.showerror("Error", "Encryption failed")

# -------- Decrypt File --------
def decrypt_file():
    file_path = filedialog.askopenfilename(
        title="Select Encrypted File",
        filetypes=[("Encrypted Files", "*.enc")]
    )
    password = password_entry.get()

    if not file_path or not password:
        messagebox.showwarning("Warning", "Select .enc file and enter password")
        return

    try:
        key = generate_key(password)
        fernet = Fernet(key)

        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        original_file = file_path.replace(".enc", "")

        with open(original_file, "wb") as f:
            f.write(decrypted_data)

        os.remove(file_path)  # 🔥 delete .enc file

        messagebox.showinfo(
            "Success",
            "File Decrypted Successfully!\nEncrypted file removed."
        )

    except Exception:
        messagebox.showerror(
            "Error",
            "Wrong password or corrupted file"
        )

# -------- GUI --------
root = tk.Tk()
root.title("File Encrypter by Sharma - Simple File Encryption")
root.geometry("420x300")
root.resizable(False, False)

tk.Label(root, text="🔐 File Encrypter by Sharma", font=("Arial", 18, "bold")).pack(pady=10)
tk.Label(root, text="Enter Password").pack()

password_entry = tk.Entry(root, show="*", width=30)
password_entry.pack(pady=5)

tk.Button(
    root, text="Encrypt File",
    width=22, bg="green", fg="white",
    command=encrypt_file
).pack(pady=10)

tk.Button(
    root, text="Decrypt File",
    width=22, bg="blue", fg="white",
    command=decrypt_file
).pack(pady=5)

tk.Label(
    root,
    text="Cyber Security Mini Project | Simple Encryption",
    fg="gray"
).pack(side="bottom", pady=10)

root.mainloop()