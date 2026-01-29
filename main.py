import customtkinter as ctk
import string
import secrets
import math
from typing import Tuple

APP_TITLE = "Kishanu's Password Generator"
APP_SIZE = "500x600"
COLOR_THEME = "blue"
APPEARANCE_MODE = "Dark"

AMBIGUOUS_CHARS = "1lI|0O"
LETTERS_LOWER = string.ascii_lowercase
LETTERS_UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

class PasswordLogic:
    """
    MODEL: Handles core logic.
    Now returns a specific COLOR for the UI to use.
    """

    @staticmethod
    def generate_password(length: int, use_upper: bool, use_lower: bool, 
                          use_digits: bool, use_symbols: bool, 
                          exclude_ambiguous: bool) -> Tuple[str, float, str, str, bool]:
        """
        Returns: (password, entropy, strength_text, color_hex, is_error)
        """ 
        pool = ""
        if use_lower: pool += LETTERS_LOWER
        if use_upper: pool += LETTERS_UPPER
        if use_digits: pool += DIGITS
        if use_symbols: pool += SYMBOLS
        if exclude_ambiguous and pool:
            ambig_set = set(AMBIGUOUS_CHARS)
            pool = "".join([c for c in pool if c not in ambig_set])
        if not pool:
            return "Select at least one option!", 0, "Error", "#FF5555", True
        password = ''.join(secrets.choice(pool) for _ in range(length))
        pool_size = len(pool)
        entropy = length * math.log2(pool_size) if pool_size > 0 else 0

        if entropy < 28: 
            strength = "Very Weak"
            color = "#FF5555"
        elif entropy < 36: 
            strength = "Weak"
            color = "#FFB86C"
        elif entropy < 60: 
            strength = "Good"
            color = "#F1FA8C"
        elif entropy < 128: 
            strength = "Strong"
            color = "#50FA7B"
        else: 
            strength = "Uncrackable"
            color = "#8BE9FD"

        return password, entropy, strength, color, False

class PasswordApp(ctk.CTk):
    """
    VIEW & CONTROLLER
    """
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode(APPEARANCE_MODE)
        ctk.set_default_color_theme(COLOR_THEME)
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self._create_widgets()
        self.generate_event()

    def _create_widgets(self):
        self.label_title = ctk.CTkLabel(
            self, text="Password Generator", 
            font=("Roboto Medium", 24), text_color="#E0E0E0"
        )
        self.label_title.grid(row=0, column=0, pady=(20, 10), sticky="ew")
        self.entry_password = ctk.CTkEntry(
            self, width=350, height=50, 
            font=("Consolas", 20), justify="center", state="readonly"
        )
        self.entry_password.grid(row=1, column=0, padx=20, pady=10)
        self.label_strength = ctk.CTkLabel(
            self, text="Strength: ---", font=("Roboto Medium", 16)
        )
        self.label_strength.grid(row=2, column=0, pady=(0, 20))
        self.frame_controls = ctk.CTkFrame(self)
        self.frame_controls.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        self.label_slider = ctk.CTkLabel(self.frame_controls, text="Length: 16", font=("Roboto", 14))
        self.label_slider.grid(row=0, column=0, padx=20, pady=10, sticky="w")
        self.slider_length = ctk.CTkSlider(
            self.frame_controls, from_=6, to=64, number_of_steps=58,
            command=self.update_slider_label
        )
        self.slider_length.set(16)
        self.slider_length.grid(row=0, column=1, padx=20, pady=10, sticky="ew")
        
        self.check_upper = ctk.CTkCheckBox(self.frame_controls, text="Uppercase (A-Z)")
        self.check_upper.select()
        self.check_upper.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.check_lower = ctk.CTkCheckBox(self.frame_controls, text="Lowercase (a-z)")
        self.check_lower.select()
        self.check_lower.grid(row=1, column=1, padx=20, pady=10, sticky="w")

        self.check_digits = ctk.CTkCheckBox(self.frame_controls, text="Digits (0-9)")
        self.check_digits.select()
        self.check_digits.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.check_symbols = ctk.CTkCheckBox(self.frame_controls, text="Symbols (!@#$)")
        self.check_symbols.select()
        self.check_symbols.grid(row=2, column=1, padx=20, pady=10, sticky="w")

        self.check_ambiguous = ctk.CTkCheckBox(self.frame_controls, text="Exclude Ambiguous (1, l, I, 0, O)")
        self.check_ambiguous.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="w")

        self.btn_generate = ctk.CTkButton(
            self, text="Generate Password", height=50, 
            font=("Roboto Medium", 16), command=self.generate_event
        )
        self.btn_generate.grid(row=4, column=0, padx=50, pady=(20, 10), sticky="ew")

        self.btn_copy = ctk.CTkButton(
            self, text="Copy to Clipboard", height=40, fg_color="transparent", 
            border_width=2, text_color=("gray10", "#DCE4EE"), 
            font=("Roboto Medium", 14), command=self.copy_to_clipboard
        )
        self.btn_copy.grid(row=5, column=0, padx=50, pady=(0, 20), sticky="ew")

        self.label_status = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.label_status.grid(row=6, column=0, pady=10)

    def update_slider_label(self, value):
        self.label_slider.configure(text=f"Length: {int(value)}")

    def generate_event(self):
        length = int(self.slider_length.get())
        use_upper = self.check_upper.get()
        use_lower = self.check_lower.get()
        use_digits = self.check_digits.get()
        use_symbols = self.check_symbols.get()
        exclude_ambig = self.check_ambiguous.get()

        pwd, entropy, strength_text, color_hex, is_error = PasswordLogic.generate_password(
            length, use_upper, use_lower, use_digits, use_symbols, exclude_ambig
        )

        self.entry_password.configure(state="normal")
        self.entry_password.delete(0, "end")
        self.entry_password.insert(0, pwd)

        if is_error:
            self.entry_password.configure(text_color="#FF5555")
        else:
            self.entry_password.configure(text_color=("black", "white"))

        self.entry_password.configure(state="readonly")

        self.label_strength.configure(
            text=f"Strength: {strength_text} ({int(entropy)} bits)",
            text_color=color_hex
        )
        
        self.label_status.configure(text="New password generated", text_color="#3B8ED0")

    def copy_to_clipboard(self):
        pwd = self.entry_password.get()
        if pwd and "Select at least" not in pwd:
            try:
                self.clipboard_clear()
                self.clipboard_append(pwd)
                self.update()
                self.label_status.configure(text="Copied to clipboard!", text_color="#2CC985")
            except Exception as e:
                self.label_status.configure(text="Clipboard Error!", text_color="#FF5555")
                print(f"Error: {e}")

if __name__ == "__main__":
    app = PasswordApp()
    app.mainloop()