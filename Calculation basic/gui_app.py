# gui_app.py
import tkinter as tk
from calculator_logic import evaluate_expression

class CalculatorGUI:
    def __init__(self, master):
        self.master = master
        master.title("Python Calculator")

        self.expression = ""
        self.input_text = tk.StringVar()

        # Create display field
        self.input_field = tk.Entry(master, font=('arial', 20, 'bold'), textvariable=self.input_text, bd=5, insertwidth=4, width=14, borderwidth=4, justify='right')
        self.input_field.grid(row=0, column=0, columnspan=4)
        
        # Create buttons
        self.create_buttons()

    def create_buttons(self):
        # A list of button labels to create
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]

        row = 1
        col = 0
        for button_text in buttons:
            action = lambda x=button_text: self.click_event(x)
            tk.Button(self.master, text=button_text, command=action, height=2, width=5, font=('arial', 15, 'bold')).grid(row=row, column=col)
            
            col += 1
            if col > 3:
                col = 0
                row += 1

    def click_event(self, key):
        if key == 'C':
            self.expression = ""
            self.input_text.set("")
        elif key == '=':
            self.expression = evaluate_expression(self.expression)
            self.input_text.set(self.expression)
        else:
            self.expression += key
            self.input_text.set(self.expression)