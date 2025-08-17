"""
Custom Exceptions cho Calculator Application
Định nghĩa các exception chuyên biệt cho từng loại lỗi
"""

from typing import Optional


class CalculatorError(Exception):
    """
    Base exception class cho tất cả calculator errors
    Tất cả custom exceptions sẽ kế thừa từ class này
    """
    def __init__(self, message: str, error_code: Optional[str] = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class ExpressionSyntaxError(CalculatorError):
    """
    Exception được raise khi biểu thức có lỗi cú pháp
    Ví dụ: '1 + + 2', '(1 + 2', '1 2 3'
    """
    def __init__(self, expression: str, position: Optional[int] = None):
        self.expression = expression
        self.position = position
        message = f"Lỗi cú pháp trong biểu thức: '{expression}'"
        if position is not None:
            message += f" tại vị trí {position}"
        super().__init__(message, "SYNTAX_ERROR")


class DivisionByZeroError(CalculatorError):
    """
    Exception được raise khi chia cho 0
    """
    def __init__(self, expression: str = ""):
        self.expression = expression
        message = "Không thể chia cho 0"
        if expression:
            message += f" trong biểu thức: '{expression}'"
        super().__init__(message, "DIVISION_BY_ZERO")


class NumberOverflowError(CalculatorError):
    """
    Exception được raise khi số quá lớn (overflow)
    """
    def __init__(self, value: float, max_value: float):
        self.value = value
        self.max_value = max_value
        message = f"Số {value} vượt quá giá trị tối đa cho phép {max_value}"
        super().__init__(message, "NUMBER_OVERFLOW")


class NumberUnderflowError(CalculatorError):
    """
    Exception được raise khi số quá nhỏ (underflow)
    """
    def __init__(self, value: float, min_value: float):
        self.value = value
        self.min_value = min_value
        message = f"Số {value} nhỏ hơn giá trị tối thiểu cho phép {min_value}"
        super().__init__(message, "NUMBER_UNDERFLOW")


class InvalidOperationError(CalculatorError):
    """
    Exception được raise khi thực hiện phép toán không hợp lệ
    Ví dụ: căn bậc hai của số âm, log của số âm
    """
    def __init__(self, operation: str, operands: Optional[str] = None):
        self.operation = operation
        self.operands = operands
        message = f"Phép toán không hợp lệ: {operation}"
        if operands:
            message += f" với toán hạng: {operands}"
        super().__init__(message, "INVALID_OPERATION")


class ExpressionTooLongError(CalculatorError):
    """
    Exception được raise khi biểu thức quá dài
    """
    def __init__(self, length: int, max_length: int):
        self.length = length
        self.max_length = max_length
        message = f"Biểu thức dài {length} ký tự, vượt quá giới hạn {max_length} ký tự"
        super().__init__(message, "EXPRESSION_TOO_LONG")


class InvalidCharacterError(CalculatorError):
    """
    Exception được raise khi gặp ký tự không hợp lệ
    """
    def __init__(self, character: str, position: Optional[int] = None):
        self.character = character
        self.position = position
        message = f"Ký tự không hợp lệ: '{character}'"
        if position is not None:
            message += f" tại vị trí {position}"
        super().__init__(message, "INVALID_CHARACTER")


class EmptyExpressionError(CalculatorError):
    """
    Exception được raise khi biểu thức rỗng
    """
    def __init__(self):
        message = "Biểu thức không được để trống"
        super().__init__(message, "EMPTY_EXPRESSION")


class ParsingError(CalculatorError):
    """
    Exception được raise khi không thể parse biểu thức
    """
    def __init__(self, expression: str, reason: str = ""):
        self.expression = expression
        self.reason = reason
        message = f"Không thể phân tích biểu thức: '{expression}'"
        if reason:
            message += f". Lý do: {reason}"
        super().__init__(message, "PARSING_ERROR")


class CalculationError(CalculatorError):
    """
    Exception được raise khi có lỗi trong quá trình tính toán
    """
    def __init__(self, expression: str, step: str = "", original_error: Optional[Exception] = None):
        self.expression = expression
        self.step = step
        self.original_error = original_error
        message = f"Lỗi tính toán trong biểu thức: '{expression}'"
        if step:
            message += f" tại bước: {step}"
        if original_error:
            message += f". Lỗi gốc: {str(original_error)}"
        super().__init__(message, "CALCULATION_ERROR")