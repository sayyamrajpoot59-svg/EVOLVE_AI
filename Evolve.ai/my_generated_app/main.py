from calculator import add, subtract, multiply, divide


def get_number(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Kripya ek valid number daalein!")


def main():
    print("=" * 35)
    print("       Simple Python Calculator")
    print("=" * 35)
    print("1. Add (+)")
    print("2. Subtract (-)")
    print("3. Multiply (*)")
    print("4. Divide (/)")
    print("5. Exit")
    print("=" * 35)

    operations = {
        "1": ("+", add),
        "2": ("-", subtract),
        "3": ("*", multiply),
        "4": ("/", divide),
    }

    while True:
        choice = input("\nOperation chunein (1-5): ").strip()

        if choice == "5":
            print("Calculator band ho raha hai. Dhanyawad!")
            break

        if choice in operations:
            symbol, func = operations[choice]
            num1 = get_number("Pehla number daalein: ")
            num2 = get_number("Doosra number daalein: ")

            try:
                result = func(num1, num2)
                print(f"\nResult: {num1} {symbol} {num2} = {result}")
            except ValueError as error:
                print(f"\nError: {error}")
        else:
            print("Galat option! Kripya 1 se 5 ke beech chunein.")


if __name__ == "__main__":
    main()
