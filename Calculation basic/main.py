# main.py
import tkinter as tk
from gui_app import CalculatorGUI

if __name__ == "__main__":
    root = tk.Tk()
    calculator_app = CalculatorGUI(root)
    root.mainloop()