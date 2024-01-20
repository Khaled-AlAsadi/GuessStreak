from asyncio import exceptions
import os
from google.auth import exceptions
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import gspread
import json
from random import randint
import time
import validation
import gspread
from google.oauth2.service_account import Credentials
from colorama import Fore, Back, Style

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("Guess-Number-Game")
Blad1 = SHEET.worksheet("Blad1")

choice = ""
level = 1
max_number = 10
name = ""
score = 0


def rules():
    """
    Function that displays the rules of the game
    """
    validation.clear_console()
    print(
        "Rule 1 : The player guess the number\n"
        "Rule 2 : On each level the max number for the guess increaases\n"
        "Rule 3 : On level completion the player gets 50 points\n"
        "Rule 4: The result gets saved to google spreadsheets on the player"
        "chooses not to keep playing by typing no on the question\n"
    )
    choice = input("Return to menu by typing 0 and press enter\n")
    if not validation.checkChoice(choice):
        print("please enter a valid choice")
    elif int(choice) == 0:
        validation.clear_console()
        menu()


def menu():
    """
    Main Menu function that runs first
    """
    print(Fore.WHITE + "1. Start Game\n" "2. Rules")
    choice = input(
        f"""
    Please choose an option from the menu and type
    the number of the choice and press enter\n
                   """
    )
    while not validation.checkChoice(choice):
        choice = input(
            Fore.RED
            + f"""Please choose a valid option from
            the menu and type the number of the choice\n
            """
        )
    if int(choice) == 1:
        validation.clear_console()
        start_game(level, max_number)
    if int(choice) == 2:
        rules()


def start_game(level, max_number):
    """
    Function that handles the game logic and saving to spreadsheet
    """
    global score
    global name
    name = (
        input(Fore.WHITE + f"Please type your name and press enter\n")
        if level == 1
        else name
    )

    while validation.check_name(name):
        name = (
            input(Fore.WHITE + "Please type your name and press enter\n")
            if level == 1
            else name
        )
    validation.clear_console()
    print("Level:", level)
    print("Score:", score)
    random_number = randint(1, max_number)
    print("Guess a number between 1 and " + str(max_number))
    guess = int(input("Enter your guess:\n "))
    while random_number != guess:
        if guess < random_number:
            print("low number")
            guess = int(input("Enter your guess again:\n "))
        elif guess > random_number:
            print("Too high number")
            guess = int(input("Enter your guess again:\n "))
    print(
        Fore.GREEN
        + "Congrats you guessed the number. The number is "
        + str(random_number)
    )
    if random_number == guess:
        score += 50

    if validation.check_input():
        print(Style.RESET_ALL)
        max_number += 5
        print(max_number)
        level += 1
        start_game(level, max_number)
        print(max_number)
    else:
        NEW_DATA = [name, level, score]
        Blad1.append_row(NEW_DATA)
        data_range = Blad1.get_all_values()
        header = data_range[0]
        data = data_range[1:]
        data.sort(key=lambda x: int(x[2]), reverse=True)
        top_10_data = data[:10]
        Blad1.clear()
        Blad1.append_row(header)
        for row, index in enumerate(top_10_data):
            Blad1.append_row(index)
            if row == 9:
                return
        validation.clear_console()
        menu()


menu()
