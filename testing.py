import re

def find_6_digit_numbers(input_string):
    # Define a regex pattern to match 6-digit numbers
    pattern = r'\b\d{6}\b'
    
    # Find all matches in the input string
    matches = re.findall(pattern, input_string)
    
    return matches

# Example usage
input_string = "Here are some numbers: 123456, 789012, and 3456, but not 12345 or 1234567."
six_digit_numbers = find_6_digit_numbers(input_string)

print("6-digit numbers found:", six_digit_numbers)