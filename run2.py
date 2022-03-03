# import to clear terminal
import os

# import random to get random word for game
import random

# import Acsii art library - pyfiglet
import pyfiglet

# import colorama for colour coding letters
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)


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


class Word:

    def __init__(self, game_word):
        self.game_word = game_word


    def validate_user_guess(self, guess):
        """
        Checks that user guess is valid - 5 letters and an actual word
        """
        try:
            if len(guess) != 5:
                raise ValueError(
                    'That is not a 5 letter word. \n'
                )
            elif guess.isalpha() is False:
                raise ValueError(
                    'Please only enter letters not numbers \n'
                )
            # need to add in check to see if its an actual word
        except ValueError as error:
            print(f'Invalid data: {error}Please try again. \n')
            return False

        return True


    def check_matching_letters(self, user_guess):
        """
        Compare user guess against word
        """

        response_string = ""

        user_guess_dict = {index: value for index, value in enumerate(user_guess)}
  
        for ind, letr in user_guess_dict.items():
            if letr == self.game_word[ind]:
                response_string += (Back.GREEN + letr)

            elif letr in self.game_word:
                response_string += (Back.YELLOW + letr)
                # need to ensure duplicate letter doesn't go orange if its already green
            else:
                response_string += (Back.RED + letr)
        print(response_string)


def introduction():
    """
    Introduction Message
    """
    print(pyfiglet.figlet_format("WELCOME TO WORD-PY", justify="center", width=80))

    print(Fore.GREEN + "Can you guess the word in 6 tries?\n".center(80))

    while True:
        username = input("Please enter your name to begin.\n").capitalize()

        if len(username.strip()) == 0:
            print(f"{Fore.RED}Name not valid!\n")
        else:
            break
    print(f"Hello {username}, welcome to Word-PY.\n")
    print("How to Play".center(80))
    print(f"""{Fore.MAGENTA}
    =======================================================\n""".center(80))
    print("Guess the word in 6 tries")
    print("Each guess MUST be a valid 5 letter word")
    print("After each guess, the color of the letters will change \
to show how close your guess was to the word")


def play_again():
    """
    when the game ends ask the user if they wish to quit or play again
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
        play_again()


def main():
    """
    Run all program functions
    """
    no_of_chances = 6
    introduction()
    answer = get_answer_from_file()
    run_game = Word(answer)
    while no_of_chances <= 6:
        if no_of_chances == 0:
            print("Gameover, No chances Left!\n")
            play_again()
            break
        else:
            print(
                f"You have {no_of_chances} chances left\n")
            while True:
                user_guess = input('Enter your guess here:\n').lower().strip()

                if run_game.validate_user_guess(user_guess):
                    print('Guess is valid')
                    break
                        
            no_of_chances -= 1

            if user_guess == answer:
                print('you win')
                play_again()
                break
            else:
                run_game.check_matching_letters(user_guess)


play_game = main()
