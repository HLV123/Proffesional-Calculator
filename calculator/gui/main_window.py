import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Dict, Any
import json
import os

from gui.components import (
    CalculatorDisplay, ButtonGrid, HistoryPanel, 
    MemoryPanel, StatusBar
)
from gui.styles import (
    get_theme_manager, get_style_manager, 
    apply_theme_to_widget
)
from core.calculator import CalculatorEngine
from utils.constants import (
    WINDOW_TITLE, WINDOW_SIZE, WINDOW_MIN_SIZE, APP_NAME, APP_VERSION
)
from utils.logger import get_logger
from utils.exceptions import CalculatorError

class CalculatorMainWindow:
    def __init__(self):
        self.logger = get_logger("MainWindow")
        
        self.calculator = CalculatorEngine()
        
        self.theme_manager = get_theme_manager()
        self.style_manager = get_style_manager()
        
        self.root: Optional[tk.Tk] = None
        self.display: Optional[CalculatorDisplay] = None
        self.button_grid: Optional[ButtonGrid] = None
        self.history_panel: Optional[HistoryPanel] = None
        self.memory_panel: Optional[MemoryPanel] = None
        self.status_bar: Optional[StatusBar] = None
        
        self.is_sidebar_visible = False
        
        self._create_main_window()
        self._create_menu()
        self._create_widgets()
        self._setup_layout()
        self._setup_keyboard_bindings()
        
        self.logger.info("Calculator main window initialized")
    
    def _create_main_window(self) -> None:
        self.root = tk.Tk()
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(*WINDOW_MIN_SIZE)
        
        apply_theme_to_widget(self.root, "window")
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_menu(self) -> None:
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tập tin", menu=file_menu)
        file_menu.add_command(label="Xuất lịch sử...", command=self._export_history)
        file_menu.add_command(label="Nhập lịch sử...", command=self._import_history)
        file_menu.add_separator()
        file_menu.add_command(label="Thoát", command=self._on_closing)
        
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Hiển thị", menu=view_menu)
        view_menu.add_command(label="Bật/Tắt Sidebar", command=self._toggle_sidebar)
        view_menu.add_separator()
        
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Theme", menu=theme_menu)
        
        available_themes = self.theme_manager.get_available_themes()
        for theme_name, description in available_themes.items():
            theme_menu.add_command(
                label=f"{theme_name.title()} - {description}",
                command=lambda t=theme_name: self._change_theme(t)
            )
        
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Công cụ", menu=tools_menu)
        tools_menu.add_command(label="Xóa lịch sử", command=self._clear_history)
        tools_menu.add_command(label="Xóa bộ nhớ", command=self._clear_memory)
        tools_menu.add_command(label="Reset máy tính", command=self._reset_calculator)
        
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Trợ giúp", menu=help_menu)
        help_menu.add_command(label="Phím tắt", command=self._show_shortcuts)
        help_menu.add_command(label="Về chương trình", command=self._show_about)
    
    def _create_widgets(self) -> None:
        self.main_frame = tk.Frame(self.root)
        apply_theme_to_widget(self.main_frame, "window")
        
        self.calculator_frame = tk.Frame(self.main_frame)
        apply_theme_to_widget(self.calculator_frame, "window")
        
        self.display = CalculatorDisplay(self.calculator_frame)
        
        self.button_grid = ButtonGrid(
            self.calculator_frame,
            self._on_button_click
        )
        
        self.sidebar_frame = tk.Frame(self.main_frame, width=300)
        apply_theme_to_widget(self.sidebar_frame, "window")
        
        self.sidebar_notebook = ttk.Notebook(self.sidebar_frame)
        
        self.history_panel = HistoryPanel(self.sidebar_notebook)
        self.sidebar_notebook.add(self.history_panel, text="Lịch Sử")
        
        self.memory_panel = MemoryPanel(
            self.sidebar_notebook,
            self._on_memory_operation
        )
        self.sidebar_notebook.add(self.memory_panel, text="Bộ Nhớ")
        
        self.status_bar = StatusBar(self.root)
    
    def _setup_layout(self) -> None:
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.calculator_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.display.pack(fill=tk.X, pady=(0, 10))
        
        self.button_grid.pack(fill=tk.BOTH, expand=True)
        
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _setup_keyboard_bindings(self) -> None:
        self.root.focus_set()
        
        for i in range(10):
            self.root.bind(str(i), lambda event, num=str(i): self._on_button_click(num))
        
        self.root.bind('+', lambda event: self._on_button_click('+'))
        self.root.bind('-', lambda event: self._on_button_click('-'))
        self.root.bind('*', lambda event: self._on_button_click('*'))
        self.root.bind('/', lambda event: self._on_button_click('/'))
        self.root.bind('.', lambda event: self._on_button_click('.'))
        self.root.bind('%', lambda event: self._on_button_click('%'))
        
        self.root.bind('<Return>', lambda event: self._on_button_click('='))
        self.root.bind('<KP_Enter>', lambda event: self._on_button_click('='))
        self.root.bind('=', lambda event: self._on_button_click('='))
        self.root.bind('<Escape>', lambda event: self._on_button_click('C'))
        self.root.bind('<BackSpace>', lambda event: self._on_button_click('CE'))
        
        self.root.bind('<Control-q>', lambda event: self._on_closing())
        self.root.bind('<Control-r>', lambda event: self._reset_calculator())
    
    def _on_button_click(self, button_value: str) -> None:
        try:
            self.status_bar.set_status("Đang tính toán...")
            
            result = self.calculator.handle_button_press(button_value)
            
            self.display.set_text(result)
            
            if button_value == '=' and not self.calculator.is_error_state:
                last_calc = self.calculator.history.get_last_calculation()
                if last_calc:
                    self.history_panel.add_calculation(
                        last_calc['expression'],
                        last_calc['result']
                    )
            
            memory_value = self.calculator.memory_recall()
            self.memory_panel.update_memory_display(memory_value)
            
            self.status_bar.set_status("Sẵn sàng")
            
        except Exception as e:
            self.logger.error(f"Error processing button click: {str(e)}")
            self.display.set_text("Lỗi")
            self.status_bar.set_status("Lỗi")
    
    def _on_memory_operation(self, operation: str) -> None:
        try:
            current_value = self.display.get_text()
            
            if operation == "MS":
                self.calculator.memory_store(current_value)
            elif operation == "MR":
                recalled_value = self.calculator.memory_recall()
                self.display.set_text(recalled_value)
            elif operation == "MC":
                self.calculator.memory_clear()
            elif operation == "M+":
                self.calculator.memory_add(current_value)
            elif operation == "M-":
                self.calculator.memory_subtract(current_value)
            
            memory_value = self.calculator.memory_recall()
            self.memory_panel.update_memory_display(memory_value)
            
        except Exception as e:
            self.logger.error(f"Memory operation error: {str(e)}")
    
    def _toggle_sidebar(self) -> None:
        if self.is_sidebar_visible:
            self.sidebar_frame.pack_forget()
            self.is_sidebar_visible = False
        else:
            self.sidebar_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 10), pady=10)
            self.sidebar_notebook.pack(fill=tk.BOTH, expand=True)
            self.is_sidebar_visible = True
    
    def _change_theme(self, theme_name: str) -> None:
        if self.theme_manager.set_theme(theme_name):
            self._refresh_all_widgets()
            self.status_bar.set_theme_indicator(theme_name)
            messagebox.showinfo("Theme", f"Đã chuyển sang theme: {theme_name.title()}")
    
    def _refresh_all_widgets(self) -> None:
        def refresh_widget(widget):
            if hasattr(widget, '_calculator_style_info'):
                style_type, widget_type = widget._calculator_style_info
                apply_theme_to_widget(widget, style_type, widget_type)
            
            for child in widget.winfo_children():
                refresh_widget(child)
        
        refresh_widget(self.root)
    
    def _export_history(self) -> None:
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Xuất lịch sử tính toán"
            )
            
            if filename:
                history_data = self.calculator.history.export_to_json()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(history_data)
                messagebox.showinfo("Thành công", f"Đã xuất lịch sử ra file: {filename}")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể xuất lịch sử: {str(e)}")
    
    def _import_history(self) -> None:
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
                title="Nhập lịch sử tính toán"
            )
            
            if filename:
                with open(filename, 'r', encoding='utf-8') as f:
                    history_data = f.read()
                
                count = self.calculator.history.import_from_json(history_data)
                messagebox.showinfo("Thành công", f"Đã nhập {count} mục lịch sử")
                
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể nhập lịch sử: {str(e)}")
    
    def _clear_history(self) -> None:
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa toàn bộ lịch sử?"):
            self.calculator.history.clear_history()
            if hasattr(self, 'history_panel') and self.history_panel:
                self.history_panel.clear_history()
    
    def _clear_memory(self) -> None:
        self.calculator.memory_clear()
        self.memory_panel.update_memory_display("0")
        messagebox.showinfo("Thông báo", "Đã xóa bộ nhớ")
    
    def _reset_calculator(self) -> None:
        if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn reset toàn bộ máy tính?"):
            self.calculator.reset()
            self.display.clear()
            if hasattr(self, 'history_panel') and self.history_panel:
                self.history_panel.clear_history()
            self.memory_panel.update_memory_display("0")
            messagebox.showinfo("Thông báo", "Đã reset máy tính")
    
    def _show_shortcuts(self) -> None:
        shortcuts = """
Phím tắt Calculator:

Số: 0-9, .
Phép toán: +, -, *, /, %
Tính: Enter hoặc =
Xóa: Escape (C), Backspace (CE)

Ctrl+Q: Thoát
Ctrl+R: Reset
        """
        messagebox.showinfo("Phím tắt", shortcuts)
    
    def _show_about(self) -> None:
        about_text = f"""
{APP_NAME}
Version {APP_VERSION}

Máy tính chuyên nghiệp với GUI hiện đại
Hỗ trợ đầy đủ các phép toán cơ bản
Có lịch sử và bộ nhớ tính toán

Phát triển bởi Lê Văn Hưng HE186837 FPTU
        """
        messagebox.showinfo("Về chương trình", about_text)
    
    def _on_closing(self) -> None:
        if messagebox.askokcancel("Thoát", "Bạn có muốn thoát khỏi Calculator?"):
            self.logger.info("Calculator closing...")
            self.root.destroy()
    
    def run(self) -> None:
        if self.root:
            self.root.mainloop()
        else:
            raise RuntimeError("GUI chưa được khởi tạo")