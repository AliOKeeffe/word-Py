# credit post by anna_ci in code institute slack channel
# https://code-institute-room.slack.com/archives/CP07TN38Q/p1576743956008500
from os import path
from datetime import date
import os  # import to clear terminal
import random  # import random to get random word for game
import gspread  # import gpsread
from google.oauth2.service_account import Credentials
import requests
import pyfiglet  # import Acsii art library - pyfiglet
import pandas as pd
import colorama  # import colorama for colour coding letters
from colorama import Fore, Back, Style

colorama.init(autoreset=True)

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
            #     raise ValueError(
            #         'Guess must be a word as per the Oxford Dictionary.\n'
            #         )
        except ValueError as error:
            print(f'Invalid data: {error}Please try again. \n')
            return False

        return True

    def check_matching_letters(self, user_guess):
        """
        Compare user guess against answer
        """
        response_string = ""

        user_guess_dict = {
            index: value for index, value in enumerate(user_guess)
            }

        for ind, letr in user_guess_dict.items():
            if letr == self.answer[ind]:
                response_string += (Back.GREEN + Fore.BLACK + letr.upper())

            elif letr in self.answer:
                response_string += (Back.YELLOW + Fore.BLACK + letr.upper())
                # need to ensure duplicate letter doesn't
                # go orange if its already green
            else:
                response_string += (Back.RED + Fore.BLACK + letr.upper())
        return response_string


class Game:
    """
    Creates and instance of the game
    """

    def __init__(self, word_checker):
        self.word_checker = word_checker
        self.guesses_list = []
        self.no_of_chances = 6
        self.username = ""
        self.leaderboard = SHEET.worksheet('leaderboard')

    def introduction(self):
        """
        Introduction Message
        """
        print(pyfiglet.figlet_format(
            "WELCOME TO WORD-PY", justify="center", width=80))
        print(Fore.GREEN + "Can you guess the word in 6 tries?\n".center(80))
        while True:
            self.username = input(
                "Please enter your name to begin.\n").capitalize()

            if len(self.username.strip()) == 0:
                print(f"{Fore.RED}Name not valid!\n")
            else:
                break
        print(f"\nHello {self.username}, welcome to Word-PY.\n")
        print('Please choose from the following options:\n')

        user_option = input(
            "P - PLAY\nI - Instructions\n").strip().lower()

        if user_option == "p":
            self.ask_for_guess()

        elif user_option == "i":
                    #  https://www.asciiart.eu/art-and-design/borders
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
            print("Not a valid option")
            self.play_again()

    def play_again(self):
        """
        When the game ends ask the user if they wish to quit or play again
        """
        user_choice = input(
            "P - PLAY AGAIN\nL - LEADERBOARD\nQ - QUIT\n").strip().lower()

        if user_choice == "p":
            os.system('clear')
            main()

        elif user_choice == "q":
            print("Goodbye. Hope to see you soon")
            exit()

        elif user_choice == "l":
            self.show_leaderboard()
            self.play_again()

        else:
            print("Not a valid option")
            self.play_again()

    def ask_for_guess(self):
        """
        Ask the user for their guess if they have chances remaining,
        if not the the game is over.
        If the user guesses correctly as them if they wish to play again.
        """
        while self.no_of_chances <= 6:
            if self.no_of_chances == 0:
                print("\nGameover, No chances Left!\n")
                self.play_again()
            else:
                print(f"\nYou have {self.no_of_chances} chances left.\n")
            while True:
                user_input = input('Enter your guess here:\n').lower().strip()
                if self.word_checker.validate_user_guess(user_input):
                    self.no_of_chances -= 1
                    self.display_guesses(user_input)
                    if user_input == self.word_checker.answer:
                        score = 6 - self.no_of_chances
                        print('\nWell done you got the correct answer!\n')
                        self.update_leaderboard(score)
                        self.play_again()
                    break

    def display_guesses(self, user_input):
        """
        Display the users guess one after the other with colors
        """
        current_guess = self.word_checker.check_matching_letters(user_input)
        self.guesses_list.append(current_guess)
        
        print(f"""\n{Fore.CYAN}\t=====================\n""")
        for i in self.guesses_list:
            print("\t\t"+i)
        print(f"""\n{Fore.CYAN}\t=====================""")

    def update_leaderboard(self, score):
        """
        Add name, score and date to row in leaderboard spreadsheet
        """
        today = date.today()
        # https://www.programiz.com/python-programming/datetime/current-datetime
        date_format = today.strftime("%d/%m/%Y")
        print('Updating leaderboard...\n')
        self.leaderboard.append_row([self.username, score, date_format])
        print("Leaderboard Updated.\n")

    def show_leaderboard(self):
        """
        Sort the leaderboard by date and then by number of attempts using
        Pandas then Show the top 10 entries in the leaderboard
        Credit: https://realpython.com/pandas-sort-python/
        """
        scores = self.leaderboard.get_all_values()
        columns = scores[0]
        data = scores[1:]

        df = pd.DataFrame(data, columns=columns)
        # https://www.tutorialspoint.com/python-center-align-column-headers-of-a-pandas-dataframe
        pd.set_option('display.colheader_justify', 'center')
        df.sort_values(
            by=['Date', 'Attempts'],
            ascending=[False, True]
            )
        df.reset_index(drop=True)
        print(df.head(10))


def main():
    """
    Run all program functions
    """

    game = Game(WordChecker(get_answer_from_file()))

    # Start the Game introduction (show the rules, ask for a name)
    game.introduction()
    # game.ask_for_guess()


main()
