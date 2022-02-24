WORD = 'snake'
USER_INPUT = 'trend'

# https://www.codegrepper.com/code-examples/python/python+turn+char+list+to+dictionary
def get_user_guess():
    """
    Get guess input from ther user via the terminal
    which must be a string 5 characters long
    """
    # print("Please enter your guess")
    # print("This should be 5 characters long and needs to be an actual word")

    # guess_str = input('Enter your guess here:\n')
    # my_dict = {}
    # for index, value in enumerate(guess_str):
        # my_dict[index] = value
    word_dict = {index:value for index, value in enumerate(WORD)}
    print(word_dict)
    
    user_input_dict = {index:value for index, value in enumerate(USER_INPUT)}
    print(user_input_dict)


get_user_guess()