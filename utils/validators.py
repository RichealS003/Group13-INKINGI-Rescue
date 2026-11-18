import re

#FOLLOWING FUNCTIONS ARE TO CHECK INPUTS----------------------------------------------------

#A phone number pattern used to validates if a Rwandan phone number was given or not
phone_number_pattern = re.compile(r"^(?:\+?250|0)(7[2389]\d{7})$")

#It will return a True boolean if it is valid so you can use in your code
def is_phone_number_valid(info):
    cleaned_number = re.sub(r"[\s\-]", "", info)    #uses re.sub to substitute whitespaces(\s) and hypens(\-) 
    if phone_number_pattern.match(cleaned_number):
        return True
    else:
        return False

#Function makes a valid Rwandan phone number a consistent format for use (07XXXXXXXX). Run valid number function first
def normalize_phone_number(info):
    cleaned_number = re.sub(r"[\s\-]", "", info)   
    match = phone_number_pattern.match(cleaned_number)
    if match:
        return "0" + match.group(1)
    else:
        raise ValueError("Invalid phone number")

#Does what the two function above do at once
def validate_and_normalize_number(info):
    if not is_phone_number_valid(info):
        raise ValueError("Invalid phone number. Please use a format like 07XXXXXXXX or +2507XXXXXXXX.")
    return normalize_phone_number(info)

#Check if input contains a letter and is longer than 2 characters
def is_place_valid(info):
    if not info:
        raise ValueError("Invalid. Please type something and try again")
    if len(info) >= 2:
        for character in input:
            if character.isalpha():
                return True
    return False


#FOLLOWING FUNCTIONS ARE TO GET USER INPUT AND AUTOMATICALLY CHECK -------------------------


#Prompts user for a menu choice and checks if the user types a number within range of the low value and high value
def get_menu_choice(prompt, low, high):
    while True:
        user_input = input(prompt).strip()

        if not user_input:
            print("Field cannot be left blank. Please try again.")
            continue
        if not user_input.isdigit():
            print(f"Invalid input. Please type a number between {low} and {high}")
            continue
        if int(user_input) >= low and int(user_input) <= high:
            return int(user_input)
        print(f"Invalid choice. Please type a number between {low} and {high}")

#Prompts user a yes and no question. Returns a boolean value depending user's input
def get_yes_and_no_choice(prompt):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in ("y", "yes"):
            return True
        if user_input in ("n", "no"):
            return False
        print("Invalid input. Please type 'y' for yes and 'n' for no")

#Prompts user for a phone number, validates and normalize a number
def get_phone_number(prompt):
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Field cannot be left blank. Please try again.")
        else:
            try:
                return validate_and_normalize_number(user_input)
            except ValueError as error:
                print(error)

#Prompts user for a place or landmark and validates whether its not blank or just numbers
def get_place_text(prompt):
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            print("Field cannot be left blank. Please try again.")
        elif not is_place_valid(user_input):
            print(f"{user_input} is invalid. Please try again.")
        else:
            return user_input