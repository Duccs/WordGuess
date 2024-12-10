import copy
import json
import random

import numpy as np
from jumpy.lax import switch
from pkg_resources import resource_string


class WordGuessState:

    def __init__(self, size=5, difficulty=0):
        """0 == heads, 1 == tails"""
        self._letters = bytearray(b'hello')
        self._guesses = 6
        self._size = size
        self._last_guess = bytearray(b'eeeee') # 'e' No guess has been made
        self._word_list = self.fetch_legal_words(difficulty)
        return

    @property
    def size(self):
        return self._size

    def randomize(self, seed=None):
        if seed is not None:
            random.seed(seed)
        random_item = random.choice(self._word_list)
        self._letters = bytearray(random_item, 'utf-8')
        return self._letters

    def fetch_legal_words(self, difficulty=0):
        if difficulty == 0:
            json_string = resource_string('wordguess', 'data/word_list_3k.json').decode('utf-8')
        elif difficulty == 1:
            json_string = resource_string('wordguess', 'data/word_list_5k.json').decode('utf-8')
        elif difficulty == 2:
            json_string = resource_string('wordguess', 'data/word_list_14k.json').decode('utf-8')
        word_list = json.loads(json_string)
        return word_list

    def fetch_letter_frequency(self):
        with open('../data/sorted_letters.json', 'r') as f:
            sorted_letters = json.load(f)
        return sorted_letters

    # "ccwaa" Returns a string with characters representing the following
    # 'c' Correct: Letter is used in the correct place
    # 'w' Wrong: Letter is used but in the wrong place
    # 'a' Absent: Letter is not used
    # 'e' Empty: No Guess has been made
    def assert_guess(self, value):
        output = bytearray(b'aaaaa')
        answer = self._letters.copy()

        # First pass: mark correct letters
        for i in range(len(value)):
            if value[i] == answer[i]:
                output[i] = ord('c')
                answer[i] = 0  # Mark as used

        # Second pass: mark wrong-position letters
        for i in range(len(value)):
            if output[i] != ord('c'):  # Skip already correct letters
                if value[i] in answer:
                    output[i] = ord('w')
                    answer[answer.index(value[i])] = 0  # Mark as used

        return output

    def ensure_bytearray(self, value):
        if not isinstance(value, bytearray):
            if isinstance(value, str):
                return bytearray(value.encode('utf-8'))
            elif isinstance(value, np.ndarray):
                return bytearray(value)
            elif isinstance(value, bytes):
                return bytearray(value)
            else:
                raise TypeError(f"Cannot convert {type(value)} to bytearray")
        return value

    def guess(self, value):
        if self._guesses == 0:
            raise ValueError("No guesses left")
        # At this stage value should be a string
        value = str(value)
        value = value.strip().lower()
        if len(value) != self._size:
            raise ValueError(f"Expected {self._size} characters, got {len(value)}")
        if value not in self._word_list:
            raise ValueError(f"{value} is not a valid word")
        # Now value will be converted to a bytearray
        value = self.ensure_bytearray(value)
        output = self.assert_guess(value)
        self._last_guess = output
        self._guesses -= 1
        return output

    @property
    def observation(self):
        return self._last_guess

    @observation.setter
    def observation(self, value):
        value = self.ensure_bytearray(value)
        self._letters = value
        self._size = len(value)
        return

    def __str__(self):
        s = "|"
        for letter in self._last_guess:
            s += f" {chr(letter)} |"
        return s

class WordGuessModel:

    def ACTIONS(state):
        actions = state.fetch_legal_words()
        return actions

    def RESULT(state, action):
        state1 = copy.deepcopy(state)
        state1.guess(action)
        return state1

    def GOAL_TEST(state):
        return state._last_guess == bytearray(b'ccccc')

    def STEP_COST(state, action, state1):
        cost = 1
        return cost

    def HEURISTIC(state):
        estimated_cost = 0.0
        return estimated_cost

# For testing
if __name__ == "__main__":
    print("Number of words: ", len(WordGuessState().fetch_legal_words(difficulty=2)))
    state = WordGuessState()
    state.randomize()
    state._letters = bytearray(b'swims')
    while True:
        value = input("Enter your guess: ")
        try:
            assertion = state.guess(value)
        except Exception as e:
            print(e)
        print(state)


