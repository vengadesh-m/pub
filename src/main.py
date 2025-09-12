# src/main.py
import tkinter as tk
from src.gui import APITestGUI

try:
    root = tk.Tk()
    app = APITestGUI(root)
    root.mainloop()
except Exception as e:
    with open("error_log.txt", "w") as f:
        f.write(str(e))