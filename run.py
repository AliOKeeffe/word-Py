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


# WORD = 'cheas'
# word_dict = {index : value for index, value in enumerate(WORD)}
# print(word_dict)
# USER_INPUT = 'books'

# class Wordle:


def get_game_word():
    """
    Open txt file and get random word
    """
    file = open('words.txt', 'r')
    lines = file.read().splitlines()
    file.close
    random_word = random.choice(lines)
    game_word_dict = {index: value for index, value in enumerate(random_word)}
    print(game_word_dict)
    return game_word_dict


# class Word():

#     def __init__(self, game_word_dict)


# https://www.codegrepper.com/code-examples/python/python+turn+char+list+to+dictionary
def get_user_guess():
    """
    Get  word guess input from ther user via the terminal
    which must be a string 5 characters long and an actual word in Oxford Dict
    Convert string into dictionary with index and character
    """
    while True:
        print("Please enter your guess")
        print("This should be 5 characters long and an actual word.")

        guess_str = input('Enter your guess here:\n').lower()
        your_guess = {}
        for index, value in enumerate(guess_str):
            your_guess[index] = value
        # user_input_dict = {index:value for index, value in enumerate(USER_INPUT)}

        if validate_user_guess(guess_str):
            print('Guess is valid')
            break
    return your_guess


def validate_user_guess(guess):
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


def check_matching_letters(game_word, user_guess):
    """
    Compare user guess against word
    """

    response_string = ""

    # if user_guess == game_word:
    #     print('Congratulations you have won!')

    # else:
    for ind, letr in user_guess.items():
        if letr == game_word[ind]:
            response_string += (Back.GREEN + letr)

        elif letr in game_word.values():
            response_string += (Back.YELLOW + letr)
            # need to ensure duplicate letter doesn't go orange if its already green
        else:
            response_string += (Back.RED + letr)

        # for i in range(0,5):
        #     if user_guess[i] == word_dict[i]:
        #         response_string += (Back.GREEN + user_guess[i])
        #         word_dict[i] = "-"

        #     elif user_guess[i] in word_dict.values():
        #         response_string += (Back.YELLOW + user_guess[i])

        #     else:
        #         response_string += (Back.RED + user_guess[i])

    print(response_string)
# def check_letter_in_word():


def introduction():
    """
    Introduction Message
    """
    print(pyfiglet.figlet_format("WELCOME TO WORD-PY", justify="center", width=80))

    print(Fore.GREEN + "Can you guess the word in 6 tries?\n".center(80))

    while True:
        username = input("Please enter your name to begin.\n")

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
    user_choice = input("Play Again? Y or N\n").lower()

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
    game_word = get_game_word()
    while no_of_chances <= 6:
        if no_of_chances == 0:
            print("Gameover, No chances Left!\n")
            play_again()
            break
        else:
            print(
                f"You have {no_of_chances} chances left\n")
            no_of_chances -= 1

            user_guess = get_user_guess()

            if user_guess == game_word:
                print('you win')
                play_again()
                break
            else:
                check_matching_letters(game_word, user_guess)


play_game = main()
