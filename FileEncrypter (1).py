import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import hashlib, base64, os
import sys

# -------- Generate Key --------
def generate_key(password):
    """Generate a Fernet key from password using SHA256"""
    return base64.urlsafe_b64encode(
        hashlib.sha256(password.encode()).digest()
    )

# -------- Validate Password --------
def validate_password(password):
    """Validate password strength"""
    if not password:
        messagebox.showwarning("Warning", "Password cannot be empty")
        return False
    if len(password) < 4:
        messagebox.showwarning("Warning", "Password must be at least 4 characters long")
        return False
    return True

# -------- Encrypt File --------
def encrypt_file():
    """Encrypt file with password protection"""
    file_path = filedialog.askopenfilename(title="Select File to Encrypt")
    password = password_entry.get()

    if not file_path:
        messagebox.showwarning("Warning", "Please select a file")
        return
    
    if not validate_password(password):
        return

    try:
        encrypted_file = file_path + ".enc"
        
        # Check if encrypted file already exists
        if os.path.exists(encrypted_file):
            response = messagebox.askyesno(
                "File Exists",
                f"Encrypted file already exists!\nOverwrite {os.path.basename(encrypted_file)}?"
            )
            if not response:
                return
        
        key = generate_key(password)
        fernet = Fernet(key)

        with open(file_path, "rb") as f:
            data = f.read()

        encrypted_data = fernet.encrypt(data)

        with open(encrypted_file, "wb") as f:
            f.write(encrypted_data)

        os.remove(file_path)  # 🔥 delete original file

        password_entry.delete(0, tk.END)  # Clear password field
        
        messagebox.showinfo(
            "Success",
            f"File Encrypted Successfully!\n\nEncrypted: {encrypted_file}\nOriginal file removed."
        )

    except PermissionError:
        messagebox.showerror("Error", "Permission Denied!\nMake sure the file is not in use.")
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found!")
    except Exception as e:
        messagebox.showerror("Error", f"Encryption failed: {str(e)}")

# -------- Decrypt File --------
def decrypt_file():
    """Decrypt encrypted file with password"""
    file_path = filedialog.askopenfilename(
        title="Select Encrypted File",
        filetypes=[("Encrypted Files", "*.enc"), ("All Files", "*.*")]
    )
    password = password_entry.get()

    if not file_path:
        messagebox.showwarning("Warning", "Please select a file")
        return
    
    if not validate_password(password):
        return

    try:
        if not file_path.endswith(".enc"):
            messagebox.showwarning("Warning", "Please select a .enc file")
            return
        
        original_file = file_path.replace(".enc", "")
        
        # Check if original file already exists
        if os.path.exists(original_file):
            response = messagebox.askyesno(
                "File Exists",
                f"Decrypted file already exists!\nOverwrite {os.path.basename(original_file)}?"
            )
            if not response:
                return
        
        key = generate_key(password)
        fernet = Fernet(key)

        with open(file_path, "rb") as f:
            encrypted_data = f.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        with open(original_file, "wb") as f:
            f.write(decrypted_data)

        os.remove(file_path)  # 🔥 delete .enc file

        password_entry.delete(0, tk.END)  # Clear password field
        
        messagebox.showinfo(
            "Success",
            f"File Decrypted Successfully!\n\nDecrypted: {original_file}\nEncrypted file removed."
        )

    except PermissionError:
        messagebox.showerror("Error", "Permission Denied!\nMake sure the file is not in use.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Encrypted file not found!")
    except Exception:
        messagebox.showerror(
            "Error",
            "Decryption failed!\nWrong password or corrupted file."
        )

# -------- GUI --------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("File Encrypter by Sharma - Simple File Encryption")
    root.geometry("420x350")
    root.resizable(False, False)

    tk.Label(root, text="🔐 File Encrypter by Sharma", font=("Arial", 18, "bold")).pack(pady=10)
    tk.Label(root, text="Enter Password", font=("Arial", 10)).pack(pady=5)

    password_entry = tk.Entry(root, show="*", width=30, font=("Arial", 10))
    password_entry.pack(pady=5)

    tk.Label(root, text="(Min 4 characters)", font=("Arial", 8, "italic"), fg="gray").pack()

    tk.Button(
        root, text="Encrypt File",
        width=25, bg="green", fg="white",
        font=("Arial", 10, "bold"),
        command=encrypt_file
    ).pack(pady=10)

    tk.Button(
        root, text="Decrypt File",
        width=25, bg="blue", fg="white",
        font=("Arial", 10, "bold"),
        command=decrypt_file
    ).pack(pady=5)

    tk.Label(
        root,
        text="Cyber Security Mini Project | Simple Encryption",
        fg="gray",
        font=("Arial", 8)
    ).pack(side="bottom", pady=10)

    root.mainloop()