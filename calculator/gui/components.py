import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from typing import Callable, Optional, List, Dict, Any
from datetime import datetime

from gui.styles import get_style_manager, apply_theme_to_widget
from utils.constants import BUTTON_LAYOUT, BUTTON_HEIGHT, BUTTON_WIDTH, BUTTON_PADDING
from utils.logger import get_logger

class CalculatorDisplay(tk.Entry):
    def __init__(self, parent: tk.Widget, **kwargs):
        self.logger = get_logger("Display")
        
        self.display_var = tk.StringVar()
        self.display_var.set("0")
        
        super().__init__(
            parent,
            textvariable=self.display_var,
            **kwargs
        )
        
        apply_theme_to_widget(self, "display")
        self._calculator_style_info = ("display", "normal")
        
        self.config(state='readonly', justify='right')
        
        self.bind('<Control-c>', self._copy_to_clipboard)
        
        self.logger.debug("Calculator display initialized")
    
    def set_text(self, text: str) -> None:
        self.config(state='normal')
        self.display_var.set(str(text))
        self.config(state='readonly')
        
        self.icursor(tk.END)
    
    def get_text(self) -> str:
        return self.display_var.get()
    
    def clear(self) -> None:
        self.set_text("0")
    
    def append_text(self, text: str) -> None:
        current = self.get_text()
        if current == "0":
            self.set_text(text)
        else:
            self.set_text(current + text)
    
    def _copy_to_clipboard(self, event=None) -> None:
        try:
            self.clipboard_clear()
            self.clipboard_append(self.get_text())
            self.logger.debug(f"Copied to clipboard: {self.get_text()}")
        except Exception as e:
            self.logger.error(f"Failed to copy to clipboard: {str(e)}")

class CalculatorButton(tk.Button):
    def __init__(self, parent: tk.Widget, text: str, command: Callable,
                 button_type: str = "number", **kwargs):
        self.button_type = button_type
        self.logger = get_logger("Button")
        
        super().__init__(parent, text=text, command=command, **kwargs)
        
        self._apply_button_style()
        self._add_effects()
        
        self._calculator_style_info = ("button", button_type)
        
        self.logger.debug(f"Created {button_type} button: {text}")
    
    def _apply_button_style(self) -> None:
        apply_theme_to_widget(self, "button", self.button_type)
        
        self.config(
            height=BUTTON_HEIGHT,
            width=BUTTON_WIDTH
        )
    
    def _add_effects(self) -> None:
        style_mgr = get_style_manager()
        style_mgr.apply_hover_effect(self, self.button_type)
        style_mgr.apply_press_effect(self)

class ButtonGrid(tk.Frame):
    def __init__(self, parent: tk.Widget, button_callback: Callable[[str], None]):
        super().__init__(parent)
        self.button_callback = button_callback
        self.buttons: Dict[str, CalculatorButton] = {}
        self.logger = get_logger("ButtonGrid")
        
        apply_theme_to_widget(self, "window")
        self._calculator_style_info = ("window", "normal")
        
        self._create_buttons()
        self.logger.debug("Button grid initialized")
    
    def _create_buttons(self) -> None:
        for row_idx, row in enumerate(BUTTON_LAYOUT):
            for col_idx, button_text in enumerate(row):
                button_type = self._get_button_type(button_text)
                
                button = CalculatorButton(
                    self,
                    text=button_text,
                    command=lambda text=button_text: self.button_callback(text),
                    button_type=button_type
                )
                
                button.grid(
                    row=row_idx,
                    column=col_idx,
                    padx=BUTTON_PADDING,
                    pady=BUTTON_PADDING,
                    sticky="nsew"
                )
                
                self.buttons[button_text] = button
        
        for i in range(len(BUTTON_LAYOUT)):
            self.grid_rowconfigure(i, weight=1)
        for i in range(len(BUTTON_LAYOUT[0])):
            self.grid_columnconfigure(i, weight=1)
    
    def _get_button_type(self, button_text: str) -> str:
        if button_text in '0123456789.':
            return "number"
        elif button_text in '+-*/':
            return "operator"
        elif button_text in ['C', 'CE', '±', '%']:
            return "function"
        elif button_text == '=':
            return "special"
        else:
            return "number"
    
    def get_button(self, button_text: str) -> Optional[CalculatorButton]:
        return self.buttons.get(button_text)
    
    def disable_button(self, button_text: str) -> None:
        button = self.get_button(button_text)
        if button:
            button.config(state='disabled')
    
    def enable_button(self, button_text: str) -> None:
        button = self.get_button(button_text)
        if button:
            button.config(state='normal')

