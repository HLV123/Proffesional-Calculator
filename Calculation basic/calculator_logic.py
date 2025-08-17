# calculator_logic.py

def evaluate_expression(expression):
    """
    Evaluates a string expression and returns the result.
    This simple function uses Python's built-in `eval()` for ease of use.
    For a more robust solution, you would write your own parser
    to handle expressions safely.
    """
    try:
        # eval() is powerful but can be a security risk if used with untrusted input.
        # For a simple, local calculator, it's acceptable.
        result = eval(expression)
        return str(result)
    except (SyntaxError, ZeroDivisionError, TypeError):
        return "Error"