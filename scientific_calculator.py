"""Scientific Calculator PBL: demonstrates functions and the math module."""

import math


def add(a, b):
    """Return the sum of two numbers."""
    return a + b


def subtract(a, b):
    """Return the difference of two numbers."""
    return a - b


def multiply(a, b):
    """Return the product of two numbers."""
    return a * b


def divide(a, b):
    """Divide a by b, rejecting division by zero."""
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


def power(a, b):
    """Return a raised to the power b."""
    result = a ** b
    if isinstance(result, complex):
        raise ValueError("Complex-number results are not supported.")
    return result


def square_root(number):
    """Return the square root of a non-negative number."""
    if number < 0:
        raise ValueError("Square root of a negative number is not supported.")
    return math.sqrt(number)


def factorial(number):
    """Return factorial for a non-negative whole number."""
    if number < 0 or not number.is_integer():
        raise ValueError("Factorial requires a non-negative whole number.")
    return math.factorial(int(number))


def trigonometric(operation, angle_degrees):
    """Calculate sine, cosine or tangent; input angle is in degrees."""
    radians = math.radians(angle_degrees)

    if operation == "sin":
        return math.sin(radians)
    if operation == "cos":
        return math.cos(radians)
    if operation == "tan":
        if math.isclose(math.cos(radians), 0.0, abs_tol=1e-12):
            raise ValueError("Tangent is undefined for this angle.")
        return math.tan(radians)

    raise ValueError("Invalid trigonometric operation.")


def format_result(value):
    """Format floating-point output without unnecessary trailing zeroes."""
    return f"{value:.6f}".rstrip("0").rstrip(".")


def show_menu():
    print("\n========== SCIENTIFIC CALCULATOR ==========")
    print("1. Addition          6. Square root")
    print("2. Subtraction       7. Factorial")
    print("3. Multiplication    8. Sine")
    print("4. Division          9. Cosine")
    print("5. Power            10. Tangent")
    print("0. Exit")


def read_number(prompt):
    """Read a number from the keyboard."""
    number = float(input(prompt))
    if not math.isfinite(number):
        raise ValueError("Please enter a finite number.")
    return number


def main():
    """Run the calculator menu until the user chooses Exit."""
    arithmetic_operations = {
        "1": ("Addition", add),
        "2": ("Subtraction", subtract),
        "3": ("Multiplication", multiply),
        "4": ("Division", divide),
        "5": ("Power", power),
    }
    trigonometric_operations = {"8": "sin", "9": "cos", "10": "tan"}

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("Thank you for using the Scientific Calculator.")
            break

        try:
            if choice in arithmetic_operations:
                first = read_number("Enter first number: ")
                second = read_number("Enter second number: ")
                label, operation = arithmetic_operations[choice]
                result = operation(first, second)
                print(f"{label} result = {format_result(result)}")

            elif choice == "6":
                number = read_number("Enter a number: ")
                print("Square root =", format_result(square_root(number)))

            elif choice == "7":
                number = read_number("Enter a non-negative whole number: ")
                print("Factorial =", factorial(number))

            elif choice in trigonometric_operations:
                angle = read_number("Enter angle in degrees: ")
                operation = trigonometric_operations[choice]
                result = trigonometric(operation, angle)
                print(f"{operation}({format_result(angle)}) = {format_result(result)}")

            else:
                print("Invalid choice. Please select an option from the menu.")

        except ValueError as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
