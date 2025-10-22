# Name: Riyan Shrestha
# ID: 1000XXXXXX
# Date: 2025-10-21
# OS: Linux (Ubuntu, VS Code workspace)

# --------------------------------------------------------------------
# Lab 03 — Extra Credit
#
# What this program does:
# 1) Reads algebraic (infix) expressions from input_RPN_EC.txt
# 2) Converts each to Reverse Polish Notation (RPN)
# 3) Evaluates the RPN
# 4) Prints:
#       RPN: <space-delimited RPN>
#       Result: <value>
#
# Assumptions (per assignment):
# - Numbers are single digits (0–9)
# - Tokens may be separated by spaces; parentheses allowed
# - Base operators: +, -, *, /
#
# Extra operators added (documented for GTA):
# - %  : modulo (binary)
# - u- : unary minus (e.g., -3, -(2+1))  ← printed as "u-" in RPN
#
# Notes:
# - Division uses true division; if the result is an exact whole number,
#   it prints as an int (e.g., 2 instead of 2.0).
# - The code avoids hard-coded paths and handles line endings cross-platform.
# --------------------------------------------------------------------

import os

# -----------------------------
# 1) Tokenize input expression
# -----------------------------
def tokenize(expr):
    """
    Turn an infix string into a list of tokens.
    Supports digits, + - * / % ( ) and unary minus (u-).
    We treat '-' as unary when it appears at the start of the expression
    or immediately after an operator or '('.
    """
    tokens = []
    i = 0
    prev_kind = None  # one of: None, 'num', 'op', 'lparen', 'rparen'

    while i < len(expr):
        ch = expr[i]

        if ch.isspace():
            i += 1
            continue

        if ch.isdigit():               # single-digit per spec
            tokens.append(ch)
            prev_kind = 'num'
            i += 1
            continue

        if ch in '+*/%':
            tokens.append(ch)
            prev_kind = 'op'
            i += 1
            continue

        if ch == '(':
            tokens.append(ch)
            prev_kind = 'lparen'
            i += 1
            continue

        if ch == ')':
            tokens.append(ch)
            prev_kind = 'rparen'
            i += 1
            continue

        if ch == '-':
            # decide unary vs binary
            if prev_kind in (None, 'op', 'lparen'):
                tokens.append('u-')  # unary minus
            else:
                tokens.append('-')   # binary minus
            prev_kind = 'op'
            i += 1
            continue

        # If we get here, it's an invalid character
        raise ValueError(f"Invalid character: {ch!r}")

    return tokens

# -------------------------------------------
# 2) Convert infix tokens to RPN (Shunting Yard)
# -------------------------------------------
def infix_to_rpn(tokens):
    """
    Shunting-Yard conversion.
    Precedence (high → low): u- (4), *, /, % (3), +, - (2)
    Associativity: u- is right-associative; others are left-associative.
    """
    output = []
    ops = []

    prec = {'u-': 4, '*': 3, '/': 3, '%': 3, '+': 2, '-': 2}
    right_assoc = {'u-'}

    def is_op(t):
        return t in prec

    for t in tokens:
        if t.isdigit():
            output.append(t)
        elif t == '(':
            ops.append(t)
        elif t == ')':
            # pop until '('
            while ops and ops[-1] != '(':
                output.append(ops.pop())
            if not ops:
                raise ValueError("Mismatched parentheses")
            ops.pop()  # discard '('
        elif is_op(t):
            # pop higher-precedence or equal-precedence (if left-assoc) operators
            while ops and ops[-1] != '(':
                top = ops[-1]
                if (prec[top] > prec[t]) or (prec[top] == prec[t] and t not in right_assoc):
                    output.append(ops.pop())
                else:
                    break
            ops.append(t)
        else:
            raise ValueError(f"Bad token: {t!r}")

    # drain remaining operators
    while ops:
        top = ops.pop()
        if top in ('(', ')'):
            raise ValueError("Mismatched parentheses at end")
        output.append(top)

    return output

# -----------------------------
# 3) Evaluate RPN
# -----------------------------
def eval_rpn(tokens):
    """
    Evaluate RPN tokens including + - * / % and unary minus u-.
    """
    stack = []

    for t in tokens:
        if t.isdigit():
            stack.append(int(t))
        elif t == 'u-':
            if not stack:
                raise ValueError("Unary minus with empty stack")
            stack.append(-stack.pop())
        elif t in {'+', '-', '*', '/', '%'}:
            if len(stack) < 2:
                raise ValueError("Not enough operands for binary operator")
            b = stack.pop()
            a = stack.pop()
            if t == '+':
                stack.append(a + b)
            elif t == '-':
                stack.append(a - b)
            elif t == '*':
                stack.append(a * b)
            elif t == '/':
                if b == 0:
                    raise ZeroDivisionError("Division by zero")
                stack.append(a / b)
            else:  # '%'
                if b == 0:
                    raise ZeroDivisionError("Modulo by zero")
                stack.append(a % b)
        else:
            raise ValueError(f"Unknown RPN token: {t!r}")

    if len(stack) != 1:
        raise ValueError("RPN left extra items on the stack")
    return stack[0]

# -----------------------------
# 4) Main: read, convert, eval
# -----------------------------
def main():
    here = os.path.dirname(os.path.abspath(__file__))
    infile = os.path.join(here, "input_RPN_EC.txt")

    try:
        # newline=None = universal newlines (handles Windows/Mac/Linux endings)
        with open(infile, "r", encoding="utf-8", newline=None) as f:
            for line in f:
                expr = line.strip()
                if not expr:
                    continue  # ignore blank lines

                try:
                    toks = tokenize(expr)
                    rpn = infix_to_rpn(toks)
                    val = eval_rpn(rpn)

                    # print RPN and result in required format
                    print("RPN:", " ".join(rpn))
                    # show as int if exact
                    if isinstance(val, float) and val.is_integer():
                        val = int(val)
                    print("Result:", val)
                except Exception:
                    print("RPN: ERROR")
                    print("Result: ERROR")
    except FileNotFoundError:
        print("RPN: ERROR")
        print("Result: input_RPN_EC.txt not found")

if __name__ == "__main__":
    main()
