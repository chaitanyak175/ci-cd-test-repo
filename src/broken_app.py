# Intentionally broken Python file for testing
# Multiple import, syntax, and logic errors

import os
import sys
import nonexistent_module  # ImportError - module doesn't exist
from missing_package import something  # ImportError

# Syntax error: invalid indentation
def broken_function():
print("This has indentation error")  # IndentationError
    return "mixed indentation"

# Undefined variable usage
def another_broken_function():
    result = undefined_variable + 10  # NameError
    return missing_function()  # NameError

# Type error
def type_error_function():
    number = "not a number"
    return number + 5  # TypeError: can't add string and int

# Missing import but using module
def missing_import_usage():
    data = json.loads('{"key": "value"}')  # NameError: json not imported
    return data

# Syntax error: invalid syntax
def syntax_error_function()  # Missing colon
    return "this won't work"

# Missing required dependency
def database_connection():
    import psycopg2  # Not installed, will fail
    conn = psycopg2.connect("postgresql://localhost/test")
    return conn

if __name__ == "__main__":
    # This will fail with multiple errors
    broken_function()
    another_broken_function()
    type_error_function()
    missing_import_usage()
    syntax_error_function()
    database_connection()
