import re
from typing import List, Set, Tuple, Optional
from decimal import Decimal, InvalidOperation

from utils.constants import (
    OPERATORS, NUMBERS, SPECIAL_CHARS, MAX_EXPRESSION_LENGTH,
    MAX_NUMBER_VALUE, MIN_NUMBER_VALUE, SUPPORTED_OPERATIONS
)
from utils.exceptions import (
    ExpressionSyntaxError, ExpressionTooLongError, InvalidCharacterError,
    EmptyExpressionError, NumberOverflowError, NumberUnderflowError
)
from utils.logger import get_logger

class ExpressionValidator:
    def __init__(self):
        self.logger = get_logger("Validator")
        self.valid_chars: Set[str] = set(OPERATORS + NUMBERS + SPECIAL_CHARS + [' '])
        
        self.number_pattern = re.compile(r'^-?\d+\.?\d*$')
        self.operator_pattern = re.compile(r'^[+\-*/()%]$')
        self.consecutive_operators = re.compile(r'[+\-*/]{2,}')
        self.balanced_parentheses = re.compile(r'^[^()]*(\([^()]*\)[^()]*)*$')
    
    def validate_expression(self, expression: str) -> str:
        self.logger.debug(f"Validating expression: '{expression}'")
        
        if not expression or expression.strip() == "":
            raise EmptyExpressionError()
        
        sanitized = self._sanitize_input(expression)
        self._validate_length(sanitized)
        self._validate_characters(sanitized)
        self._validate_basic_syntax(sanitized)
        self._validate_advanced_syntax(sanitized)
        self._validate_numeric_values(sanitized)
        
        self.logger.info(f"Expression validated successfully: '{sanitized}'")
        return sanitized
    
    def _sanitize_input(self, expression: str) -> str:
        sanitized = re.sub(r'\s+', ' ', expression.strip())
        
        replacements = {
            '×': '*',
            '÷': '/',
            '−': '-',
            '–': '-',
            '—': '-',
        }
        
        for old, new in replacements.items():
            sanitized = sanitized.replace(old, new)
        
        sanitized = re.sub(r'\s*([+\-*/()%])\s*', r'\1', sanitized)
        
        return sanitized
    
    def _validate_length(self, expression: str) -> None:
        if len(expression) > MAX_EXPRESSION_LENGTH:
            raise ExpressionTooLongError(len(expression), MAX_EXPRESSION_LENGTH)
    
    def _validate_characters(self, expression: str) -> None:
        for i, char in enumerate(expression):
            if char not in self.valid_chars:
                raise InvalidCharacterError(char, i)
    
    def _validate_basic_syntax(self, expression: str) -> None:
        if expression[0] in ['*', '/', '%'] or expression[-1] in ['+', '-', '*', '/', '%']:
            raise ExpressionSyntaxError(expression, 0 if expression[0] in ['*', '/', '%'] else len(expression)-1)
        
        if self.consecutive_operators.search(expression):
            if not re.search(r'[+\-]\-', expression):
                match = self.consecutive_operators.search(expression)
                if match:
                    raise ExpressionSyntaxError(expression, match.start())
        
        self._validate_decimal_points(expression)
        self._validate_parentheses_balance(expression)
    
    def _validate_decimal_points(self, expression: str) -> None:
        invalid_decimal = re.compile(r'\d+\..*\.')
        if invalid_decimal.search(expression):
            match = invalid_decimal.search(expression)
            raise ExpressionSyntaxError(expression, match.start())
        
        if re.search(r'[+\-*/()%]\.\s*[+\-*/()%]', expression):
            raise ExpressionSyntaxError(expression)
    
    def _validate_parentheses_balance(self, expression: str) -> None:
        balance = 0
        for i, char in enumerate(expression):
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    raise ExpressionSyntaxError(expression, i)
        
        if balance != 0:
            raise ExpressionSyntaxError(expression)
    
    def _validate_advanced_syntax(self, expression: str) -> None:
        if '()' in expression:
            raise ExpressionSyntaxError(expression, expression.index('()'))
        
        if re.search(r'\d\(', expression):
            match = re.search(r'\d\(', expression)
            raise ExpressionSyntaxError(expression, match.start())
        
        if re.search(r'\)\d', expression):
            match = re.search(r'\)\d', expression)
            raise ExpressionSyntaxError(expression, match.start())
    
    def _validate_numeric_values(self, expression: str) -> None:
        number_pattern = re.compile(r'-?\d+\.?\d*')
        numbers = number_pattern.findall(expression)
        
        for num_str in numbers:
            if num_str and num_str not in ['-', '.', '-.']:
                try:
                    num_value = float(num_str)
                    
                    if num_value > MAX_NUMBER_VALUE:
                        raise NumberOverflowError(num_value, MAX_NUMBER_VALUE)
                    elif num_value < MIN_NUMBER_VALUE:
                        raise NumberUnderflowError(num_value, MIN_NUMBER_VALUE)
                        
                except ValueError:
                    raise ExpressionSyntaxError(expression)
    
    def validate_single_number(self, number_str: str) -> float:
        try:
            clean_str = number_str.strip()
            
            if not self.number_pattern.match(clean_str):
                raise InvalidCharacterError(number_str)
            
            value = float(clean_str)
            
            if value > MAX_NUMBER_VALUE:
                raise NumberOverflowError(value, MAX_NUMBER_VALUE)
            elif value < MIN_NUMBER_VALUE:
                raise NumberUnderflowError(value, MIN_NUMBER_VALUE)
            
            return value
            
        except ValueError as e:
            raise InvalidCharacterError(number_str) from e
    
    def is_valid_operator(self, operator: str) -> bool:
        return operator in SUPPORTED_OPERATIONS or operator in ['(', ')']
    
    def sanitize_for_display(self, expression: str) -> str:
        if not expression:
            return ""
        
        display_expr = expression
        for op in ['+', '-', '*', '/', '%']:
            display_expr = display_expr.replace(op, f' {op} ')
        
        display_expr = re.sub(r'\s+', ' ', display_expr).strip()
        
        return display_expr
    
    def extract_numbers_and_operators(self, expression: str) -> Tuple[List[str], List[str]]:
        numbers = re.findall(r'-?\d+\.?\d*', expression)
        operators = re.findall(r'[+\-*/()%]', expression)
        
        numbers = [n for n in numbers if n and n not in ['-', '.']]
        
        return numbers, operators

