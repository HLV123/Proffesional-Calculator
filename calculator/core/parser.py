import re
from typing import List, Union, Optional, Tuple
from decimal import Decimal, getcontext, InvalidOperation
from math import sqrt, pow, log, sin, cos, tan, factorial

from utils.constants import OPERATOR_PRECEDENCE, SUPPORTED_OPERATIONS
from utils.exceptions import (
    ExpressionSyntaxError, DivisionByZeroError, InvalidOperationError,
    ParsingError, CalculationError, NumberOverflowError
)
from utils.logger import get_logger, logged

getcontext().prec = 28

class Token:
    def __init__(self, value: str, token_type: str, position: int = 0):
        self.value = value
        self.type = token_type
        self.position = position
    
    def __repr__(self) -> str:
        return f"Token({self.value}, {self.type})"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Token):
            return False
        return self.value == other.value and self.type == other.type

class ExpressionTokenizer:
    def __init__(self):
        self.logger = get_logger("Tokenizer")
        
        self.patterns = {
            'number': re.compile(r'\d+\.?\d*'),
            'operator': re.compile(r'[+\-*/()%^]'),
            'function': re.compile(r'(sqrt|sin|cos|tan|log|abs|fact)\('),
            'whitespace': re.compile(r'\s+')
        }
    
    @logged("Tokenizer")
    def tokenize(self, expression: str) -> List[Token]:
        tokens = []
        position = 0
        
        while position < len(expression):
            if expression[position].isspace():
                position += 1
                continue
            
            if expression[position].isdigit() or expression[position] == '.':
                token, new_pos = self._parse_number(expression, position)
                tokens.append(token)
                position = new_pos
                continue
            
            if expression[position] in '+-*/()%^':
                token = Token(expression[position], 'operator', position)
                tokens.append(token)
                position += 1
                continue
            
            func_match = self._match_function(expression, position)
            if func_match:
                func_name, new_pos = func_match
                token = Token(func_name, 'function', position)
                tokens.append(token)
                position = new_pos
                continue
            
            raise ParsingError(expression, f"Ký tự không nhận diện: '{expression[position]}' tại vị trí {position}")
        
        self.logger.debug(f"Tokenized '{expression}' into {len(tokens)} tokens")
        return tokens
    
    def _parse_number(self, expression: str, start_pos: int) -> Tuple[Token, int]:
        end_pos = start_pos
        has_decimal = False
        
        if expression[start_pos] == '-':
            end_pos += 1
        
        while end_pos < len(expression):
            char = expression[end_pos]
            
            if char.isdigit():
                end_pos += 1
            elif char == '.' and not has_decimal:
                has_decimal = True
                end_pos += 1
            else:
                break
        
        number_str = expression[start_pos:end_pos]
        token = Token(number_str, 'number', start_pos)
        
        return token, end_pos
    
    def _match_function(self, expression: str, position: int) -> Optional[Tuple[str, int]]:
        functions = ['sqrt', 'sin', 'cos', 'tan', 'log', 'abs', 'fact']
        
        for func in functions:
            if expression[position:].startswith(func):
                return func, position + len(func)
        
        return None

class ExpressionParser:
    def __init__(self):
        self.logger = get_logger("Parser")
        self.tokenizer = ExpressionTokenizer()
    
    @logged("Parser")
    def parse(self, expression: str) -> List[Token]:
        try:
            tokens = self.tokenizer.tokenize(expression)
            postfix = self._infix_to_postfix(tokens)
            
            self.logger.info(f"Parsed expression successfully: {len(postfix)} tokens")
            return postfix
            
        except Exception as e:
            self.logger.error(f"Parsing failed for '{expression}': {str(e)}")
            raise ParsingError(expression, str(e)) from e
    
    def _infix_to_postfix(self, tokens: List[Token]) -> List[Token]:
        output_queue = []
        operator_stack = []
        
        for token in tokens:
            if token.type == 'number':
                output_queue.append(token)
                
            elif token.type == 'function':
                operator_stack.append(token)
                
            elif token.type == 'operator':
                if token.value == '(':
                    operator_stack.append(token)
                    
                elif token.value == ')':
                    while (operator_stack and 
                           operator_stack[-1].value != '('):
                        output_queue.append(operator_stack.pop())
                    
                    if not operator_stack:
                        raise ParsingError("", "Dấu ngoặc không cân bằng")
                    
                    operator_stack.pop()
                    
                    if (operator_stack and 
                        operator_stack[-1].type == 'function'):
                        output_queue.append(operator_stack.pop())
                        
                else:
                    while (operator_stack and
                           self._has_higher_precedence(operator_stack[-1], token)):
                        output_queue.append(operator_stack.pop())
                    
                    operator_stack.append(token)
        
        while operator_stack:
            if operator_stack[-1].value in '()':
                raise ParsingError("", "Dấu ngoặc không cân bằng")
            output_queue.append(operator_stack.pop())
        
        return output_queue
    
    def _has_higher_precedence(self, op1: Token, op2: Token) -> bool:
        if op1.type == 'function':
            return True
        
        if op1.value == '(' or op2.value == ')':
            return False
        
        prec1 = OPERATOR_PRECEDENCE.get(op1.value, 0)
        prec2 = OPERATOR_PRECEDENCE.get(op2.value, 0)
        
        return prec1 >= prec2

