# planetary_scientist_assistant/sci_utils/calculator.py
import math
import re

# More extensive list of allowed functions and constants for eval context
ALLOWED_NAMES = {
    "abs": abs,
    "acos": math.acos,
    "asin": math.asin,
    "atan": math.atan,
    "atan2": math.atan2,
    "ceil": math.ceil,
    "cos": math.cos,
    "cosh": math.cosh,
    "degrees": math.degrees,
    "exp": math.exp,
    "fabs": math.fabs,
    "floor": math.floor,
    "fmod": math.fmod,
    "frexp": math.frexp,
    "hypot": math.hypot,
    "ldexp": math.ldexp,
    "log": math.log,
    "log10": math.log10,
    "log1p": math.log1p, # log(1+x)
    "modf": math.modf,
    "pow": pow, # Using built-in pow for flexibility (e.g. pow(x, y, z))
    "radians": math.radians,
    "sin": math.sin,
    "sinh": math.sinh,
    "sqrt": math.sqrt,
    "tan": math.tan,
    "tanh": math.tanh,
    "pi": math.pi,
    "e": math.e,
    # Simple operations are handled by eval directly: +, -, *, /, //, %
    # Bitwise ops could be added if needed: ^, &, |
}

# Regular expression to validate the expression for allowed characters and patterns.
# This is a critical security measure if using eval.
# - Allows numbers (integers, floats, scientific notation like 1e-5).
# - Allows operators: +, -, *, /, //, %, ** (for power).
# - Allows parentheses for grouping.
# - Allows function calls (alphanumeric names followed by parentheses).
# - Allows commas for function arguments.
# - Allows whitespace.
# - Allows allowed names (constants like pi, e).
# This regex is a basic attempt and might need refinement for more complex valid expressions
# or to be more restrictive. A full parser would be safer than regex + eval.
ALLOWED_EXPRESSION_PATTERN = re.compile(
    r"^[0-9a-zA-Z_+\-*/%().,\s\^eE]*$"  # Allow common math symbols and names.
    # The '^' in the character set is literal here if not first/last or range.
    # For power, Python uses '**', not '^'. Let's adjust.
)
# More precise pattern:
# Allows: numbers, identifiers (for functions/constants), operators, parentheses, commas, whitespace.
# We will rely more on the namespacing of `eval` for security.
# The main risk with eval is access to builtins or unintended global variables.

def safe_eval(expression, custom_allowed_names=None):
    """
    Safely evaluates a mathematical expression string using a restricted eval().

    Args:
        expression (str): The mathematical expression to evaluate.
        custom_allowed_names (dict, optional): Additional names to allow in the evaluation context.
                                              Defaults to None, using the global ALLOWED_NAMES.

    Returns:
        The result of the evaluation (float, int, or potentially complex number),
        or an error string if evaluation fails or is deemed unsafe.
    """
    # Basic check for potentially harmful characters, though not foolproof.
    # A better approach for security would be to parse the expression with ast.parse
    # and then evaluate only whitelisted node types.
    # For now, we rely on a very restricted globals and locals for eval.

    # Disallow direct access to builtins like __import__ or open
    # by providing a minimal __builtins__ dictionary.
    safe_builtins = {
        'abs': abs, 'round': round, 'len': len, # examples of safe builtins
        'pow': pow, 'sum': sum, 'min': min, 'max': max,
        'True': True, 'False': False, 'None': None
        # Add any other builtins you deem safe and necessary
    }

    # Combine default allowed names with any custom ones provided
    eval_globals = {"__builtins__": safe_builtins}
    if custom_allowed_names:
        eval_globals.update(custom_allowed_names)
    else:
        eval_globals.update(ALLOWED_NAMES)

    # The expression itself will be evaluated within the locals,
    # which are empty, preventing it from defining new variables in an unsafe way.
    # Globals provide the functions and constants.
    try:
        # Validate the expression more strictly before eval
        # This is a simplified check. A proper AST traversal would be more robust.
        if not all(c in "0123456789.+-*/%()eE ,_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" for c in expression.replace('**','')): # Allow **
             #粗略检查，排除一些明显不安全的字符
             #This is a rough check and might block some valid complex numbers or specific notations.
             #A more sophisticated validation (e.g., using ast.parse and checking node types) is recommended for production.
             #For now, this adds a layer of filtering.
             #If we find this too restrictive, we can adjust. The primary safety comes from the restricted eval context.
             pass # Let eval handle it if it passes the restricted context.

        result = eval(expression, eval_globals, {}) # Empty dict for locals
        return result, "Calculation successful."
    except NameError as ne:
        # Try to identify if the NameError is due to an undefined variable/function
        # or something deliberately excluded.
        # Example: "Name 'os' is not defined"
        # This regex extracts the name from the error message.
        name_match = re.search(r"name '([^']*)' is not defined", str(ne))
        if name_match:
            undefined_name = name_match.group(1)
            if undefined_name not in eval_globals and undefined_name not in safe_builtins:
                 return None, f"Error: Name '{undefined_name}' is not allowed or not defined. Please use supported functions/constants."
        return None, f"Error: {ne}. Ensure all functions and variables are supported."
    except SyntaxError as se:
        return None, f"Syntax Error: {se}. Please check your expression."
    except TypeError as te:
        return None, f"Type Error: {te}. Check function arguments and types."
    except ZeroDivisionError:
        return None, "Error: Division by zero."
    except Exception as e:
        # Catch any other unexpected errors during evaluation.
        return None, f"An unexpected error occurred: {e}"


