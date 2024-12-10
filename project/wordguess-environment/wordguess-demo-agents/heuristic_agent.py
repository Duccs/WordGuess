#!/usr/bin/env python3
from wordguess import WordGuessState
from collections import Counter
import gymnasium as gym
import functools

last_guess = None
difficulty = 0
s = WordGuessState()
word_list = s.fetch_legal_words(difficulty)

def agent_function(state):
    """
    state: A wordguess.WordGuessState object. The current state of the environment.

    returns: A 5-letter word as a string
    """
    global last_guess
    global word_list

    feedback = state # Convert bytearray to string

    if feedback == "eeeee":
        # First guess: choose a word with common, diverse letters
        last_guess = get_best_word()
        return last_guess  # This is a common starting word in Wordle

    # Filter words based on previous guesses and feedback
    filter_words(feedback)

    # Choose the word that eliminates the most possibilities
    guess = get_best_word()

    # Update the last guess
    last_guess = guess
    return guess

def filter_words(feedback):
    global last_guess
    global word_list

    for i, (feedback_char, guess_char) in enumerate(zip(feedback, last_guess)):
        if feedback_char == 'c':
            word_list = [w for w in word_list if w[i] == guess_char]
        elif feedback_char == 'w':
            word_list = [w for w in word_list if guess_char in w and w[i] != guess_char]
        elif feedback_char == 'a':
            # Count the occurrences of the letter in the guess and feedback
            correct_count = sum(1 for f, g in zip(feedback, last_guess) if f in ['c', 'w'] and g == guess_char)

            # Filter words based on the count
            word_list = [w for w in word_list if w.count(guess_char) == correct_count and w[i] != guess_char]

    if not word_list:
        print(f"Word list is empty. Last guess: {last_guess}")

    return word_list

# Cache frequently used code
@functools.lru_cache(maxsize=None)
def word_score(word):
    # Count letter frequencies in the remaining word list
    letter_freq = Counter(''.join(word_list))

    # Normalize letter frequencies
    total_letters = sum(letter_freq.values())
    letter_freq = {letter: freq / total_letters for letter, freq in letter_freq.items()}

    # Calculate score based on letter frequency and uniqueness
    frequency_score = sum(letter_freq[letter] for letter in set(word))
    uniqueness_score = len(set(word)) / len(word)
    return (frequency_score * 0.7) + (uniqueness_score * 0.3)


def get_best_word():
    return max(word_list, key=word_score)


def main():
    render_mode = "ansi"
    num_episodes = 1000
    success_count = 0
    guesses_left = 0
    total_guesses = 0
    global s
    global word_list

    for episode in range(num_episodes):
        word_list = s.fetch_legal_words(difficulty)
        env = gym.make('wordguess/WordGuess-v0', render_mode=render_mode, letter_count=5, difficulty=difficulty,
                       max_episode_steps=20)
        observation, info = env.reset()
        terminated = truncated = False
        while not (terminated or truncated):
            action = agent_function(observation)
            observation, reward, terminated, truncated, info = env.step(action)
            total_guesses += 1

        if terminated:
            success_count += 1
            guesses_left += info['guesses_left']
            print("Success !! Guesses left:", info['guesses_left'])
            print()
        elif truncated:
            print(f"Episode {episode + 1}: The correct answer was: {info['correct_answer']}")
            print()

    print(f"\nResults after {num_episodes} episodes:")
    print(f"Total successes: {success_count}")
    print(f"Success rate: {success_count / num_episodes * 100}%")
    print(f"Average guesses left: {guesses_left / success_count}")
    print(f"Average guesses used: {total_guesses / success_count}")
    env.close()
    return


if __name__ == "__main__":
    main()


