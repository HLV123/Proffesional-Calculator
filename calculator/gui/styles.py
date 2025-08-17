from typing import Dict, Any, Optional
import tkinter as tk
from tkinter import font

from utils.constants import COLORS, DISPLAY_FONT, BUTTON_FONT, MENU_FONT

class ThemeManager:
    def __init__(self):
        self.current_theme = "light"
        self.themes = self._initialize_themes()
        self.custom_fonts = {}
        
    def _initialize_themes(self) -> Dict[str, Dict[str, Any]]:
        return {
            "light": {
                "name": "Light Theme",
                "description": "Giao diện sáng, dễ nhìn ban ngày",
                "colors": {
                    "background": "#FFFFFF",
                    "surface": "#F8F9FA",
                    "primary": "#007BFF",
                    "secondary": "#6C757D",
                    "success": "#28A745",
                    "warning": "#FFC107",
                    "danger": "#DC3545",
                    "text": "#212529",
                    "text_secondary": "#6C757D",
                    "border": "#DEE2E6",
                    "hover": "#E9ECEF",
                    "pressed": "#DEE2E6",
                    "display_bg": "#FFFFFF",
                    "display_text": "#212529",
                    "button_number": "#F8F9FA",
                    "button_operator": "#007BFF",
                    "button_function": "#6C757D",
                    "button_special": "#28A745"
                }
            },
            
            "dark": {
                "name": "Dark Theme", 
                "description": "Giao diện tối, bảo vệ mắt ban đêm",
                "colors": {
                    "background": "#1E1E1E",
                    "surface": "#252526",
                    "primary": "#0E639C",
                    "secondary": "#3C3C3C",
                    "success": "#16A085",
                    "warning": "#F39C12",
                    "danger": "#E74C3C",
                    "text": "#FFFFFF",
                    "text_secondary": "#CCCCCC",
                    "border": "#3C3C3C",
                    "hover": "#3C3C3C",
                    "pressed": "#4C4C4C",
                    "display_bg": "#252526",
                    "display_text": "#FFFFFF",
                    "button_number": "#2D2D30",
                    "button_operator": "#0E639C",
                    "button_function": "#3C3C3C",
                    "button_special": "#16A085"
                }
            },
            
            "blue": {
                "name": "Blue Theme",
                "description": "Giao diện xanh dương chuyên nghiệp",
                "colors": {
                    "background": "#F0F8FF",
                    "surface": "#E6F3FF",
                    "primary": "#1E90FF",
                    "secondary": "#4682B4",
                    "success": "#20B2AA",
                    "warning": "#FFD700",
                    "danger": "#FF6347",
                    "text": "#191970",
                    "text_secondary": "#4682B4",
                    "border": "#B0E0E6",
                    "hover": "#E0F6FF",
                    "pressed": "#D0F0FF",
                    "display_bg": "#FFFFFF",
                    "display_text": "#191970",
                    "button_number": "#E6F3FF",
                    "button_operator": "#1E90FF",
                    "button_function": "#4682B4",
                    "button_special": "#20B2AA"
                }
            },
            
            "green": {
                "name": "Green Theme",
                "description": "Giao diện xanh lá mát mắt",
                "colors": {
                    "background": "#F0FFF0",
                    "surface": "#F5FFFA",
                    "primary": "#228B22",
                    "secondary": "#32CD32",
                    "success": "#00FF7F",
                    "warning": "#FFD700",
                    "danger": "#FF6347",
                    "text": "#006400",
                    "text_secondary": "#228B22",
                    "border": "#90EE90",
                    "hover": "#F0FFF0",
                    "pressed": "#E0FFE0",
                    "display_bg": "#FFFFFF",
                    "display_text": "#006400",
                    "button_number": "#F5FFFA",
                    "button_operator": "#228B22",
                    "button_function": "#32CD32",
                    "button_special": "#00FF7F"
                }
            }
        }
    
    def get_current_theme(self) -> Dict[str, Any]:
        return self.themes[self.current_theme]
    
    def set_theme(self, theme_name: str) -> bool:
        if theme_name in self.themes:
            self.current_theme = theme_name
            return True
        return False
    
    def get_available_themes(self) -> Dict[str, str]:
        return {
            name: config["description"] 
            for name, config in self.themes.items()
        }
    
    def get_color(self, color_name: str) -> str:
        theme = self.get_current_theme()
        return theme["colors"].get(color_name, "#000000")

