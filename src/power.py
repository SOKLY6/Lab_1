import re
from src.constants import PRIORITIES, ERRORS


import re

def isNumber(token):
    """
    Check if the token is a number (integer, float, or exponential form).

    Args:
        token (str | int | float): The token to check.

    Returns:
        bool: True if the token represents a number, otherwise False.
    """
    return bool(re.fullmatch(r"([-+]?[1-9][0-9]*(.[0-9]*)?)|(0(.0*)?|([-+]?[1-9][0-9]*(.[0-9]*)?[eE][-+]?[1-9][0-9]*))", str(token)))


def isOperation(token):
    """
    Check if the token is a valid arithmetic operation.

    Args:
        token (str): The token to check.

    Returns:
        bool: True if the token is one of (+, -, *, /, |, %, ^), otherwise False.
    """
    return token in ['+', '-', '*', '/', '|', '%', '^']


def getToken(expression):
    """
    Extract the first token from the expression.

    Args:
        expression (list | str): A sequence of tokens or a string expression.

    Returns:
        str | None: The first token, or None if the expression is empty.
    """
    if expression:
        return expression[0]
    return None


def check_and_extract_parentheses(expression):
    """
    Check and evaluate the expression inside parentheses (recursively).

    Args:
        expression (list | str): Expression starting with '('.

    Returns:
        tuple:
            - result (float | int | str): The evaluated result or an error message.
            - expression (list | str | None): The remaining expression after ')'.
    """
    if ')' in expression[1:]:
        recursive_stack = []
        expression = expression[1:]
        while token := getToken(expression):
            if token == '(':
                recursive_res, expression = check_and_extract_parentheses(expression)
                recursive_stack.append(recursive_res)
                expression = expression[1:]
                continue
            if token == ')':
                break
            recursive_stack.append(token)
            expression = expression[1:]
        return calculate(recursive_stack), expression
    else:
        return None, None


def operation(stack, token):
    """
    Perform an arithmetic operation on the top two elements of the stack.

    Args:
        stack (list[float]): Operand stack.
        token (str): Operation ('+', '-', '*', '/', '|', '%', '^').

    Returns:
        tuple:
            - result (float | str): The operation result or an error message.
            - stack (list | None): Updated stack, or None if error occurred.
    """
    try:
        operand_2 = stack.pop()
        operand_1 = stack.pop()
        match token:
            case '+':
                result = operand_1 + operand_2
            case '-':
                result = operand_1 - operand_2
            case '*':
                result = operand_1 * operand_2
            case '/':
                if operand_2 == 0:
                    return "\033[31mDividing into zero not defined\033[0m", None
                result = operand_1 / operand_2
            case '|':
                if operand_1.is_integer() and operand_2.is_integer:
                    if operand_2 == 0:
                        return "\033[31mDividing into zero not defined\033[0m", None
                    result = int(operand_1) // int(operand_2)
                else:
                    return "\033[31mYou cannot perform an operation '|' on float numbers\033[0m", None
            case '%':
                if operand_1.is_integer() and operand_2.is_integer:
                    if operand_2 == 0:
                        return "\033[31mDividing into zero not defined\033[0m", None
                    result = int(operand_1) % int(operand_2)
                else:
                    return "\033[31mYou cannot perform an operation '%' on float numbers\033[0m", None
            case '^':
                try:
                    result = operand_1 ** operand_2
                    if isinstance(result, int) and result > 10**308:
                        result = float('inf')
                except OverflowError:
                    result = float('inf')
            case _:
                return "\033[31mUnknown operation\033[0m", None
        return result, stack
    except ValueError:
        return float('inf'), None


def translate_in_RPN(expression):
    """
    Convert an expression into Reverse Polish Notation (RPN).

    Args:
        expression (list | str): A mathematical expression.

    Returns:
        list[str] | str: Tokens in RPN format, or an error message.
    """
    result = []
    operation_stack = []
    while token := getToken(expression):

        if isNumber(token):
            result.append(token)
            expression = expression[1:]
            continue

        if isOperation(token):
            while operation_stack and isOperation(token) and (PRIORITIES[operation_stack[-1]] >= PRIORITIES[token]):

                result.append(operation_stack.pop())
            operation_stack.append(token)
            expression = expression[1:]
            continue

        if token == '(':
            operation_stack.append(token)
            expression = expression[1:]
            continue

        if token == ')':
            if '(' not in operation_stack:
                return "\033[31mSyntax error\033[0m"
            while operation_stack and operation_stack[-1] != '(':
                result.append(operation_stack.pop())
            if operation_stack and operation_stack[-1] == '(':
                operation_stack.pop()
            expression = expression[1:]
            continue

        return "\033[31mSyntax error\033[0m"

    if '(' in result:
        return "\033[31mSyntax error\033[0m"
    while operation_stack:
        result.append(operation_stack.pop())
    return result


def calculate(expression):
    """
    Evaluate an expression in Reverse Polish Notation (RPN) or infix form (with parentheses).

    Args:
        expression (list | str): A mathematical expression.

    Returns:
        int | float | str:
            - int: if the result is an integer
            - float: if the result is a decimal
            - str: error message
    """
    stack = []
    while token := getToken(expression):
        if isNumber(token):
            stack.append(float(token))
            expression = expression[1:]
            continue

        if isOperation(token):
            try:
                if type(stack[-1]) in [int, float] and type(stack[-2]) in [int, float]:
                    result, stack = operation(stack, token)
                    if stack == None:
                        return result
                    stack.append(float(result))
                    expression = expression[1:]
                    continue
            except:
                return "\033[31mNot enough operands\033[0m"

        if token == '(':
            recursive_res, expression = check_and_extract_parentheses(expression)
            if recursive_res in ERRORS:
                return recursive_res
            if expression == None:
                return "\033[31mSyntax error\033[0m"
            stack.append(recursive_res)
            expression = expression[1:]
            continue

        return "\033[31mSyntax error\033[0m"

    if stack:
        result = stack.pop()
    else:
        return "\033[31mSyntax error\033[0m"
    if not stack:
        if isinstance(result, float):
            if result.is_integer():
                return int(result)
            else:
                return result
        elif isinstance(result, int):
            return result
        else:
            return result
    else:
        return "\033[31mSyntax error\033[0m"




