class InputSanitizer:
    def __init__(self):
        self.logger = get_logger("Sanitizer")
        self.validator = ExpressionValidator()
    
    def sanitize_calculator_input(self, user_input: str) -> str:
        if not user_input:
            return ""
        
        sanitized = self._remove_dangerous_chars(user_input)
        sanitized = self._normalize_operators(sanitized)
        sanitized = self._clean_whitespace(sanitized)
        
        self.logger.debug(f"Sanitized input: '{user_input}' -> '{sanitized}'")
        return sanitized
    
    def _remove_dangerous_chars(self, text: str) -> str:
        dangerous_chars = ['<', '>', '&', '"', "'", '`', '\\', ';', '|']
        
        result = text
        for char in dangerous_chars:
            result = result.replace(char, '')
        
        return result
    
    def _normalize_operators(self, text: str) -> str:
        operator_map = {
            'x': '*',
            'X': '*',
            '×': '*',
            '÷': '/',
            ':': '/',
            '−': '-',
            '–': '-',
            '—': '-',
        }
        
        result = text
        for old, new in operator_map.items():
            result = result.replace(old, new)
        
        return result
    
    def _clean_whitespace(self, text: str) -> str:
        result = text.strip()
        result = re.sub(r'\s+', ' ', result)
        
        return result
    
    def validate_and_sanitize(self, user_input: str) -> str:
        sanitized = self.sanitize_calculator_input(user_input)
        validated = self.validator.validate_expression(sanitized)
        
        return validated