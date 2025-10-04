from src.power import calculate, translate_in_RPN
import pytest



# === CORRECT EXPRESSIONS ===
@pytest.mark.parametrize("expression, expected", [
    ("7 8 +", 15),
    ("20 3 -", 17),
    ("6 5 *", 30),
    ("15 4 /", 3.75),
    ("20 3 |", 6),
    ("19 7 %", 5),
    ("4 3 ^", 64),
    ("2 6 3 * +", 20),
    ("8 2 3 + 5 * + 4 -", 29),
    ("4.5 2 *", 9.0),
    ("9", 9),
    ("-4", -4),
    ("+5", 5),
    ("2e2 3 +", 203),
    ("3 1e-2 *", 0.03),
    ("6.0 2 +", 8),
    ("7 -2 +", 5),
    ("10 +4 +", 14),
    ("3 2 3 ^ ^", 6561),
    ("0 0 ^", 1),
    ("( ( 5 ) )", 5),
    ("3 2 + 6 *", 30),
    ("6 2 3 + 3 ^ + 5 -", 126),
])
def test_rpn_correct(expression, expected):
    result = calculate(expression.split())
    assert result == expected


# === ZERO DIVISION ===
@pytest.mark.parametrize("expression, expected", [
    ("10 0 /", "\033[31mDividing into zero not defined\033[0m"),
    ("9 0 |", "\033[31mDividing into zero not defined\033[0m"),
    ("12 0 %", "\033[31mDividing into zero not defined\033[0m"),
])
def test_rpn_zero_division(expression, expected):
    result = calculate(expression.split())
    assert result == expected


# === TYPE ERRORS ===
@pytest.mark.parametrize("expression, expected", [
    ("4.2 3 |", "\033[31mYou cannot perform an operation '|' on float numbers\033[0m"),
    ("5.1 2 %", "\033[31mYou cannot perform an operation '%' on float numbers\033[0m"),
])
def test_rpn_type_error(expression, expected):
    result = calculate(expression.split())
    assert result == expected


# === LARGE POWERS ===
@pytest.mark.parametrize("expression, expected", [
    ("3 1000000000 ^", float('inf')),
    ("5 500000 ^", float('inf')),
    ("2 -50 ^", 8.881784197001252e-16),
])
def test_rpn_large_power(expression, expected):
    result = calculate(expression.split())
    assert result == expected


# === SYNTAX ERRORS ===
@pytest.mark.parametrize("expression, expected", [
    ("7 +", "\033[31mNot enough operands\033[0m"),
    ("4 2 #", "\033[31mSyntax error\033[0m"),
    ("", "\033[31mSyntax error\033[0m"),
    ("8 3 + 2", "\033[31mSyntax error\033[0m"),
    ("xyz 4 +", "\033[31mSyntax error\033[0m"),
    ("--5 3 +", "\033[31mSyntax error\033[0m"),
    ("+", "\033[31mNot enough operands\033[0m"),
])
def test_rpn_syntax_error(expression, expected):
    result = calculate(expression.split())
    assert result == expected


# === VALID PARENTHESES ===
@pytest.mark.parametrize("expression, expected", [
    ("( 6 7 + )", 13),
    ("3 ( 4 5 * ) +", 23),
    ("( 2 3 * ) 4 +", 10),
    ("5 6 + ( 2 3 * ) 1 + +", 18),
])
def test_rpn_parentheses_valid(expression, expected):
    result = calculate(expression.split())
    assert result == expected


# === INVALID PARENTHESES ===
@pytest.mark.parametrize("expression, expected", [
    ("( 7 8 +", "\033[31mSyntax error\033[0m"),
    ("5 6 + )", "\033[31mSyntax error\033[0m"),
    ("(3 + 4) )", "\033[31mSyntax error\033[0m"),
    ("( (1 + 2 )", "\033[31mSyntax error\033[0m"),
    (") 4 5 + (", "\033[31mSyntax error\033[0m"),
    ("()", "\033[31mSyntax error\033[0m"),
    ("( 1 2 )", "\033[31mSyntax error\033[0m"),
])
def test_rpn_parentheses_invalid(expression, expected):
    result = calculate(expression.split())
    assert result == expected





