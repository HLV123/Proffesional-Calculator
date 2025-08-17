from typing import Optional, List, Dict, Any
from decimal import Decimal
import json
from datetime import datetime

from core.parser import SafeCalculatorEngine
from core.validator import InputSanitizer, ExpressionValidator
from utils.constants import ERROR_MESSAGES, MAX_EXPRESSION_LENGTH
from utils.exceptions import (
    CalculatorError, ExpressionSyntaxError, DivisionByZeroError,
    NumberOverflowError, NumberUnderflowError, InvalidOperationError,
    EmptyExpressionError
)
from utils.logger import get_logger, logged, log_calculation_step, log_error_with_context

class CalculationHistory:
    def __init__(self, max_entries: int = 100):
        self.max_entries = max_entries
        self.history: List[Dict[str, Any]] = []
        self.logger = get_logger("History")
    
    def add_calculation(self, expression: str, result: str, 
                       calculation_time: Optional[datetime] = None) -> None:
        if calculation_time is None:
            calculation_time = datetime.now()
        
        entry = {
            'expression': expression,
            'result': result,
            'timestamp': calculation_time.isoformat(),
            'formatted_time': calculation_time.strftime("%H:%M:%S %d/%m/%Y")
        }
        
        self.history.append(entry)
        
        if len(self.history) > self.max_entries:
            self.history.pop(0)
        
        self.logger.debug(f"Added to history: {expression} = {result}")
    
    def get_last_calculation(self) -> Optional[Dict[str, Any]]:
        return self.history[-1] if self.history else None
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        if limit:
            return self.history[-limit:]
        return self.history.copy()
    
    def clear_history(self) -> None:
        self.history.clear()
        self.logger.info("History cleared")
    
    def export_to_json(self) -> str:
        return json.dumps(self.history, indent=2, ensure_ascii=False)
    
    def import_from_json(self, json_str: str) -> int:
        try:
            imported_data = json.loads(json_str)
            
            if not isinstance(imported_data, list):
                raise ValueError("JSON data phải là một list")
            
            count = 0
            for entry in imported_data:
                if self._validate_history_entry(entry):
                    self.history.append(entry)
                    count += 1
            
            if len(self.history) > self.max_entries:
                self.history = self.history[-self.max_entries:]
            
            self.logger.info(f"Imported {count} history entries")
            return count
            
        except (json.JSONDecodeError, ValueError) as e:
            self.logger.error(f"Failed to import history: {str(e)}")
            raise ValueError(f"Không thể import lịch sử: {str(e)}")
    
    def _validate_history_entry(self, entry: Dict[str, Any]) -> bool:
        required_fields = ['expression', 'result', 'timestamp']
        return (isinstance(entry, dict) and 
                all(field in entry for field in required_fields))