class HistoryPanel(tk.Frame):
    def __init__(self, parent: tk.Widget):
        super().__init__(parent)
        self.logger = get_logger("HistoryPanel")
        
        self._create_widgets()
        self._setup_layout()
        
        apply_theme_to_widget(self, "window")
        self._calculator_style_info = ("window", "normal")
        
        self.logger.debug("History panel initialized")
    
    def _create_widgets(self) -> None:
        self.title_label = tk.Label(self, text="Lịch Sử Tính Toán")
        apply_theme_to_widget(self.title_label, "label", "title")
        self.title_label._calculator_style_info = ("label", "title")
        
        self.history_frame = tk.Frame(self)
        apply_theme_to_widget(self.history_frame, "window")
        self.history_frame._calculator_style_info = ("window", "normal")
        
        self.history_listbox = tk.Listbox(
            self.history_frame,
            selectmode=tk.SINGLE,
            activestyle='dotbox'
        )
        
        self.scrollbar = tk.Scrollbar(
            self.history_frame,
            orient=tk.VERTICAL,
            command=self.history_listbox.yview
        )
        
        self.history_listbox.config(yscrollcommand=self.scrollbar.set)
        
        self.button_frame = tk.Frame(self)
        apply_theme_to_widget(self.button_frame, "window")
        self.button_frame._calculator_style_info = ("window", "normal")
        
        self.clear_button = CalculatorButton(
            self.button_frame,
            text="Xóa Lịch Sử",
            command=self.clear_history,
            button_type="function"
        )
        
        self.copy_button = CalculatorButton(
            self.button_frame,
            text="Sao Chép",
            command=self.copy_selected,
            button_type="function"
        )
        
        self.history_listbox.bind('<Double-Button-1>', self.on_double_click)
        self.history_listbox.bind('<Return>', self.on_double_click)
    
    def _setup_layout(self) -> None:
        self.title_label.pack(pady=(10, 5))
        
        self.history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 5))
        self.copy_button.pack(side=tk.LEFT)
    
    def add_calculation(self, expression: str, result: str) -> None:
        timestamp = datetime.now().strftime("%H:%M:%S")
        history_text = f"{timestamp} | {expression} = {result}"
        
        self.history_listbox.insert(tk.END, history_text)
        
        self.history_listbox.see(tk.END)
        
        self.logger.debug(f"Added to history: {history_text}")
    
    def clear_history(self) -> None:
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ lịch sử?"):
            self.history_listbox.delete(0, tk.END)
            self.logger.info("History cleared")
    
    def copy_selected(self) -> None:
        selection = self.history_listbox.curselection()
        if selection:
            text = self.history_listbox.get(selection[0])
            if " | " in text and " = " in text:
                expression_part = text.split(" | ")[1].split(" = ")[0]
                try:
                    self.clipboard_clear()
                    self.clipboard_append(expression_part)
                    self.logger.debug(f"Copied expression: {expression_part}")
                except Exception as e:
                    self.logger.error(f"Failed to copy: {str(e)}")
    
    def on_double_click(self, event=None) -> None:
        selection = self.history_listbox.curselection()
        if selection:
            self.copy_selected()
    
    def get_history_data(self) -> List[str]:
        return [self.history_listbox.get(i) for i in range(self.history_listbox.size())]

