"""
Calculator (M3 + M2 variant) with support for Reverse Polish Notation (RPN)
and Infix expressions with optional parentheses validation.
"""

import sys

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
        "Welcome to the Calculator!"
        "\nYou can enter expressions in two modes:"
        "\n  1) RPN (Reverse Polish Notation) - tokens separated by spaces"
        "\n  2) IN (Infix notation) - standard mathematical notation with optional parentheses"
        "\nType 'stop' at any time to exit the current mode or the program."
    )

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        if line.upper() == "RPN":
            print("\nEntered RPN mode. Input expressions with tokens separated by spaces.")
            print("Type 'stop' to exit RPN mode.")
            try:
                for line_rpn in sys.stdin:
                    line_rpn = line_rpn.strip()
                    if not line_rpn:
                        continue
                    if line_rpn.lower() == "stop":
                        print("Exiting RPN mode.\n")
                        break
                    tokens_rpn: list[str] = line_rpn.split()
                    result = calculate(tokens_rpn)
                    print("Result:", result)
            except (ValueError, IndexError, TypeError):
                print("\033[31mInput error\033[0m")

        elif line.upper() == "IN":
            print("\nEntered Infix mode. Input standard mathematical expressions.")
            print("Type 'stop' to exit Infix mode.")
            try:
                for line_in in sys.stdin:
                    line_in = line_in.strip()
                    if not line_in:
                        continue
                    if line_in.lower() == "stop":
                        print("Exiting Infix mode.\n")
                        break
                    tokens_in: list[str] = line_in.split()
                    RPN_expression = translate_in_RPN(tokens_in)

                    # Проверяем тип, чтобы mypy был доволен
                    if isinstance(RPN_expression, list):
                        result = calculate(RPN_expression)
                        print("Result:", result)
                    else:
                        # Это строка с ошибкой
                        print(RPN_expression)
            except (ValueError, IndexError, TypeError):
                print("\033[31mInput error\033[0m")

        elif line.lower() == "stop":
            print("Exiting calculator. Goodbye!")
            break
        else:
            print("Unknown command. Please type 'RPN', 'IN', or 'stop'.")


