WordGuess
=========

A Gymnasium-compatible reinforcement learning environment based on [Wordle](https://www.nytimes.com/games/wordle/index.html), 
the popular word-guessing game.<br>
The environment trains and evaluates reinforcement learning agents on the task of deducing a hidden five-letter word through strategic guessing with limited attempts.

<br>

Action Space | Discrete(len(wordlist))
--- | --- | 
Observation Space | `Text(min_length=5, max_length=5)` |
Import | `gymnasium.make("wordguess/WordGuess-v0")` |

<br>

The guessing system uses letter placement and feedback to advance toward the solution. Feedback can only be obtained by submitting valid five-letter words as guesses, with each guess revealing which letters are correct (green), present but misplaced (yellow), or absent (gray).

Description
-----------

The game starts with a feedback reading of `"| e | e | e | e | e |"` indicating that no guess has been made yet. The player has six attempts at guessing the hidden word, and using the feedback from each guess to deduce the answer. 

Feedback can only be obtained by submitting valid five-letter words as guesses, with each guess revealing which letters are correct `"C"`, present but misplaced `"W"`, or absent `"A"`.

Action Space
------------

The action space is any valid 5-letter string. Valid words are words that appear in the list of words used to draw out the hidden word.

e.g. `"hello"` `"apple"`

Observation Space
-----------------

Observations are 5-character strings representing feedback for each letter position:

- **Type**: `Text(min_length=5, max_length=5)`
- **Feedback characters**:
  - `c` - **Correct**: Letter is in the correct position (green in Wordle)
  - `w` - **Wrong position**: Letter exists but in wrong position (yellow in Wordle)
  - `a` - **Absent**: Letter is not in the word (gray in Wordle)
  - `e` - **Empty**: No guess has been made yet

**Example**: `"ccwaa"` means the first two letters are correct, the third is in the word but wrong position, and the last two are absent.

Additionally the list of valid words used to select the hidden word is made available through a static method in the model

Starting State
--------------

The episode starts with the observation returning as `"eeeee"` indicating that no guesses have been made yet.

Reward
------

- Each guess incurs -1 reward
- The episode continues until the word is guessed correctly or all 6 attempts are exhausted
- Optimal strategy minimizes the number of guesses needed

Episode End
-----------

The episode terminates when the player enters the hidden word.

