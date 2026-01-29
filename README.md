# password-generator-python-gui

A professional, cryptographically secure password generator built with Python and a modern Dark Mode GUI.  
Implements the Model-View-Controller (MVC) pattern, uses Python's `secrets` (CSPRNG) for generation, and provides real-time Shannon entropy to grade password strength.


---

Table of Contents
- [Highlights](#highlights)
- [Security Details](#security-details)
- [Entropy & Strength Grading](#entropy--strength-grading)
- [Architecture (MVC)](#architecture-mvc)
- [Install & Run](#install--run)
- [Usage](#usage)
- [Code Overview (quick)](#code-overview-quick)
- [Contributing](#contributing)
- [License](#license)
- [Contact / Author](#contact--author)

---

## Highlights

- Cryptographically secure password generation using Python's `secrets` module (wraps OS CSPRNG).
- Real-time Shannon entropy calculation (bits) and strength classification.
- Dark-themed cross-platform GUI using `customtkinter`.
- Options to include/exclude character classes and to filter ambiguous characters (e.g., `1`, `l`, `I`, `0`, `O`).
- Clean MVC separation:
  - Model: `PasswordLogic` — pure logic, testable, typed.
  - View/Controller: `PasswordApp` — GUI with event handling and presentation.
- Clipboard integration with status feedback and error handling.

---

## Security Details

- Uses `secrets.choice` (CSPRNG) — safe for generating secrets and passwords.
- Avoids the insecure `random` module for password generation.
- Character pools are filtered and built deterministically; excluding ambiguous characters is supported.
- Entropy is computed precisely with information-theory formula.

---

## Entropy & Strength Grading

We calculate bits of entropy using:

H = L × log2(N)

Where:
- L = password length
- N = size of the effective character pool

Example: lowercase + uppercase + digits (62 char pool), length 12:
H ≈ 12 × log2(62) ≈ 71.2 bits

Strength buckets used by the app:
- < 28 bits — Very Weak 🔴
- 28–35 bits — Weak 🟠
- 36–59 bits — Good 🟡
- 60–127 bits — Strong 🟢
- >= 128 bits — Uncrackable 🛡️

Note: For very high-security use cases, prefer passphrases or longer random strings to reach 128+ bits.

---

## Architecture (MVC)

- Model: `PasswordLogic`
  - Builds character pools, applies ambiguity filters, generates passwords with `secrets`, computes entropy, returns strength and a hex color for UI.
  - Pure logic with typed signatures for easy unit testing.
- View & Controller: `PasswordApp`
  - Built with `customtkinter` (Dark Mode), contains layout, controls (sliders, toggles, buttons), and event handling.
  - Delegates generation and calculations to `PasswordLogic`.

Benefits:
- Logic can be tested independently of UI.
- Clear separation improves maintainability and extensibility.

---

## Install & Run

Prerequisites:
- Python 3.8+
- Git (optional)

Quickstart:
```bash
git clone https://github.com/YOUR_USERNAME/password-generator-python-gui.git
cd password-generator-python-gui
python -m venv .venv
# macOS / Linux
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\Activate.ps1

pip install customtkinter packaging
# or, if present:
# pip install -r requirements.txt

python main.py
```

Notes:
- On some Linux distros, you may need system Tk packages (e.g., `tk`, `tk-dev`, or similar) for tkinter/customtkinter to work.
- If you package this as a distributable, ensure `tk` runtime is available on target systems.

---

## Usage

- Launch the app with `python main.py`.
- Pick which character classes to include: Uppercase, Lowercase, Digits, Symbols.
- Toggle "Exclude Ambiguous" to remove confusing glyphs (like `0`, `O`, `1`, `l`).
- Use the slider to set password length (default 16).
- Click "Generate Password" to produce a secure password and see entropy + strength.
- Click "Copy to Clipboard" to copy the password (status shown in the UI).

---

## Code Overview (quick)

Primary components (as provided in this repository):
- `main.py` — contains `PasswordLogic` (Model) and `PasswordApp` (View/Controller).
  - `PasswordLogic.generate_password(length, use_upper, use_lower, use_digits, use_symbols, exclude_ambiguous)`  
    Returns: `(password, entropy_bits, strength_text, color_hex, is_error)`
  - `PasswordApp` — `customtkinter` GUI that uses `PasswordLogic` to produce results and update the UI.

Conceptual example:
```python
from password_logic import PasswordLogic

pwd, entropy, strength, color_hex, is_error = PasswordLogic.generate_password(
    length=16, use_upper=True, use_lower=True, use_digits=True, use_symbols=True, exclude_ambiguous=False
)
```

## Credits & Links

- Author: Kishanu Mondal
- GitHub: https://github.com/kxnux-builds
- LinkedIn: https://www.linkedin.com/in/kishanu-mondal/
- X (Twitter): https://x.com/Kxnux_Dev

---

## License

See the LICENSE file for license details:
[LICENSE](./LICENSE)

---