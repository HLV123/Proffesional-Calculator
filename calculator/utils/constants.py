"""
Constants cho Calculator Application
Chứa các hằng số được sử dụng trong toàn bộ ứng dụng
"""

from typing import Dict, List, Tuple

# Thông tin ứng dụng
APP_NAME = "Professional Calculator"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Calculator Team"

# Cấu hình GUI
WINDOW_TITLE = "Máy Tính Chuyên Nghiệp"
WINDOW_SIZE = "400x500"
WINDOW_MIN_SIZE = (300, 400)

# Font configurations
DISPLAY_FONT = ("Arial", 20, "bold")
BUTTON_FONT = ("Arial", 14, "bold")
MENU_FONT = ("Arial", 10)

# Màu sắc giao diện
COLORS = {
    "primary": "#2C3E50",
    "secondary": "#34495E", 
    "accent": "#3498DB",
    "success": "#27AE60",
    "warning": "#F39C12",
    "danger": "#E74C3C",
    "light": "#ECF0F1",
    "dark": "#2C3E50",
    "background": "#FFFFFF",
    "text": "#2C3E50"
}

# Layout constants
BUTTON_PADDING = 5
BUTTON_HEIGHT = 2
BUTTON_WIDTH = 5
DISPLAY_HEIGHT = 2

# Toán tử và ký tự hợp lệ
OPERATORS: List[str] = ['+', '-', '*', '/', '(', ')']
NUMBERS: List[str] = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
SPECIAL_CHARS: List[str] = ['.', 'C', '=', 'CE', '±', '%']

# Button layout configuration
BUTTON_LAYOUT: List[List[str]] = [
    ['CE', 'C', '±', '/'],
    ['7', '8', '9', '*'],
    ['4', '5', '6', '-'],
    ['1', '2', '3', '+'],
    ['%', '0', '.', '=']
]

# Các phép toán được hỗ trợ
SUPPORTED_OPERATIONS: Dict[str, str] = {
    '+': 'addition',
    '-': 'subtraction', 
    '*': 'multiplication',
    '/': 'division',
    '%': 'modulo',
    '**': 'power',
    '//': 'floor_division'
}

# Độ ưu tiên của các toán tử
OPERATOR_PRECEDENCE: Dict[str, int] = {
    '(': 0,
    ')': 0,
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '//': 2,
    '**': 3,
    'unary-': 4  # Dấu âm
}

# Validation limits
MAX_EXPRESSION_LENGTH = 100
MAX_DECIMAL_PLACES = 10
MAX_NUMBER_VALUE = 1e10
MIN_NUMBER_VALUE = -1e10

# Error messages
ERROR_MESSAGES = {
    "syntax_error": "Lỗi cú pháp trong biểu thức",
    "division_by_zero": "Không thể chia cho 0",
    "overflow": "Số quá lớn",
    "underflow": "Số quá nhỏ", 
    "invalid_operation": "Phép toán không hợp lệ",
    "too_long": "Biểu thức quá dài",
    "invalid_character": "Ký tự không hợp lệ",
    "empty_expression": "Biểu thức trống"
}

# Logging configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = "calculator.log"