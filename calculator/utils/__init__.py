# calculator/utils/__init__.py
"""
Utility Modules
Chứa constants, exceptions, logger và utilities
"""

try:
    from utils.constants import *
    from utils.exceptions import (
        CalculatorError, ExpressionSyntaxError, DivisionByZeroError,
        NumberOverflowError, NumberUnderflowError, InvalidOperationError,
        ExpressionTooLongError, InvalidCharacterError, EmptyExpressionError,
        ParsingError, CalculationError
    )
    from utils.logger import get_logger, CalculatorLogger, logged
except ImportError:
    # Fallback for direct execution
    from utils.constants import *
    from utils.exceptions import (
        CalculatorError, ExpressionSyntaxError, DivisionByZeroError,
        NumberOverflowError, NumberUnderflowError, InvalidOperationError,
        ExpressionTooLongError, InvalidCharacterError, EmptyExpressionError,
        ParsingError, CalculationError
    )
    from utils.logger import get_logger, CalculatorLogger, logged

__all__ = [
    # Constants (tất cả từ constants.py)
    'APP_NAME', 'APP_VERSION', 'WINDOW_TITLE', 'COLORS', 'BUTTON_LAYOUT',
    'OPERATORS', 'NUMBERS', 'SUPPORTED_OPERATIONS', 'ERROR_MESSAGES',
    
    # Exceptions
    'CalculatorError', 'ExpressionSyntaxError', 'DivisionByZeroError',
    'NumberOverflowError', 'NumberUnderflowError', 'InvalidOperationError',
    'ExpressionTooLongError', 'InvalidCharacterError', 'EmptyExpressionError',
    'ParsingError', 'CalculationError',
    
    # Logger
    'get_logger', 'CalculatorLogger', 'logged'
]