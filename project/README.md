WordGuess
=========

This environment is a recreation of the game [Wordle](https://www.nytimes.com/games/wordle/index.html); A game of deducing a hidden five-letter word through strategic guessing.

Action Space | Discrete(len(wordlist))
--- | --- | 
Observation Space | Text(min_length=5, max_length=5) |
Import | gymnasium.make("wordguess/WordGuess-v0") |

The guessing system uses letter placement and feedback to advance toward the solution. Feedback can only be obtained by submitting valid five-letter words as guesses, with each guess revealing which letters are correct (green), present but misplaced (yellow), or absent (gray).

Description
-----------

The game starts with a feedback reading of "| e | e | e | e | e |" indicating that no guess has been made yet. The player has six attempts at guessing the hidden word, and using the feedback from each guess to deduce the answer. 

Feedback can only be obtained by submitting valid five-letter words as guesses, with each guess revealing which letters are correct "C", present but misplaced (W), or absent (A)

Action Space
------------

The action space is any valid 5-letter string. Valid words are words that appear in the list of words used to draw out the hidden word.

e.g. "hello" "apple"

Observation Space
-----------------

The observation space is a 5 letter string denoting the feedback

e.g. "ccwae"

-   c → Correct letter and in correct position

-   w → Letter exists but in wrong position

-   a → Letter is absent

-   e → empty feedback, no guess made yet

Additionally the list of valid words used to select the hidden word is made available through a static method in the model

Starting State
--------------

The episode starts with the observation returning as "eeeee" indicating that no guesses have been made yet.

Reward
------

Each guess incurs -1 reward.

Episode End
-----------

The episode terminates when the player enters the hidden word.

Version History
---------------

-   v0: Initial version release