# === CORRECT EXPRESSIONS ===
@pytest.mark.parametrize("expression, expected", [
    ("7 + 8", 15),
    ("20 - 3", 17),
    ("6 * 5", 30),
    ("15 / 4", 3.75),
    ("20 | 3", 6),
    ("19 % 7", 5),
    ("4 ^ 3", 64),
    ("2 + 6 * 3", 20),
    ("8 + ( 2 + 3 ) * 5 - 4", 29),
    ("4.5 * 2", 9),
    ("9", 9),
    ("-4", -4),
    ("+5", 5),
    ("2e2 + 3", 203),
    ("3 * 1e-2", 0.03),
    ("6.0 + 2", 8),
    ("7 + ( -2 )", 5),
    ("10 + ( +4 )", 14),
    ("3 ^ ( 3 ^ 3 )", 7625597484987),
    ("0 ^ 0", 1),
    ("( ( 5 ) )", 5),
    ("( 3 + 2 ) * 6", 30),
    ("6 + ( 2 + 3 ) ^ 3 - 5", 126),
])
def test_infix_correct(expression, expected):
    result = calculate(translate_in_RPN(expression.split()))
    assert result == expected


# === ZERO DIVISION ===
@pytest.mark.parametrize("expression, expected", [
    ("10 / 0", "\033[31mDividing into zero not defined\033[0m"),
    ("9 | 0", "\033[31mDividing into zero not defined\033[0m"),
    ("12 % 0", "\033[31mDividing into zero not defined\033[0m"),
])
def test_infix_zero_division(expression, expected):
    result = calculate(translate_in_RPN(expression.split()))
    assert result == expected


# === TYPE ERRORS ===
@pytest.mark.parametrize("expression, expected", [
    ("4.2 | 3", "\033[31mYou cannot perform an operation '|' on float numbers\033[0m"),
    ("5.1 % 2", "\033[31mYou cannot perform an operation '%' on float numbers\033[0m"),
])
def test_infix_type_error(expression, expected):
    result = calculate(translate_in_RPN(expression.split()))
    assert result == expected


# === LARGE POWERS ===
@pytest.mark.parametrize("expression, expected", [
    ("3 ^ 1000000000", float('inf')),
    ("5 ^ 500000", float('inf')),
    ("2 ^ -50", 8.881784197001252e-16),
])
def test_infix_large_power(expression, expected):
    result = calculate(translate_in_RPN(expression.split()))
    assert result == expected


# === SYNTAX ERRORS ===
@pytest.mark.parametrize("expression, expected", [
    ("7 +", "\033[31mNot enough operands\033[0m"),
    ("4 + 2 #", "\033[31mSyntax error\033[0m"),
    ("", "\033[31mSyntax error\033[0m"),
    ("8 3 + 2", "\033[31mSyntax error\033[0m"),
    ("xyz + 4", "\033[31mSyntax error\033[0m"),
    ("--5 + 3", "\033[31mSyntax error\033[0m"),
    ("+", "\033[31mNot enough operands\033[0m"),
])
def test_infix_syntax_error(expression, expected):
    result = calculate(translate_in_RPN(expression.split()))
    assert result == expected


# === VALID PARENTHESES ===
@pytest.mark.parametrize("expression, expected", [
    ("( 3 + 4 )", 7),
    ("2 + ( 3 * 4 )", 14),
    ("( 2 * 3 ) + 4", 10),
    ("2 + 3 + ( 3 * 4 ) + 3", 20),
])
def test_infix_parentheses_valid(expression, expected):
    result = calculate(translate_in_RPN(expression.split()))
    assert result == expected


# === INVALID PARENTHESES ===
@pytest.mark.parametrize("expression, expected", [
    ("( 7 + 8", "\033[31mSyntax error\033[0m"),
    ("5 + 6 )", "\033[31mSyntax error\033[0m"),
    ("( 3 + 4 ) )", "\033[31mSyntax error\033[0m"),
    ("( ( 1 + 2 )", "\033[31mSyntax error\033[0m"),
    (") 4 + 5 (", "\033[31mSyntax error\033[0m"),
    ("( )", "\033[31mSyntax error\033[0m"),
    ("( 1 2 )", "\033[31mSyntax error\033[0m"),
])
def test_infix_parentheses_invalid(expression, expected):
    result = calculate(translate_in_RPN(expression.split()))
    assert result == expected