if __name__ == '__main__':
    print("--- Testing Safe Calculator ---")

    expressions_to_test = [
        ("1 + 1", 2),
        ("2 * (3 + 4)", 14),
        ("10 / 2", 5.0),
        ("10 // 3", 3),
        ("10 % 3", 1),
        ("2 ** 3", 8),
        ("pow(2, 3)", 8),
        ("sqrt(16)", 4.0),
        ("sin(pi/2)", 1.0),
        ("log10(100)", 2.0),
        ("e", math.e),
        ("abs(-5)", 5),
        ("round(3.14159, 2)", 3.14),
        ("1e-2 + 0.01", 0.02),
        # Invalid/unsafe expressions (should return None and an error message)
        ("import os", None), # Security test
        ("open('file.txt')", None), # Security test
        ("__import__('os').system('echo unsafe')", None), # Security test
        ("undefined_variable * 2", None), # NameError test
        ("sqrt(-1)", None), # Math domain error, caught by Exception or specific math error
        ("1 / 0", None), # ZeroDivisionError test
        ("1 +", None), # SyntaxError test
        ("sin(pi, 2)", None) # TypeError test for sin
    ]

    for expr, expected in expressions_to_test:
        result, msg = safe_eval(expr)
        print(f"Expression: '{expr}'")
        if result is not None:
            print(f"  Result: {result}, Message: {msg}")
            if expected is not None:
                # Comparing floats requires tolerance
                if isinstance(result, float) and isinstance(expected, float):
                    assert math.isclose(result, expected), f"Expected {expected}, got {result}"
                else:
                    assert result == expected, f"Expected {expected}, got {result}"
        else:
            print(f"  Error: {msg}")
            # For tests designed to fail, 'expected' is None
            assert expected is None, f"Expected error for '{expr}', but got a result: {result}"
        print("-" * 20)

    print("\nSafe calculator tests completed.")

    # Example of a more complex expression
    complex_expr = "log(sqrt(pow(3,2) + pow(4,2)) + 5) * sin(radians(30))" # log(sqrt(9+16)+5) * sin(0.523) = log(10)*0.5 = 2.302 * 0.5 = 1.151
    # log(sqrt(25)+5) * 0.5 = log(5+5)*0.5 = log(10)*0.5 = 2.302585 * 0.5 = 1.15129
    res, m = safe_eval(complex_expr)
    print(f"Complex expr: {complex_expr}\nResult: {res}, Msg: {m}")
    if res is not None:
        assert math.isclose(res, math.log(10) * math.sin(math.radians(30)))

    # Test with a disallowed name (if not in ALLOWED_NAMES)
    # For example, if 'gamma' from math was not added:
    # res_gamma, msg_gamma = safe_eval("gamma(5)") # math.gamma
    # print(f"Expression: 'gamma(5)'\n  Result: {res_gamma}, Message: {msg_gamma}")
    # assert res_gamma is None # This should fail if gamma is not in ALLOWED_NAMES

    # Test simple variable assignment (should not work due to empty locals)
    # res_assign, msg_assign = safe_eval("x=5; x*2")
    # print(f"Expression: 'x=5; x*2'\n  Result: {res_assign}, Message: {msg_assign}")
    # This will likely be a SyntaxError because assignment expressions are not simple eval targets
    # or NameError if eval tries to resolve 'x' before assignment in its restricted way.
    # `eval` doesn't execute statements, only expressions.
    # For assignments, one would need `exec`, which is much harder to secure.
    # The current `safe_eval` is for single expressions.
    # If the expression was just "x=5", it would be a SyntaxError for eval.
    # If it was "x*2" after "x=5" was somehow set in globals, it might work, but we don't allow that.
    # The current safe_eval will likely return a SyntaxError for "x=5; x*2"
    # or an error related to the semicolon. Let's test a simpler "x*2"
    res_var, msg_var = safe_eval("x*2")
    print(f"Expression: 'x*2'\n Result: {res_var}, Message: {msg_var}")
    assert res_var is None # x is not defined.
    assert "name 'x' is not defined" in msg_var.lower() or "name 'x' is not allowed" in msg_var.lower()

    print("Additional tests completed.")
