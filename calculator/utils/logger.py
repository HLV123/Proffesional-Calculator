import logging
import logging.handlers
import os
import sys
from typing import Optional
from datetime import datetime

try:
    import colorlog
    COLORLOG_AVAILABLE = True
except ImportError:
    COLORLOG_AVAILABLE = False

from utils.constants import LOG_LEVEL, LOG_FORMAT, LOG_FILE

class CalculatorLogger:
    def __init__(self, name: str = "Calculator", log_level: str = LOG_LEVEL):
        self.name = name
        self.log_level = getattr(logging, log_level.upper())
        self.logger = logging.getLogger(name)
        self.logger.setLevel(self.log_level)
        
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self) -> None:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        if COLORLOG_AVAILABLE:
            color_formatter = colorlog.ColoredFormatter(
                '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors={
                    'DEBUG': 'cyan',
                    'INFO': 'green',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'red,bg_white',
                }
            )
            console_handler.setFormatter(color_formatter)
        else:
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(console_formatter)
        
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_path = os.path.join(log_dir, LOG_FILE)
        file_handler = logging.handlers.RotatingFileHandler(
            file_path,
            maxBytes=10*1024*1024,
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        file_formatter = logging.Formatter(
            LOG_FORMAT,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def get_logger(self) -> logging.Logger:
        return self.logger
    
    def debug(self, message: str, *args, **kwargs) -> None:
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        self.logger.critical(message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs) -> None:
        self.logger.exception(message, *args, **kwargs)

_loggers = {}

def get_logger(name: str = "Calculator", log_level: Optional[str] = None) -> CalculatorLogger:
    if name not in _loggers:
        level = log_level or LOG_LEVEL
        _loggers[name] = CalculatorLogger(name, level)
    
    return _loggers[name]

def log_function_call(func_name: str, args: Optional[tuple] = None, 
                     kwargs: Optional[dict] = None) -> None:
    logger = get_logger("FunctionCall")
    
    log_msg = f"Gọi hàm: {func_name}"
    if args:
        log_msg += f" với args: {args}"
    if kwargs:
        log_msg += f" với kwargs: {kwargs}"
    
    logger.debug(log_msg)

def log_calculation_step(step: str, expression: str, result: str) -> None:
    logger = get_logger("Calculation")
    logger.debug(f"Bước {step}: '{expression}' -> '{result}'")

def log_error_with_context(error: Exception, context: dict) -> None:
    logger = get_logger("Error")
    
    error_msg = f"Lỗi: {type(error).__name__}: {str(error)}"
    
    if context:
        error_msg += f"\nContext: {context}"
    
    logger.error(error_msg)
    logger.exception("Chi tiết lỗi:")

def logged(logger_name: str = "Calculator"):
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            func_name = func.__name__
            
            logger.debug(f"Bắt đầu thực hiện: {func_name}")
            
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Hoàn thành: {func_name}")
                return result
            except Exception as e:
                logger.error(f"Lỗi trong {func_name}: {str(e)}")
                raise
        
        return wrapper
    return decorator