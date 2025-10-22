# Name: Riyan Shrestha
# ID: 1002223799
# Date: 2025-10-21
# OS: Linux (VS Code workspace)


import os

def calculate_rpn(expression):
    stack = []

    for token in expression:
        # Check if token is an operator or a number
        if token in ['+', '-', '*', '/']:
            # Make sure there are at least two numbers to operate on
            if len(stack) < 2:
                raise ValueError("Not enough operands for operation")

            # Pop the top two values
            right = stack.pop()
            left = stack.pop()

            # Perform operation
            if token == '+':
                stack.append(left + right)
            elif token == '-':
                stack.append(left - right)
            elif token == '*':
                stack.append(left * right)
            elif token == '/':
                if right == 0:
                    raise ZeroDivisionError("Division by zero is not allowed")
                stack.append(left / right)
        else:
            # Convert the number to int and push it onto the stack
            stack.append(int(token))

    # Final result should be the only item left
    if len(stack) != 1:
        raise ValueError("Invalid RPN expression")
    return stack[0]


def main():
    # Get the current directory path so it works on all systems
    current_folder = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_folder, "input_RPN.txt")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue  # Skip empty lines

                tokens = line.split()
                try:
                    result = calculate_rpn(tokens)
                    # Print result as integer if whole number
                    if isinstance(result, float) and result.is_integer():
                        result = int(result)
                    print(result)
                except Exception as err:
                    print(f"Error: {err}")
    except FileNotFoundError:
        print("Error: input_RPN.txt not found in this folder.")


if __name__ == "__main__":
    main()
