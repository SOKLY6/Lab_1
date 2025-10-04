import re
from typing import Callable, Optional

from src.constants import PRIORITIES

# ------------------ Helper Functions ------------------

def isNumber(token: str | int | float) -> bool:
    """Check if the token is a number (integer, float, or exponential form)."""
    return bool(
        re.fullmatch(
            r"([-+]?[1-9][0-9]*(\.[0-9]*)?)|(0(\.0*)?|([-+]?[1-9][0-9]*(\.[0-9]*)?[eE][-+]?[1-9][0-9]*))",
            str(token),
        )
    )


def isOperation(token: str) -> bool:
    """Check if the token is a valid arithmetic operation."""
    return token in ["+", "-", "*", "/", "|", "%", "^"]


def getToken(expression: list[str]) -> Optional[str]:
    """Extract the first token from the expression."""
    if expression:
        return expression[0]
    return None

# ------------------ Parentheses Extraction ------------------

def check_and_extract_parentheses(expression: list[str]) -> tuple[list[str] | str, list[str]]:
    """
    Extract tokens inside parentheses for RPN evaluation.
    Returns a tuple:
      - tokens inside the parentheses (or error string)
      - remaining tokens after the closing ')'
    """
    inner_tokens: list[str] = []
    expression = expression[1:]  

    while expression:
        token = expression[0]
        expression = expression[1:]

        if token == "(":
            sub_tokens, expression = check_and_extract_parentheses([token] + expression)
            if isinstance(sub_tokens, str):  
                return sub_tokens, []
            inner_tokens.append("(")
            inner_tokens.extend(sub_tokens)
            inner_tokens.append(")")
        elif token == ")":
            return inner_tokens, expression
        else:
            inner_tokens.append(token)

    # Если дошли до конца, а закрывающей скобки не было — ошибка
    return "\033[31mSyntax error\033[0m", []

# ------------------ Arithmetic Operations ------------------

def safe_div(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError
    return a / b

def safe_int_div(a: float, b: float) -> int:
    if not a.is_integer() or not b.is_integer():
        raise TypeError
    if b == 0:
        raise ZeroDivisionError
    return int(a) // int(b)

def safe_mod(a: float, b: float) -> int:
    if not a.is_integer() or not b.is_integer():
        raise TypeError
    if b == 0:
        raise ZeroDivisionError
    return int(a) % int(b)

def safe_pow(a: float, b: float) -> float | int:
    try:
        result: float | int = a ** b
        if isinstance(result, int) and result > 10**308:
            return float("inf")
        return result
    except OverflowError:
        return float("inf")

OP_MAP: dict[str, Callable[[float, float], float | int]] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": safe_div,
    "|": safe_int_div,
    "%": safe_mod,
    "^": safe_pow,
}

def operation(stack: list[float], token: str) -> tuple[float | str, list[float] | None]:
    """Perform operation on top two elements of the stack."""
    try:
        b = stack.pop()
        a = stack.pop()
        try:
            result = OP_MAP[token](a, b)
        except ZeroDivisionError:
            return "\033[31mDividing into zero not defined\033[0m", None
        except TypeError:
            return f"\033[31mYou cannot perform an operation '{token}' on float numbers\033[0m", None
        return result, stack
    except IndexError:
        return "\033[31mNot enough operands\033[0m", None

# ------------------ RPN Conversion ------------------

def translate_in_RPN(expression: list[str]) -> list[str] | str: # noqa: C901
    """Convert expression to Reverse Polish Notation."""
    result: list[str] = []
    stack_ops: list[str] = []
    for token in expression:
        if isNumber(token):
            result.append(token)
        elif isOperation(token):
            while (
                stack_ops
                and isOperation(stack_ops[-1])
                and PRIORITIES[stack_ops[-1]] >= PRIORITIES[token]
            ):
                result.append(stack_ops.pop())
            stack_ops.append(token)
        elif token == "(":
            stack_ops.append(token)
        elif token == ")":
            while stack_ops and stack_ops[-1] != "(":
                result.append(stack_ops.pop())
            if not stack_ops or stack_ops.pop() != "(":
                return "\033[31mSyntax error\033[0m"
        else:
            return "\033[31mSyntax error\033[0m"

    while stack_ops:
        if stack_ops[-1] == "(":
            return "\033[31mSyntax error\033[0m"
        result.append(stack_ops.pop())

    return result

# ------------------ RPN Evaluation ------------------

def calculate(expression: list[str]) -> int | float | str: # noqa: C901
    """Evaluate RPN or infix expression (with parentheses)."""
    stack: list[float] = []
    while expression:
        token = expression[0]
        expression = expression[1:]

        if isNumber(token):
            stack.append(float(token))
        elif isOperation(token):
            result, new_stack = operation(stack, token)
            if new_stack is None:
                return result
            if isinstance(result, (int, float)):
                stack = new_stack
                stack.append(float(result))
            else:
                return result
        elif token == "(":
            inner_tokens, rest_tokens = check_and_extract_parentheses([token] + expression)
            if isinstance(inner_tokens, str):
                return inner_tokens  
            rpn_inner = translate_in_RPN(inner_tokens)
            if isinstance(rpn_inner, str):
                return rpn_inner
            result = calculate(rpn_inner)
            if isinstance(result, str):
                return result
            stack.append(float(result))
            expression = rest_tokens
        else:
            return "\033[31mSyntax error\033[0m"

    if not stack:
        return "\033[31mSyntax error\033[0m"
    result = stack.pop()
    if stack:
        return "\033[31mSyntax error\033[0m"

    if isinstance(result, float) and result.is_integer():
        return int(result)
    return result
























