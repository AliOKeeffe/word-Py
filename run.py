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
from collections import Counter

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
    print(random_word.lower())
    return random_word.lower()


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
        Credit post by anna_ci in code institute slack channel
        https://code-institute-room.slack.com/archives/CP07TN38Q/p1576743956008500
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
        # https://stackoverflow.com/questions/1155617/count-the-number-of-occurrences-of-a-character-in-a-string

    def validate_user_guess(self, guess):
        """
        Checks that user guess is valid - 5 letters and an actual word
        """
        try:
            if len(guess) != 5:
                raise ValueError('That is not a 5 letter word.\n')
            elif guess.isalpha() is False:
                raise ValueError('Please only enter letters not numbers.\n')
            # if the return status is 404(not found) then raise vaidation error
            # elif OxfordDictAPI().check_in_dict(guess) == 404:
            #     raise ValueError(
            #         'Guess must be a word as per the Oxford Dictionary.\n'
            #         )
        except ValueError as error:
            print(f'{Fore.RED}Invalid data: {error}Please try again. \n')
            return False

        return True

    def check_matching_letters(self, user_guess):
        """
        Compare user guess against answer
        """
        letter_count = Counter(self.answer)

        user_guess_dict = {
            index: value for index, value in enumerate(user_guess)
            }

        response = {}

        for ind, letr in user_guess_dict.items():  # for every letter in the guess
            if letr == self.answer[ind]:  # if it's in the word and in the right place
                response[ind] = {"value": letr, "color": "green"}  # define it as green
                letter_count[letr] -= 1  # subtract 1 from that letter's count

        for ind, letr in user_guess_dict.items():  # for every letter in the guess
            if letr != self.answer[ind]:  # if it's not already gone green
                if letr in self.answer and letter_count[letr] != 0:  # if the letter is in the word and the letter's count is not 0
                    response[ind] = {"value": letr, "color": "yellow"}  # define it as yellow
                    letter_count[letr] -= 1  # subtract 1 from that letter's count
                else:
                    response[ind] = {"value": letr, "color": "red"}  # define it as red

        response_string = ""
        for key in sorted(response):  # we need to sort the dictionary by the index - the dictinoary is ordered based on when the item was added, which will be based on the conditions above, as opposed to the order the user entered the characters
            value_dictionary = response[key]
            if value_dictionary["color"] == "green":
                response_string += (Back.GREEN)
            elif value_dictionary["color"] == "yellow":
                response_string += (Back.YELLOW)
            elif value_dictionary["color"] == "red":
                response_string += (Back.RED)
            response_string += Fore.BLACK + value_dictionary["value"].upper()

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
        """
        print('Please choose from the following options:\n')
        user_option = input(
            f"{Fore.MAGENTA}P - PLAY\nI - INSTRUCTIONS{Fore.RESET}\n"
            ).strip().lower()

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
            print(Fore.RED+"Not a valid option\n")
            self.user_menu()

    def play_again(self):
        """
        When the game ends ask the user if they wish to quit or play again
        """
        print('Please choose from the following options:\n')
        user_choice = input(
            Fore.MAGENTA + "P - PLAY AGAIN\nL - LEADERBOARD\nQ - QUIT\n"
            ).strip().lower()

        if user_choice == "p":
            os.system('clear')
            main()

        elif user_choice == "q":
            print(" " + Fore.RESET)
            print(pyfiglet.figlet_format(
                    "Goodbye", justify="center", width=80))
            exit()

        elif user_choice == "l":
            self.show_leaderboard()
            self.play_again()

        else:
            print(Fore.RED+"Not a valid option\n")
            self.play_again()

    def ask_for_guess(self):
        """
        Ask the user for their guess if they have chances remaining,
        if not the the game is over.
        If the user guesses correctly as them if they wish to play again.
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
        Display the users guess one after the other with colors
        """
        current_guess = self.word_checker.check_matching_letters(user_input)
        self.guesses_list.append(current_guess)

        print(f"""\n{Fore.CYAN}\t\t\t      =====================\n""")
        for i in self.guesses_list:
            print("\t\t\t\t      "+i)
        print(f"""\n{Fore.CYAN}\t\t\t      =====================""")

    def update_leaderboard(self, score):
        """
        Add name, score and date to row in leaderboard spreadsheet
        """
        today = date.today()
        # https://www.programiz.com/python-programming/datetime/current-datetime
        date_format = today.strftime("%d/%m/%Y")
        print('Updating leaderboard...\n')
        self.leaderboard.append_row([self.username, score, date_format])
        print(Fore.CYAN + Style.BRIGHT + "Leaderboard Updated.\n")

    def show_leaderboard(self):
        """
        Sort the leaderboard by date and then by number of attempts using
        Pandas then Show the top 10 entries in the leaderboard
        Credit: https://realpython.com/pandas-sort-python/
        """
        scores = self.leaderboard.get_all_values()
        columns = scores[0]
        data = scores[1:]

        data_frame = pd.DataFrame(data, columns=columns)
        # https://www.tutorialspoint.com/python-center-align-column-headers-of-a-pandas-dataframe
        pd.set_option('display.colheader_justify', 'center')
        data_frame = data_frame.sort_values(
            by=['Date', 'Attempts'],
            ascending=[False, True])
        data_frame = data_frame.reset_index(drop=True)
        data_frame.index = data_frame.index + 1  # start the index at 1 instead of 0
        print(f"\n{Fore.CYAN}==============================\n")
        print(data_frame.head(10))
        print(f"\n{Fore.CYAN}==============================\n")


def main():
    """
    Run all program functions
    """
    answer = get_answer_from_file()
    game = Game(WordChecker(answer))
    # Start the Game introduction (show the rules, ask for a name)
    game.introduction()


main()
