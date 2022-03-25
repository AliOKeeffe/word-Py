"""
Defines the main() function which starts the game, along with the Game class
which is responsible for controlling the flow of the game.
"""

from datetime import date
import os
import random
import gspread
from google.oauth2.service_account import Credentials
import pyfiglet
import pandas as pd
import colorama
from colorama import Fore, Style
from modules.word_checker import WordChecker

colorama.init(autoreset=True)

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
    Open text file and get random word for the game answer.
    """
    file = open('words.txt', 'r', encoding='utf-8')
    lines = file.read().splitlines()
    random_word = random.choice(lines)
    return random_word.lower()


class Game:
    """
    This class is responsible for controlling the flow of the game. It handles
    things like taking the user input and presenting data back to the user.
    It contains methods for the general running of the game such as displaying
    the introduction, displaying user options, taking user guesses, displaying
    guesses, updating the leader board and displaying the leader board.
    """

    def __init__(self, word_checker):
        self.word_checker = word_checker
        self.guesses_list = []
        self.no_of_chances = 6
        self.username = ""
        self.leaderboard = SHEET.worksheet('leaderboard')

    def introduction(self):
        """
        Display introduction message and ask for username.
        Return error message if blank space is entered.
        Greet the user by their username.
        """
        print(pyfiglet.figlet_format(
            "WELCOME TO WORD-PY", justify="center", width=80))
        print(
            Fore.CYAN + Style.BRIGHT +
            "Can you guess the word in 6 tries?\n".center(80))
        while True:
            self.username = input(
                "Please enter your name to begin.\n").strip().capitalize()

            if len(self.username.strip()) == 0:
                print(f"{Fore.RED}Username must contain letters or numbers.\n")
            else:
                break
        print(f"{Fore.CYAN}\nHello {self.username}, welcome to Word-PY.\n")
        self.user_menu()

    def user_menu(self):
        """
        Ask the user if the wish to play or see the instructions.
        Return an error message if user inputs an invalid selection.
        """
        print('Please choose from the following options:\n')
        user_option = input(
            f"{Fore.CYAN}P - PLAY\nI - INSTRUCTIONS{Fore.RESET}\n"
            ).strip().lower()

        if user_option == "p":
            self.ask_for_guess()

        elif user_option == "i":
            #  Credit: https://www.asciiart.eu/art-and-design/borders
            intro_message = """
             __| |____________________________________________| |__
            (__   ____________________________________________   __)
               | |                                            | |
               | |               How to Play                  | |
               | |                                            | |
               | |    Guess the word in SIX or less tries     | |
               | |                                            | |
               | |  Each guess MUST be a valid 5 letter word  | |
               | |                                            | |
               | | After each guess, the color of the letters | |
               | |   will change to show how close your guess | |
               | |              was to the word!              | |
               | |                                            | |
               | |   Green is a correct letter and position   | |
               | | Yellow is a correct letter, wrong position | |
               | |           Red is a wrong letter            | |
             __| |____________________________________________| |__
            (__   ____________________________________________   __)
               | |                                            | |
            """
            print(intro_message)
            self.ask_for_guess()
        else:
            print(Fore.RED + "Not a valid option\n")
            self.user_menu()

    def play_again(self):
        """
        When the game ends ask the user if they wish to quit,
        view the leaderboard or play again.
        Return an error message if user inputs invalid selection.
        """
        print('Please choose from the following options:\n')
        user_choice = input(
            Fore.CYAN + "P - PLAY AGAIN\nL - LEADERBOARD\nQ - QUIT\n"
            ).strip().lower()

        if user_choice == "p":
            os.system('clear')
            main()

        elif user_choice == "q":
            print(" " + Fore.RESET)
            print(pyfiglet.figlet_format(
                    "GOODBYE", justify="center", width=80))
            exit()

        elif user_choice == "l":
            self.show_leaderboard()
            self.play_again()

        else:
            print(Fore.RED+"Not a valid option\n")
            self.play_again()

    def ask_for_guess(self):
        """
        Run a while loop to collect a valid guess from the user if they have
        chances remaining.
        If the user has no chances the the game is over.
        If the user guesses correctly, they win and leaderboard is updated.
        Display the game over menu.
        """
        while self.no_of_chances <= 6:
            if self.no_of_chances == 0:
                print(' \n')
                print(pyfiglet.figlet_format(
                    "GAME OVER", justify="center", width=80))
                fore = Fore.YELLOW + Style.BRIGHT
                upper_answer = self.word_checker.answer.upper()
                print(f"The answer was....{fore}{upper_answer}\n")
                self.play_again()
            else:
                fore = Fore.YELLOW + Style.BRIGHT
                chances = self.no_of_chances
                reset = Fore.RESET + Style.RESET_ALL
                print(f"\nYou have {fore}{chances}{reset} chances left.\n")
            while True:
                user_input = input(
                    'Enter your 5 letter guess here:\n').lower().strip()
                if self.word_checker.validate_user_guess(user_input):
                    self.no_of_chances -= 1
                    self.display_guesses(user_input)
                    if user_input == self.word_checker.answer:
                        score = 6 - self.no_of_chances
                        print(' \n')
                        print(pyfiglet.figlet_format(
                            "YOU WIN", justify="center", width=80))
                        print('\nWell done you got the correct answer!\n')
                        self.update_leaderboard(score)
                        self.play_again()
                    break

    def display_guesses(self, user_input):
        """
        Display the user's guess and previous guesses one after the
        other with color-codes.
        """
        current_guess = self.word_checker.check_matching_letters(user_input)
        self.guesses_list.append(current_guess)

        print(f"""\n{Fore.CYAN}\t\t\t      =====================\n""")
        for i in self.guesses_list:
            print("\t\t\t\t      "+i)
        print(f"""\n{Fore.CYAN}\t\t\t      =====================""")

    def update_leaderboard(self, score):
        """
        Add name, score and date to row in leaderboard Google Sheet.
        """
        today = date.today()
        date_format = today.strftime("%d/%m/%Y")
        print('Updating leaderboard...\n')
        self.leaderboard.append_row([self.username, score, date_format])
        print(Fore.CYAN + Style.BRIGHT + "Leaderboard Updated.\n")

    def show_leaderboard(self):
        """
        Get the leaderboard data from Google Sheets.
        Sort the leaderboard by date and then by number of attempts with Pandas
        Reset the table index and start it at 1.
        Show the top 10 entries in the leaderboard.
        Credit: https://realpython.com/pandas-sort-python/
        """
        scores = self.leaderboard.get_all_values()
        columns = scores[0]
        data = scores[1:]

        data_frame = pd.DataFrame(data, columns=columns)

        pd.set_option('display.colheader_justify', 'center')
        data_frame = data_frame.sort_values(
            by=['Date', 'Attempts'],
            ascending=[False, True])
        data_frame = data_frame.reset_index(drop=True)
        data_frame.index = data_frame.index + 1
        print(f"\n{Fore.CYAN}===============================\n")
        print(data_frame.head(10))
        print(f"\n{Fore.CYAN}===============================\n")


def main():
    """
    Retrieve an answer string from the words.txt file. Create a new instance of
    WordChecker, passing the answer as an parameter. Create a new instance of
    Game, passing the WordChecker instance as a parameter.
    Start the game using the introduction() method.
    """
    answer = get_answer_from_file()
    game = Game(WordChecker(answer))
    game.introduction()


main()
