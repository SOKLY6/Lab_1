"""
Calculator (M3 + M2 variant) with support for Reverse Polish Notation (RPN)
and Infix expressions with optional parentheses validation.
"""

import sys

from src.constants import ERRORS
from src.power import calculate, translate_in_RPN


def run() -> None:  # noqa: C901
    """
    Run the calculator REPL loop.

    Behavior:
    - Prompts the user to input expressions.
    - Supports two modes:
        * "RPN" → input is already in Reverse Polish Notation.
        * "IN"  → input is Infix, converted to RPN automatically.
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

        if line == "RPN":
            try:
                for line_RPN in sys.stdin:
                    line_RPN = line_RPN.strip()
                    if not line_RPN:
                        continue
                    if line_RPN == "stop":
                        break
                    tokens_rpn: list[str] = line_RPN.split()
                    result = calculate(tokens_rpn)
                    print(result)
            except (ValueError, IndexError, TypeError):
                print("\033[31mInput error\033[0m")

        if line == "IN":
            try:
                for line_IN in sys.stdin:
                    line_IN = line_IN.strip()
                    if not line_IN:
                        continue
                    if line_IN == "stop":
                        break
                    tokens_in: list[str] = line_IN.split()
                    RPN_expression = translate_in_RPN(tokens_in)

                    # Проверка: translate_in_RPN может вернуть list[str] или str (ошибка)
                    if isinstance(RPN_expression, str) and RPN_expression in ERRORS:
                        print(RPN_expression)
                        continue

                    result = calculate(RPN_expression)  # type: ignore[arg-type]
                    print(result)
            except (ValueError, IndexError, TypeError):
                print("\033[31mInput error\033[0m")


if __name__ == "__main__":
    run()