class ExpressionEvaluator:
    def __init__(self):
        self.logger = get_logger("Evaluator")
    
    @logged("Evaluator")
    def evaluate(self, postfix_tokens: List[Token]) -> Decimal:
        if not postfix_tokens:
            return Decimal('0')
        
        stack = []
        
        try:
            for token in postfix_tokens:
                if token.type == 'number':
                    value = Decimal(token.value)
                    stack.append(value)
                    
                elif token.type == 'operator':
                    result = self._perform_operation(token.value, stack)
                    stack.append(result)
                    
                elif token.type == 'function':
                    result = self._perform_function(token.value, stack)
                    stack.append(result)
            
            if len(stack) != 1:
                raise CalculationError("", "Lỗi cấu trúc biểu thức")
            
            result = stack[0]
            self.logger.info(f"Evaluation completed: {result}")
            return result
            
        except Exception as e:
            self.logger.error(f"Evaluation failed: {str(e)}")
            raise CalculationError("", str(e)) from e
    
    def _perform_operation(self, operator: str, stack: List[Decimal]) -> Decimal:
        if len(stack) < 2:
            raise CalculationError("", f"Không đủ operand cho toán tử {operator}")
        
        b = stack.pop()
        a = stack.pop()
        
        try:
            if operator == '+':
                return a + b
            elif operator == '-':
                return a - b
            elif operator == '*':
                return a * b
            elif operator == '/':
                if b == 0:
                    raise DivisionByZeroError()
                return a / b
            elif operator == '%':
                if b == 0:
                    raise DivisionByZeroError()
                return a % b
            elif operator == '^' or operator == '**':
                return Decimal(str(pow(float(a), float(b))))
            else:
                raise InvalidOperationError(operator, f"{a} {operator} {b}")
                
        except (InvalidOperation, OverflowError) as e:
            raise NumberOverflowError(float(a), 1e10) from e
    
    def _perform_function(self, function: str, stack: List[Decimal]) -> Decimal:
        if len(stack) < 1:
            raise CalculationError("", f"Không đủ operand cho function {function}")
        
        a = stack.pop()
        a_float = float(a)
        
        try:
            if function == 'sqrt':
                if a_float < 0:
                    raise InvalidOperationError(function, str(a))
                return Decimal(str(sqrt(a_float)))
                
            elif function == 'abs':
                return abs(a)
                
            elif function == 'sin':
                return Decimal(str(sin(a_float)))
                
            elif function == 'cos':
                return Decimal(str(cos(a_float)))
                
            elif function == 'tan':
                return Decimal(str(tan(a_float)))
                
            elif function == 'log':
                if a_float <= 0:
                    raise InvalidOperationError(function, str(a))
                return Decimal(str(log(a_float)))
                
            elif function == 'fact':
                if a_float < 0 or a_float != int(a_float):
                    raise InvalidOperationError(function, str(a))
                return Decimal(str(factorial(int(a_float))))
                
            else:
                raise InvalidOperationError(function, str(a))
                
        except (ValueError, OverflowError) as e:
            raise CalculationError("", f"Lỗi function {function}: {str(e)}") from e

class SafeCalculatorEngine:
    def __init__(self):
        self.logger = get_logger("CalculatorEngine")
        self.parser = ExpressionParser()
        self.evaluator = ExpressionEvaluator()
    
    @logged("CalculatorEngine")
    def calculate(self, expression: str) -> str:
        self.logger.info(f"Calculating expression: '{expression}'")
        
        try:
            postfix_tokens = self.parser.parse(expression)
            result = self.evaluator.evaluate(postfix_tokens)
            result_str = self._format_result(result)
            
            self.logger.info(f"Calculation successful: '{expression}' = {result_str}")
            return result_str
            
        except Exception as e:
            self.logger.error(f"Calculation failed: {str(e)}")
            raise
    
    def _format_result(self, result: Decimal) -> str:
        result_str = str(result.normalize())
        
        if '.' in result_str and result_str.endswith('.0'):
            result_str = result_str[:-2]
        
        return result_str