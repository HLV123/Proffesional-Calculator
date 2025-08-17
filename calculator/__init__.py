# calculator/__init__.py
"""
Calculator Package
Professional Calculator Application với GUI hiện đại
"""

__version__ = "1.0.0"
__author__ = "Calculator Team"
__description__ = "Professional Calculator with Modern GUI"

# Import main components để dễ dàng access
try:
    from .core.calculator import CalculatorEngine
    from .gui.main_window import CalculatorMainWindow
    from .utils.logger import get_logger
except ImportError:
    # Fallback for direct execution
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    from core.calculator import CalculatorEngine
    from gui.main_window import CalculatorMainWindow
    from utils.logger import get_logger

__all__ = [
    'CalculatorEngine',
    'CalculatorMainWindow', 
    'get_logger'
]