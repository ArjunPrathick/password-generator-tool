import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip
import re

class PasswordGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")
        self.root.geometry("500x600")
        self.root.resizable(False, False)
        
        # Configure style
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#2196F3")
        self.style.configure("TCheckbutton", padding=6)
        self.style.configure("TLabel", padding=6)
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Dark mode toggle
        self.dark_mode = tk.BooleanVar(value=False)
        self.toggle_button = ttk.Checkbutton(self.main_frame, text="Dark Mode", variable=self.dark_mode, command=self.toggle_dark_mode)
        self.toggle_button.pack(anchor=tk.NE, pady=5)
        
        # Password length
        self.length_label = ttk.Label(self.main_frame, text="Password Length:")
        self.length_label.pack(pady=5)
        
        self.length_var = tk.IntVar(value=12)
        self.length_scale = ttk.Scale(self.main_frame, from_=8, to=32, orient=tk.HORIZONTAL, 
                                    variable=self.length_var, command=self.update_length_label)
        self.length_scale.pack(fill=tk.X, pady=5)
        
        self.length_value_label = ttk.Label(self.main_frame, text="12")
        self.length_value_label.pack(pady=5)
        
        # Character options
        self.options_frame = ttk.LabelFrame(self.main_frame, text="Character Options", padding="10")
        self.options_frame.pack(fill=tk.X, pady=10)
        
        self.uppercase_var = tk.BooleanVar(value=True)
        self.lowercase_var = tk.BooleanVar(value=True)
        self.numbers_var = tk.BooleanVar(value=True)
        self.symbols_var = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(self.options_frame, text="Uppercase Letters", variable=self.uppercase_var).pack(anchor=tk.W)
        ttk.Checkbutton(self.options_frame, text="Lowercase Letters", variable=self.lowercase_var).pack(anchor=tk.W)
        ttk.Checkbutton(self.options_frame, text="Numbers", variable=self.numbers_var).pack(anchor=tk.W)
        ttk.Checkbutton(self.options_frame, text="Symbols", variable=self.symbols_var).pack(anchor=tk.W)
        
        # Generate button
        self.generate_button = ttk.Button(self.main_frame, text="Generate Password", command=self.generate_password)
        self.generate_button.pack(pady=20)
        
        # Password display
        self.password_frame = ttk.LabelFrame(self.main_frame, text="Generated Password", padding="10")
        self.password_frame.pack(fill=tk.X, pady=10)
        
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(self.password_frame, textvariable=self.password_var, 
                                      font=("Arial", 12), justify=tk.CENTER)
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Copy button
        self.copy_button = ttk.Button(self.password_frame, text="Copy to Clipboard", 
                                    command=self.copy_to_clipboard)
        self.copy_button.pack(pady=5)
        
        # Strength indicator
        self.strength_frame = ttk.LabelFrame(self.main_frame, text="Password Strength", padding="10")
        self.strength_frame.pack(fill=tk.X, pady=10)
        
        # Create a container frame for the strength indicator
        self.strength_container = ttk.Frame(self.strength_frame)
        self.strength_container.pack(fill=tk.X, pady=5)
        
        # Create the strength bar canvas with a fixed size
        self.strength_canvas = tk.Canvas(self.strength_container, height=30, width=400, bg="white", highlightthickness=1, highlightbackground="black")
        self.strength_canvas.pack(side=tk.LEFT, padx=5)
        
        # Create the strength label with larger font
        self.strength_label = ttk.Label(self.strength_container, text="", font=("Arial", 10, "bold"))
        self.strength_label.pack(side=tk.LEFT, padx=5)
        
        # Bind password generation to option changes
        for var in [self.uppercase_var, self.lowercase_var, self.numbers_var, self.symbols_var]:
            var.trace_add("write", lambda *args: self.generate_password())
        
        # Generate initial password
        self.generate_password()
    
    def toggle_dark_mode(self):
        if self.dark_mode.get():
            self.root.configure(bg='#333333')
            self.main_frame.configure(style='Dark.TFrame')
            self.style.configure('Dark.TFrame', background='#333333')
            self.style.configure('TLabel', background='#333333', foreground='white')
            self.style.configure('TButton', background='#555555', foreground='white')
            self.strength_canvas.configure(bg='#555555')
        else:
            self.root.configure(bg='white')
            self.main_frame.configure(style='TFrame')
            self.style.configure('TFrame', background='white')
            self.style.configure('TLabel', background='white', foreground='black')
            self.style.configure('TButton', background='#2196F3', foreground='black')
            self.strength_canvas.configure(bg='white')
        self.generate_password()  # Update UI after mode change
    
    def update_length_label(self, *args):
        self.length_value_label.config(text=str(int(self.length_var.get())))
        self.generate_password()
    
    def generate_password(self):
        length = int(self.length_var.get())
        characters = []
        
        if self.uppercase_var.get():
            characters.extend(string.ascii_uppercase)
        if self.lowercase_var.get():
            characters.extend(string.ascii_lowercase)
        if self.numbers_var.get():
            characters.extend(string.digits)
        if self.symbols_var.get():
            characters.extend(string.punctuation)
        
        if not characters:
            messagebox.showwarning("Warning", "Please select at least one character type!")
            return
        
        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_var.set(password)
        self.check_strength(password)
    
    def check_strength(self, password):
        score = 0
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        
        # Character type checks
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[0-9]', password):
            score += 1
        if re.search(r'[^A-Za-z0-9]', password):
            score += 1
        
        # Ensure score is between 1 and 5
        score = max(1, min(score, 5))
        
        # Update strength indicator
        self.strength_canvas.delete("all")
        colors = ["#FF0000", "#FFA500", "#FFFF00", "#90EE90", "#008000"]  # More vibrant colors
        canvas_width = 400  # Fixed width
        bar_width = (canvas_width * score) / 5
        
        # Draw the strength bar with a border
        self.strength_canvas.create_rectangle(0, 0, bar_width, 30, fill=colors[score-1], outline="black")
        
        # Update strength text with color
        strength_texts = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]
        self.strength_label.config(text=strength_texts[score-1], foreground=colors[score-1])
    
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Success", "Password copied to clipboard!")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGenerator(root)
    root.mainloop() 