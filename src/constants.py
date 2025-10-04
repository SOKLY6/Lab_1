PRIORITIES = {'(': 0, ')': 0, '+': 1, '-': 1, '*': 2, '/': 2, '|': 2, '%': 2, '^': 3}
ERRORS = ["\033[31mUnknown operation\033[0m", "\033[31mYou cannot perform an operation '%' on float numbers\033[0m",
          "\033[31mDividing into zero not defined\033[0m", "\033[31mYou cannot perform an operation '|' on float numbers\033[0m", 
          "\033[31mSyntax error\033[0m", "\033[31mNot enough operands\033[0m"]