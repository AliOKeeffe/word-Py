"""
Defines the Wordchecker class, which is responsible for all actions related to
checking the user-provided "guess" input against the generated "answer".
"""

from collections import Counter
import colorama
from colorama import Fore, Back
from modules.oxford_api import OxfordDictAPI

colorama.init(autoreset=True)


class WordChecker:
    """
    This class is responsible for all actions related to checking the
    user-provided "guess" input against the generated "answer". This includes
    validating the input, handling any errors and building the colour-coded
    response which is returned to the Game instance.
    """

    def __init__(self, answer):
        self.answer = answer

    def validate_user_guess(self, guess):
        """
        Check the user guess is valid.
        Guess must be letters only, 5 letters in length and an actual word
        in the Oxford English Dictionary.
        Raise ValueError if data is not valid.
        """
        try:
            if len(guess) != 5:
                raise ValueError('That is not a 5 letter word.\n')
            elif guess.isalpha() is False:
                raise ValueError('The game will only accept letters.\n')
            # If the return status is 404 (not found) then raise ValueError
            elif OxfordDictAPI().check_in_dict(guess) == 404:
                raise ValueError(
                    'Guess must be a word in the Oxford English Dictionary.\n'
                    )
        except ValueError as error:
            print(f'\n{Fore.RED}Invalid data: {error}Please try again. \n')
            return False

        return True

    def check_matching_letters(self, user_guess):
        """
        Compare user guess against answer and apply colour-codes based on
        accuracy of guess. Return string with colour coded guess.
        """

        letter_count = Counter(self.answer)

        user_guess_dict = {
            index: value for index, value in enumerate(user_guess)
            }

        response = {}

        for ind, letr in user_guess_dict.items():
            # If the provided letter is correct and in the correct position
            if letr == self.answer[ind]:
                response[ind] = {"value": letr, "color": "green"}
                letter_count[letr] -= 1

        for ind, letr in user_guess_dict.items():
            if letr != self.answer[ind]:
                # If the letter is in the word, but not in the correct position
                if letr in self.answer and letter_count[letr] != 0:
                    response[ind] = {"value": letr, "color": "yellow"}
                    letter_count[letr] -= 1
                # Else if the letter is not in the word
                else:
                    response[ind] = {"value": letr, "color": "red"}

        response_string = ""
        for key in sorted(response):
            value_dictionary = response[key]
            if value_dictionary["color"] == "green":
                response_string += (Back.GREEN)
            elif value_dictionary["color"] == "yellow":
                response_string += (Back.YELLOW)
            elif value_dictionary["color"] == "red":
                response_string += (Back.RED)
            response_string += Fore.BLACK + value_dictionary["value"].upper()

        return response_string
