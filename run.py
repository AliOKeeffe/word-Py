# import colorama for adding colour
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

import random

# WORD = 'cheas'
# word_dict = {index : value for index, value in enumerate(WORD)}
# print(word_dict)
USER_INPUT = 'books'


def get_game_word():
    """
    Open txt file and get random word
    """
    f = open('words.txt', 'r')
    lines = f.read().splitlines()
    f.close
    random_word = random.choice(lines)
    game_word = {index : value for index, value in enumerate(random_word)}
    print(game_word)
    return game_word
    


# https://www.codegrepper.com/code-examples/python/python+turn+char+list+to+dictionary
def get_user_guess():
    """
    Get guess input from ther user via the terminal
    which must be a string 5 characters long
    Convert string into dictionary with index and character
    """
    # print("Please enter your guess")
    # print("This should be 5 characters long and needs to be an actual word")

    # guess_str = input('Enter your guess here:\n')
    # my_dict = {}
    # for index, value in enumerate(guess_str):
        # my_dict[index] = value

    user_input_dict = {index:value for index, value in enumerate(USER_INPUT)}
    print(user_input_dict)

    return user_input_dict




def check_matching_letters(game_word, user_guess):
    """
    Compare user guess against word
    """

    response_string = ""

    if user_guess == game_word:
        print('Congratulations you have won!')

    else:
        for ind,letr in user_guess.items():
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


game_word = get_game_word()
user_guess = get_user_guess()
check_matching_letters(game_word, user_guess)