class CalculatorEngine:
    def __init__(self):
        self.logger = get_logger("CalculatorEngine")
        
        self.sanitizer = InputSanitizer()
        self.validator = ExpressionValidator()
        self.calculation_engine = SafeCalculatorEngine()
        self.history = CalculationHistory()
        
        self.current_expression = ""
        self.last_result = "0"
        self.memory_value = Decimal('0')
        self.is_error_state = False
        
        self.logger.info("Calculator engine initialized")
    
    @logged("CalculatorEngine")
    def calculate_expression(self, expression: str) -> str:
        if not expression or expression.strip() == "":
            return "0"
        
        try:
            self.is_error_state = False
            
            sanitized = self.sanitizer.sanitize_calculator_input(expression)
            log_calculation_step("Sanitize", expression, sanitized)
            
            validated = self.validator.validate_expression(sanitized)
            log_calculation_step("Validate", sanitized, validated)
            
            result = self.calculation_engine.calculate(validated)
            log_calculation_step("Calculate", validated, result)
            
            self.current_expression = validated
            self.last_result = result
            self.history.add_calculation(validated, result)
            
            self.logger.info(f"Calculation successful: '{expression}' = {result}")
            return result
            
        except CalculatorError as e:
            self.is_error_state = True
            error_msg = self._get_user_friendly_error(e)
            
            log_error_with_context(e, {
                'expression': expression,
                'error_type': type(e).__name__,
                'error_code': getattr(e, 'error_code', None)
            })
            
            return error_msg
            
        except Exception as e:
            self.is_error_state = True
            self.logger.error(f"Unexpected error calculating '{expression}': {str(e)}")
            return "Lỗi không xác định"
    
    def _get_user_friendly_error(self, error: CalculatorError) -> str:
        error_code = getattr(error, 'error_code', None)
        
        if error_code in ERROR_MESSAGES:
            return ERROR_MESSAGES[error_code]
        
        if isinstance(error, ExpressionSyntaxError):
            return "Lỗi cú pháp"
        elif isinstance(error, DivisionByZeroError):
            return "Không thể chia cho 0"
        elif isinstance(error, NumberOverflowError):
            return "Số quá lớn"
        elif isinstance(error, NumberUnderflowError):
            return "Số quá nhỏ"
        elif isinstance(error, InvalidOperationError):
            return "Phép toán không hợp lệ"
        elif isinstance(error, EmptyExpressionError):
            return "0"
        else:
            return "Lỗi"
    
    def handle_button_press(self, button_value: str) -> str:
        self.logger.debug(f"Button pressed: {button_value}")
        
        try:
            if button_value == 'C':
                return self._handle_clear()
            elif button_value == 'CE':
                return self._handle_clear_entry()
            elif button_value == '=':
                return self._handle_equals()
            elif button_value == '±':
                return self._handle_plus_minus()
            elif button_value == '%':
                return self._handle_percentage()
            elif button_value in '0123456789.':
                return self._handle_number(button_value)
            elif button_value in '+-*/':
                return self._handle_operator(button_value)
            elif button_value in '()':
                return self._handle_parenthesis(button_value)
            else:
                self.logger.warning(f"Unknown button: {button_value}")
                return self.current_expression
                
        except Exception as e:
            self.logger.error(f"Error handling button '{button_value}': {str(e)}")
            return "Lỗi"
    
    def _handle_clear(self) -> str:
        self.current_expression = ""
        self.last_result = "0"
        self.is_error_state = False
        self.logger.debug("Calculator cleared")
        return "0"
    
    def _handle_clear_entry(self) -> str:
        if self.current_expression:
            self.current_expression = self.current_expression[:-1]
        
        if not self.current_expression:
            return "0"
        
        return self.current_expression
    
    def _handle_equals(self) -> str:
        if not self.current_expression:
            return self.last_result
        
        result = self.calculate_expression(self.current_expression)
        
        if not self.is_error_state:
            self.current_expression = ""
        
        return result
    
    def _handle_plus_minus(self) -> str:
        if not self.current_expression:
            if self.last_result != "0":
                try:
                    value = Decimal(self.last_result)
                    result = str(-value)
                    return result
                except:
                    return self.last_result
            return "0"
        
        if self.current_expression.startswith('-'):
            self.current_expression = self.current_expression[1:]
        else:
            self.current_expression = '-' + self.current_expression
        
        return self.current_expression
    
    def _handle_percentage(self) -> str:
        if not self.current_expression:
            if self.last_result != "0":
                try:
                    value = Decimal(self.last_result)
                    result = str(value / 100)
                    return result
                except:
                    return self.last_result
            return "0"
        
        self.current_expression += "/100"
        return self.current_expression
    
    def _handle_number(self, digit: str) -> str:
        if self.is_error_state:
            self.current_expression = ""
            self.is_error_state = False
        
        if len(self.current_expression) >= MAX_EXPRESSION_LENGTH:
            return self.current_expression
        
        if digit == '.':
            last_number = self._get_last_number()
            if '.' in last_number:
                return self.current_expression
        
        self.current_expression += digit
        return self.current_expression
    
    def _handle_operator(self, operator: str) -> str:
        if self.is_error_state:
            self.is_error_state = False
            self.current_expression = self.last_result
        
        if not self.current_expression:
            if operator == '-':
                self.current_expression = '-'
                return self.current_expression
            else:
                self.current_expression = self.last_result
        
        if (self.current_expression and 
            self.current_expression[-1] in '+-*/' and 
            operator != '-'):
            self.current_expression = self.current_expression[:-1]
        
        self.current_expression += operator
        return self.current_expression
    
    def _handle_parenthesis(self, paren: str) -> str:
        if self.is_error_state:
            self.current_expression = ""
            self.is_error_state = False
        
        self.current_expression += paren
        return self.current_expression
    
    def _get_last_number(self) -> str:
        if not self.current_expression:
            return ""
        
        parts = self.current_expression.replace('+', ' ').replace('-', ' ').replace('*', ' ').replace('/', ' ').split()
        
        return parts[-1] if parts else ""
    
    def memory_store(self, value: Optional[str] = None) -> None:
        try:
            if value is None:
                value = self.last_result
            
            self.memory_value = Decimal(value)
            self.logger.debug(f"Stored in memory: {self.memory_value}")
            
        except:
            self.logger.warning(f"Cannot store invalid value in memory: {value}")
    
    def memory_recall(self) -> str:
        return str(self.memory_value)
    
    def memory_clear(self) -> None:
        self.memory_value = Decimal('0')
        self.logger.debug("Memory cleared")
    
    def memory_add(self, value: Optional[str] = None) -> None:
        try:
            if value is None:
                value = self.last_result
            
            self.memory_value += Decimal(value)
            self.logger.debug(f"Added to memory: {value}, new value: {self.memory_value}")
            
        except:
            self.logger.warning(f"Cannot add invalid value to memory: {value}")
    
    def memory_subtract(self, value: Optional[str] = None) -> None:
        try:
            if value is None:
                value = self.last_result
            
            self.memory_value -= Decimal(value)
            self.logger.debug(f"Subtracted from memory: {value}, new value: {self.memory_value}")
            
        except:
            self.logger.warning(f"Cannot subtract invalid value from memory: {value}")
    
    def get_current_state(self) -> Dict[str, Any]:
        return {
            'current_expression': self.current_expression,
            'last_result': self.last_result,
            'memory_value': str(self.memory_value),
            'is_error_state': self.is_error_state,
            'history_count': len(self.history.history)
        }
    
    def reset(self) -> None:
        self.current_expression = ""
        self.last_result = "0"
        self.memory_value = Decimal('0')
        self.is_error_state = False
        self.history.clear_history()
        self.logger.info("Calculator reset to initial state")