# import to clear terminal
import os

# import random to get random word for game
import random

# import gpsread
import gspread
from google.oauth2.service_account import Credentials

# imports for Oxford Dictionary API to check word
import json
import requests

from datetime import date

# import Acsii art library - pyfiglet
import pyfiglet

import pandas as pd

# import colorama for colour coding letters
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# credit post by anna_ci in code institute slack channel https://code-institute-room.slack.com/archives/CP07TN38Q/p1576743956008500
from os import path
if path.exists("env.py"):
    import env


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('word-Py-Leaderboard')



def get_answer_from_file():
    """
    Open txt file and get random word
    """
    file = open('words.txt', 'r')
    lines = file.read().splitlines()
    file.close
    random_word = random.choice(lines)
    print(random_word)
    return random_word


class OxfordDictAPI:
    """
    checks user guess is an actual word in the Oxford Dict
    """
    def __init__(self):
        self.load_api_credentials()
        self.base_url = "https://od-api.oxforddictionaries.com/api/v2"
        self.headers = {"app_id": self.app_id, "app_key": self.app_key}

    def check_in_dict(self, guess):
        """
        look up the user guess in oxford dict.
        Return the status code
        """
        url = self.base_url + "/entries/en-gb/" + guess.lower()
        api_response = requests.get(url, headers=self.headers)
        print("code {}\n".format(api_response.status_code))
        return api_response.status_code

    def load_api_credentials(self):
        """
        Get API credentials from env.py file
        credit: https://www.programiz.com/python-programming/json
        """
        # with open('oxford_api_credentials.json', 'r') as json_file:
        #     credentials = json.load(json_file)
        # self.app_id = credentials["app_id"]
        # self.app_key = credentials["app_key"]
        self.app_id = os.environ["OXFORD_API_APP_ID"]
        self.app_key = os.environ["OXFORD_API_APP_KEY"]


class WordChecker:
    """
    Creates an instance of WordChecker
    """
    def __init__(self, answer):
        self.answer = answer

    def validate_user_guess(self, guess):
        """
        Checks that user guess is valid - 5 letters and an actual word
        """
        try:
            if len(guess) != 5:
                raise ValueError('That is not a 5 letter word. \n')
            elif guess.isalpha() is False:
                raise ValueError('Please only enter letters not numbers. \n')
            # if the return status is 404(not found) then raise vaidation error
            # elif OxfordDictAPI().check_in_dict(guess) == 404:
            #     raise ValueError('Guess must be an actual word as per the Oxford Dictionary. \n')
        except ValueError as error:
            print(f'Invalid data: {error}Please try again. \n')
            return False

        return True

    def check_matching_letters(self, user_guess):
        """
        Compare user guess against answer
        """
        response_string = ""

        user_guess_dict = {index: value for index, value in enumerate(user_guess)}

        for ind, letr in user_guess_dict.items():
            if letr == self.answer[ind]:
                response_string += (Back.GREEN + letr)

            elif letr in self.answer:
                response_string += (Back.YELLOW + letr)
                # need to ensure duplicate letter doesn't go orange if its already green
            else:
                response_string += (Back.RED + letr)
        print(response_string)


class Game:
    """
    Creates and instance of the game
    """

    def __init__(self, word_checker):
        self.word_checker = word_checker
        self.no_of_chances = 6
        self.username = ""
        self.leaderboard = SHEET.worksheet('leaderboard')

    def introduction(self):
        """
        Introduction Message
        """
        print(pyfiglet.figlet_format("WELCOME TO WORD-PY", justify="center", width=80))
        print(Fore.GREEN + "Can you guess the word in 6 tries?\n".center(80))
        while True:
            self.username = input("Please enter your name to begin.\n").capitalize()

            if len(self.username.strip()) == 0:
                print(f"{Fore.RED}Name not valid!\n")
            else:
                break
        print(f"Hello {self.username}, welcome to Word-PY.\n")
        print("How to Play".center(80))
        print(f"""{Fore.MAGENTA}=======================================================\n""".center(80))
        print("Guess the word in 6 tries")
        print("Each guess MUST be a valid 5 letter word")
        print("After each guess, the color of the letters will change to show how close your guess was to the word")

    def play_again(self):
        """
        When the game ends ask the user if they wish to quit or play again
        """
        user_choice = input("Play Again? Y or N\n").strip().lower()

        if user_choice == "y":
            os.system('clear')
            main()

        elif user_choice == "n":
            print("Goodbye. Hope to see you soon")
            exit()

        else:
            print("Not a valid option")
            self.play_again()

    def ask_for_guess(self):
        """
        Ask the user for their guess if they have chances remaining, if not, gameover.
        If the user guesses correctly as them if they wish to play again.
        """
        while self.no_of_chances <= 6:
            if self.no_of_chances == 0:
                print("Gameover, No chances Left!\n")
                self.play_again()
            else:
                print(f"You have {self.no_of_chances} chances left\n")
            while True:
                user_input = input('Enter your guess here:\n').lower().strip()
                if self.word_checker.validate_user_guess(user_input):
                    self.no_of_chances -= 1
                    self.word_checker.check_matching_letters(user_input)
                    if user_input == self.word_checker.answer:
                        score = 6 - self.no_of_chances
                        print(f'Well done you got the correct answer in {score} attempts!')
                        self.update_leaderboard(score)
                        self.show_leaderboard()
                        self.play_again()
                    break

    def update_leaderboard(self, score):
        """
        Add name, score and date to row in leaderboard spreadsheet
        """
        today = date.today()
        # https://www.programiz.com/python-programming/datetime/current-datetime
        date_format = today.strftime("%d/%m/%Y")
        print('Updating leaderboard...\n')
        self.leaderboard.append_row([self.username, score, date_format])
        print("Leaderboard Updated")

    def show_leaderboard(self):
        """
        show the top 10 entries in the leaderboard
        """
        scores = self.leaderboard.get_all_values()
        columns = scores[0]
        data = scores[1:]
        print(columns)
        print(data)
        df = pd.DataFrame(data, columns=columns)
        print(df)

def main():
    """
    Run all program functions
    """

    # Define the answer
    answer = get_answer_from_file()
    # Use answer to instantiate Word
    word_checker = WordChecker(answer)

    # Instantiate game, passing it the answer Word
    game = Game(word_checker)

    # Start the Game introduction (show the rules, ask for a name)
    game.introduction()
    game.ask_for_guess()

    # While # of chances < the limit
        # Ask the user to provide a guess
        # Check the guess against the answer
        # Print out formatted guess string
        # If it's not a successful guess, decrement the chances counter

    # if Game.has_chances_left:
    #     Game.ask_for_guess()
    # else
    #     Game.end_message()

    # while no_of_chances <= 6:
    #     if no_of_chances == 0:
    #         print("Gameover, No chances Left!\n")
    #         play_again()
    #         break
    #     else:
    #         print(
    #             f"You have {no_of_chances} chances left\n")
    #         while True:
    #             user_guess = input('Enter your guess here:\n').lower().strip()

    #             if run_game.validate_user_guess(user_guess):
    #                 print('Guess is valid')
    #                 break

    #         no_of_chances -= 1

    #         if user_guess == answer:
    #             print('you win')
    #             play_again()
    #             break
    #         else:
    #             run_game.check_matching_letters(user_guess)


play_game = main()
