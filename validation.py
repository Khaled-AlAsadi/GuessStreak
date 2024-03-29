import os
import re
import time
from colorama import Fore, Back, Style


def checkChoice(text):
    try:
        if int(text) < 0:
            print(
                Fore.WHITE
                + Back.RED
                + "Please enter a positive number."
                + Style.RESET_ALL
            )
            return False
        elif int(text) > 3:
            return False
        else:
            return True
    except ValueError:
        print(Fore.RED + "Please enter a valid number." + Style.RESET_ALL)
        return False


def checkRulesChoice(text):
    try:
        num = int(text)
        if num == 0:
            return True
        else:
            return False
    except ValueError:
        return False


def check_input():
    while True:
        answer = input(
            "Do you want to proceed to the next level? (yes/no): \n").lower()
        if answer == "yes":
            print(Style.RESET_ALL)
            return True
        elif answer == "no":
            print(Style.RESET_ALL)
            return False
        else:
            print(Fore.RED + "Invalid input. Please enter 'yes' or 'no'.")
            print(Style.RESET_ALL)
            time.sleep(0.1)


def check_name(name):
    if len(name.strip()) == 0:
        print(Fore.RED + "Please enter a valid name" + Style.RESET_ALL)
        return True
    elif not re.match("^[a-zA-Z0-9 ]+$", name):
        print(Fore.RED +
              "Name should contain only letters, numbers, and spaces" +
              Style.RESET_ALL)
        return True
    else:
        return False


def clear_console():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
