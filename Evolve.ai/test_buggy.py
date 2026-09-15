# test_buggy.py - Corrected script for testing Evolve Labs Autonomous Agent
import os
import sys

def calculate_total_price(item_list, tax_rate):
    """
    Calculates the total price of a list of items including tax.
    Handles missing keys, invalid types, and incorrect formats gracefully.
    """
    total = 0
    if not isinstance(item_list, list):
        return 0.0
        
    # Bug 2: Safely convert tax_rate to float to prevent TypeError/ValueError
    try:
        tax_rate = float(tax_rate)
    except (TypeError, ValueError):
        tax_rate = 0.0

    for item in item_list:
        if not isinstance(item, dict):
            continue
            
        # Bug 1 & 4: Safe key access with default fallbacks
        price = item.get('price', 0.0)
        quantity = item.get('qty', 1)  # Default to 1 quantity if key is missing
        
        # Ensure price and quantity are valid numeric values
        try:
            price = float(price)
            quantity = float(quantity)
        except (TypeError, ValueError):
            price = 0.0
            quantity = 0.0
            
        total += price * quantity
    
    final_amount = total + (total * tax_rate)
    return final_amount

def process_user_data(file_name):
    """
    Safely reads user data from a file, preventing file resource leaks and unhandled IO exceptions.
    """
    # Bug 3: Using 'with' context manager to auto-close and try-except block to handle missing files
    try:
        with open(file_name, 'r') as f:
            data = f.read()
        print("File data loaded successfully.")
        return data
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' does not exist.")
        return None
    except Exception as e:
        print(f"Error reading file '{file_name}': {e}")
        return None

if __name__ == "__main__":
    items = [
        {"name": "Laptop", "price": 1200, "qty": 1},
        {"name": "Mouse", "price": 25}  # Bug 4: No longer raises KeyError
    ]
    
    tax = 0.05
    total_cost = calculate_total_price(items, tax)
    print(f"Total Cost: {total_cost}")
    
    process_user_data("non_existent_file.txt")