class MemoryPanel(tk.Frame):
    def __init__(self, parent: tk.Widget, memory_callback: Callable[[str], None]):
        super().__init__(parent)
        self.memory_callback = memory_callback
        self.memory_value = "0"
        self.logger = get_logger("MemoryPanel")
        
        self._create_widgets()
        self._setup_layout()
        
        apply_theme_to_widget(self, "window")
        self._calculator_style_info = ("window", "normal")
        
        self.logger.debug("Memory panel initialized")
    
    def _create_widgets(self) -> None:
        self.title_label = tk.Label(self, text="Bộ Nhớ")
        apply_theme_to_widget(self.title_label, "label", "title")
        self.title_label._calculator_style_info = ("label", "title")
        
        self.memory_display = tk.Label(
            self,
            text="M: 0",
            relief=tk.SUNKEN,
            borderwidth=2,
            anchor='e',
            padx=10
        )
        apply_theme_to_widget(self.memory_display, "label", "normal")
        self.memory_display._calculator_style_info = ("label", "normal")
        
        self.button_frame = tk.Frame(self)
        apply_theme_to_widget(self.button_frame, "window")
        self.button_frame._calculator_style_info = ("window", "normal")
        
        self.ms_button = CalculatorButton(
            self.button_frame,
            text="MS",
            command=lambda: self.memory_callback("MS"),
            button_type="function"
        )
        
        self.mr_button = CalculatorButton(
            self.button_frame,
            text="MR",
            command=lambda: self.memory_callback("MR"),
            button_type="function"
        )
        
        self.mc_button = CalculatorButton(
            self.button_frame,
            text="MC",
            command=lambda: self.memory_callback("MC"),
            button_type="function"
        )
        
        self.m_plus_button = CalculatorButton(
            self.button_frame,
            text="M+",
            command=lambda: self.memory_callback("M+"),
            button_type="function"
        )
        
        self.m_minus_button = CalculatorButton(
            self.button_frame,
            text="M-",
            command=lambda: self.memory_callback("M-"),
            button_type="function"
        )
    
    def _setup_layout(self) -> None:
        self.title_label.pack(pady=(10, 5))
        self.memory_display.pack(fill=tk.X, padx=10, pady=5)
        
        self.button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.ms_button.grid(row=0, column=0, padx=2, pady=2)
        self.mr_button.grid(row=0, column=1, padx=2, pady=2)
        self.mc_button.grid(row=0, column=2, padx=2, pady=2)
        self.m_plus_button.grid(row=1, column=0, padx=2, pady=2)
        self.m_minus_button.grid(row=1, column=1, padx=2, pady=2)
        
        for i in range(3):
            self.button_frame.grid_columnconfigure(i, weight=1)
    
    def update_memory_display(self, value: str) -> None:
        self.memory_value = value
        display_text = f"M: {value}"
        if len(display_text) > 20:
            display_text = f"M: {value[:15]}..."
        
        self.memory_display.config(text=display_text)
        self.logger.debug(f"Memory updated: {value}")

class StatusBar(tk.Frame):
    def __init__(self, parent: tk.Widget):
        super().__init__(parent, relief=tk.SUNKEN, borderwidth=1)
        
        self.status_label = tk.Label(
            self,
            text="Sẵn sàng",
            anchor='w'
        )
        apply_theme_to_widget(self.status_label, "label", "small")
        self.status_label._calculator_style_info = ("label", "small")
        
        self.theme_label = tk.Label(
            self,
            text="Light",
            anchor='e'
        )
        apply_theme_to_widget(self.theme_label, "label", "small")
        self.theme_label._calculator_style_info = ("label", "small")
        
        self.status_label.pack(side=tk.LEFT, padx=5)
        self.theme_label.pack(side=tk.RIGHT, padx=5)
        
        apply_theme_to_widget(self, "window")
        self._calculator_style_info = ("window", "normal")
    
    def set_status(self, message: str) -> None:
        self.status_label.config(text=message)
    
    def set_theme_indicator(self, theme_name: str) -> None:
        self.theme_label.config(text=theme_name.title())