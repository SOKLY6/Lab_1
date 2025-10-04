"""
RPN Calculator (M3 variant) with support for Reverse Polish Notation (RPN)
and infix expressions with optional parentheses validation.

Features:
- Supported operators: +, -, *, /, ^, |, %
- | and % are only allowed for integers
- Unary + / - are allowed inside numbers (e.g., -3 or +4.5)
- Parentheses may be present in infix input; each parentheses group must reduce to a single value:
    Examples:
        ( 2 ) -> OK
        ( 1 2 + ) -> OK
        ( 1 2 ) + -> INVALID (inside parentheses leaves more than one value)
- No usage of eval/exec for security reasons.

Usage:
------
Run the program:
    $ python3 src/main.py

The calculator starts in interactive mode and accepts two commands:

1) RPN mode:
    Enter `RPN` to evaluate expressions written directly in Reverse Polish Notation.
    Tokens must be space-separated.

    Example:
        Input:
            RPN
            3 4 + 
            5 2 - 
            stop

        Output:
            7
            3

2) IN mode:
    Enter `IN` to evaluate infix expressions. They will be converted
    into RPN automatically before evaluation.

    Example:
        Input:
            IN
            ( 3 + 4 ) * 2
            2 ^ 10
            stop

        Output:
            14
            1024

Type `stop` at any time to exit the current mode.
"""

import sys
from src.power import calculate, translate_in_RPN
from src.constants import ERRORS


def run():
    """
    Run the calculator REPL loop.

    Behavior:
    - Prompts the user to input expressions.
    - Supports two modes:
        * "RPN" → input is already in Reverse Polish Notation.
        * "IN"  → input is infix, converted to RPN automatically.
    - Stops reading expressions if the user types 'stop'.

    Error handling:
    - If an invalid expression is provided, prints an error message.
    """
    print(
        "Welcome to calculator! Enter RPN and Infix expressions, tokens separated by spaces. "
        "Parentheses allowed. Unary +- must be written directly with the number (e.g., -3, +2.5)."
    )
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if line == 'RPN':
            try:
                for line_RPN in sys.stdin:
                    line_RPN = line_RPN.strip()
                    if not line_RPN:
                        continue
                    if line_RPN == 'stop':
                        break
                    tokens = line_RPN.split()
                    result = calculate(tokens)
                    if result is not None:
                        print(result)
            except:
                print("\033[31mInput error\033[0m")

        if line == 'IN':
            try:
                for line_IN in sys.stdin:
                    line_IN = line_IN.strip()
                    if not line_IN:
                        continue
                    if line_IN == 'stop':
                        break
                    tokens = line_IN.split()
                    RPN_expression = translate_in_RPN(tokens)
                    if RPN_expression in ERRORS:
                        print(RPN_expression)
                        continue
                    result = calculate(RPN_expression)
                    if result is not None:
                        print(result)
            except:
                print("\033[31mInput error\033[0m")


if __name__ == "__main__":
    run()
