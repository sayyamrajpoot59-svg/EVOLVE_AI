def add(a: float, b: float) -> float:
    """Do numbers ko jodta hai."""
    return a + b


def subtract(a: float, b: float) -> float:
    """Pehle number me se dusra number ghatata hai."""
    return a - b


def multiply(a: float, b: float) -> float:
    """Do numbers ko guna karta hai."""
    return a * b


def divide(a: float, b: float) -> float:
    """Pehle number ko dusre number se divide karta hai."""
    if b == 0:
        raise ValueError("Zero se divide nahi kiya ja sakta (Division by zero error).")
    return a / b


def display_menu() -> None:
    print("\n==========================")
    print("      PYTHON CALCULATOR   ")
    print("==========================")
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    print("5. Exit")
    print("==========================")


def main():
    while True:
        display_menu()
        choice = input("Apna option chunein (1-5): ").strip()

        if choice == '5':
            print("Calculator band ho raha hai. Dhanyawad!")
            break

        if choice not in ['1', '2', '3', '4']:
            print("Galat option! Kripya 1 se 5 ke beech chunein.")
            continue

        try:
            num1 = float(input("Pehla number daalein: "))
            num2 = float(input("Dusra number daalein: "))
        except ValueError:
            print("Error: Kripya valid numeric value daalein.")
            continue

        try:
            if choice == '1':
                result = add(num1, num2)
                operator = "+"
            elif choice == '2':
                result = subtract(num1, num2)
                operator = "-"
            elif choice == '3':
                result = multiply(num1, num2)
                operator = "*"
            elif choice == '4':
                result = divide(num1, num2)
                operator = "/"

            print(f"\nNateeja (Result): {num1} {operator} {num2} = {result}")
        except ValueError as err:
            print(f"\nError: {err}")


if __name__ == "__main__":
    main()
