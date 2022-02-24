WORD = 'snakp'
word_dict = {index : value for index, value in enumerate(WORD)}
print(word_dict)
USER_INPUT = 'supep'

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




def check_matching_letters(user_guess):
    """
    Compare user guess again word
    """
    # # if user_guess == word_dict:
    #     # print('you win')
    # for letr in user_guess.values():
    #     if letr not in word_dict.values():
    #         print(f"word doesn't contain {letr}")
    # # This check if the letter is in the word and in the correct position (i.e green)
    # for letr in user_guess.values():
    #     if letr in word_dict.values():
    #         print(letr)

    # # This checks if the letter is in the word and in the correct position (i.e green)
    # for letr in user_guess.items():
    #     if letr in word_dict.items():
    #         print(letr)
 
    for ind,letr in user_guess.items():
        if letr == word_dict[ind]:
            print(f'Green {letr}')
        elif letr in word_dict.values():
            print(f'Orange {letr}')
        else:
            print(f'Grey {letr}')
 
    # word_dict.values()

    # word_dict.items()




# def check_letter_in_word():

user_guess = get_user_guess()
check_matching_letters(user_guess)