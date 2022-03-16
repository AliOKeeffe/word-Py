# Word-Py
Word-Py is a simple word guessing game that is based on the same idea as the popular game "Wordle". The user must guess the random 5 letter word within 6 tries and they will be given hints as they play. The user must guess carefully as their guess needs to be an actual word within the Oxford English Dictionary!

The game is a mixture of luck and logic. Not only does it allow the user to improve their problem solving and vocabulary skills but also gives them five minutes "timeout" in their busy day.  

The live link can be found here - [Word-Py](https://word-py.herokuapp.com/)

INSERT RESPONSINATOR IMAGE

## How to Play
- The user has 6 chances to guess a random 5 letter word.
- After each guess the user is provided with color coded blocks which let them know if their chosen letters are correct and in the right position;
  - Green means that the letter is in the word and is in the correct position.
  - Yellow means that the letter is in the word but is in the wrong position
  - Red means that the letter is not in the word. 
- The user must guess carefully as their guess needs to be an actual word within the Oxford English Dictionary.
- If the user guesses the correct word within 6 turns they have won the game. 
- The users score is saved to the leaderboard (only top 10 scores are shown.)

## Site Owner Goals
- To provide the user with simple game that is both challenging and rewarding.
- To present the user with an app that functions well and is easy to use. 
- To entice the user to return to the game to improve their score.

## User Stories

- ### First Time User
  - As a first time user I want to understand the main purpose of the game.
  - As a first time user I want to be kept engaged throughout the game by being provided with easy to understand hints as to how close my guess was to the answer.
  - As a first time user I want to be challenged by having to come up with an actual word and not just inputting random letters.
  - As a first time user I want to see how many turns I have left.
  - As a first time user I want to find out the answer if I am not successful.
  - As a first time user I want to compare my score to others on the leaderboard.

- ### Returning user
  - As a returning user I want to get a new word each time I play.
  - As a returning user I want to be able to beat my score on the leaderboard.
  - As a returning user I want to be able to beat other user's scores on the leaderboard.

Bugs
API keys for oxford dictionary
letter stays orange even if it's green