class StyleManager:
    def __init__(self, theme_manager: ThemeManager):
        self.theme_manager = theme_manager
        self.fonts = {}
        self._initialize_fonts()
    
    def _initialize_fonts(self) -> None:
        try:
            self.fonts['display'] = font.Font(
                family=DISPLAY_FONT[0],
                size=DISPLAY_FONT[1],
                weight=DISPLAY_FONT[2] if len(DISPLAY_FONT) > 2 else "normal"
            )
            
            self.fonts['button'] = font.Font(
                family=BUTTON_FONT[0],
                size=BUTTON_FONT[1],
                weight=BUTTON_FONT[2] if len(BUTTON_FONT) > 2 else "normal"
            )
            
            self.fonts['menu'] = font.Font(
                family=MENU_FONT[0],
                size=MENU_FONT[1],
                weight="normal"
            )
            
            self.fonts['small'] = font.Font(
                family="Arial",
                size=9,
                weight="normal"
            )
            
            self.fonts['title'] = font.Font(
                family="Arial",
                size=16,
                weight="bold"
            )
            
        except Exception as e:
            self.fonts = {
                'display': ("Arial", 20, "bold"),
                'button': ("Arial", 14, "bold"),
                'menu': ("Arial", 10),
                'small': ("Arial", 9),
                'title': ("Arial", 16, "bold")
            }
    
    def get_font(self, font_name: str) -> Any:
        return self.fonts.get(font_name, self.fonts['button'])
    
    def get_button_style(self, button_type: str = "number") -> Dict[str, Any]:
        base_style = {
            'font': self.get_font('button'),
            'relief': 'raised',
            'borderwidth': 1,
            'cursor': 'hand2'
        }
        
        if button_type == "number":
            base_style.update({
                'bg': self.theme_manager.get_color('button_number'),
                'fg': self.theme_manager.get_color('text'),
                'activebackground': self.theme_manager.get_color('hover'),
                'activeforeground': self.theme_manager.get_color('text')
            })
        elif button_type == "operator":
            base_style.update({
                'bg': self.theme_manager.get_color('button_operator'),
                'fg': 'white',
                'activebackground': self.theme_manager.get_color('primary'),
                'activeforeground': 'white'
            })
        elif button_type == "function":
            base_style.update({
                'bg': self.theme_manager.get_color('button_function'),
                'fg': 'white',
                'activebackground': self.theme_manager.get_color('secondary'),
                'activeforeground': 'white'
            })
        elif button_type == "special":
            base_style.update({
                'bg': self.theme_manager.get_color('button_special'),
                'fg': 'white',
                'activebackground': self.theme_manager.get_color('success'),
                'activeforeground': 'white'
            })
        else:
            base_style.update({
                'bg': self.theme_manager.get_color('surface'),
                'fg': self.theme_manager.get_color('text'),
                'activebackground': self.theme_manager.get_color('hover'),
                'activeforeground': self.theme_manager.get_color('text')
            })
        
        return base_style
    
    def get_display_style(self) -> Dict[str, Any]:
        return {
            'font': self.get_font('display'),
            'bg': self.theme_manager.get_color('display_bg'),
            'fg': self.theme_manager.get_color('display_text'),
            'relief': 'sunken',
            'borderwidth': 2,
            'justify': 'right',
            'state': 'readonly'
        }
    
    def get_window_style(self) -> Dict[str, Any]:
        return {
            'bg': self.theme_manager.get_color('background'),
            'relief': 'flat'
        }
    
    def get_menu_style(self) -> Dict[str, Any]:
        return {
            'font': self.get_font('menu'),
            'bg': self.theme_manager.get_color('surface'),
            'fg': self.theme_manager.get_color('text'),
            'activebackground': self.theme_manager.get_color('primary'),
            'activeforeground': 'white'
        }
    
    def get_label_style(self, label_type: str = "normal") -> Dict[str, Any]:
        base_style = {
            'bg': self.theme_manager.get_color('background'),
            'fg': self.theme_manager.get_color('text')
        }
        
        if label_type == "title":
            base_style['font'] = self.get_font('title')
        elif label_type == "small":
            base_style['font'] = self.get_font('small')
            base_style['fg'] = self.theme_manager.get_color('text_secondary')
        else:
            base_style['font'] = self.get_font('menu')
        
        return base_style
    
    def apply_hover_effect(self, widget: tk.Widget, button_type: str = "number") -> None:
        original_bg = widget.cget('bg')
        hover_color = self.theme_manager.get_color('hover')
        
        if button_type == "operator":
            hover_color = self.theme_manager.get_color('primary')
        elif button_type == "function":
            hover_color = self.theme_manager.get_color('secondary')
        elif button_type == "special":
            hover_color = self.theme_manager.get_color('success')
        
        def on_enter(event):
            widget.config(bg=hover_color)
        
        def on_leave(event):
            widget.config(bg=original_bg)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def apply_press_effect(self, widget: tk.Widget) -> None:
        original_relief = widget.cget('relief')
        
        def on_press(event):
            widget.config(relief='sunken')
        
        def on_release(event):
            widget.config(relief=original_relief)
        
        widget.bind("<Button-1>", on_press)
        widget.bind("<ButtonRelease-1>", on_release)

_theme_manager = None
_style_manager = None

def get_theme_manager() -> ThemeManager:
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager

def get_style_manager() -> StyleManager:
    global _style_manager
    if _style_manager is None:
        theme_mgr = get_theme_manager()
        _style_manager = StyleManager(theme_mgr)
    return _style_manager

def apply_theme_to_widget(widget: tk.Widget, style_type: str, 
                         widget_type: str = "normal") -> None:
    style_mgr = get_style_manager()
    
    try:
        if style_type == "button":
            style = style_mgr.get_button_style(widget_type)
        elif style_type == "display":
            style = style_mgr.get_display_style()
        elif style_type == "window":
            style = style_mgr.get_window_style()
        elif style_type == "menu":
            style = style_mgr.get_menu_style()
        elif style_type == "label":
            style = style_mgr.get_label_style(widget_type)
        else:
            style = style_mgr.get_window_style()
        
        widget.config(**style)
        
    except Exception as e:
        try:
            widget.config(bg='white', fg='black')
        except:
            pass

def refresh_all_widgets(root_widget: tk.Widget) -> None:
    def refresh_widget(widget):
        if hasattr(widget, '_calculator_style_info'):
            style_type, widget_type = widget._calculator_style_info
            apply_theme_to_widget(widget, style_type, widget_type)
        
        for child in widget.winfo_children():
            refresh_widget(child)
    
    refresh_widget(root_widget)