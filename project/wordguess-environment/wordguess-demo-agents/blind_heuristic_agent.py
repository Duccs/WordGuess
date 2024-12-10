#!/usr/bin/env python3
from wordguess import WordGuessState
from collections import Counter
import gymnasium as gym
import functools

# English letter frequencies
LETTER_FREQ = {
    'e': 11.1607, 't': 9.3562, 'a': 8.4966, 'o': 7.5809, 'i': 7.5448,
    'n': 7.2397, 's': 6.3827, 'r': 6.2787, 'h': 5.9526, 'd': 4.2531,
    'l': 4.0125, 'u': 3.6285, 'c': 3.3725, 'm': 3.0129, 'f': 2.8004,
    'y': 2.1716, 'w': 2.0920, 'g': 2.0720, 'p': 2.0276, 'b': 1.5909,
    'v': 1.1364, 'k': 0.6900, 'x': 0.1965, 'q': 0.1962, 'j': 0.1532,
    'z': 0.0877
}

last_guess = None
possible_words = None
difficulty = 0

def agent_function(state):
    """
    state: A wordguess.WordGuessState object. The current state of the environment.

    returns: A 5-letter word as a string
    """
    global last_guess
    global possible_words

    if last_guess is None:
        # First guess, generate all possible 5-letter words
        possible_words = generate_possible_words(5)
    else:
        # Filter words based on previous guess and feedback
        possible_words = filter_words(possible_words, last_guess, state)

    # Get the best word from the remaining possibilities
    best_word = get_best_word(possible_words)
    last_guess = best_word
    return best_word

def filter_words(words, guess, feedback):
    return [word for word in words if all(
        (f == '2' and g == w) or
        (f == '1' and g in w and g != w[i]) or
        (f == '0' and g not in w)
        for i, (g, f, w) in enumerate(zip(guess, feedback, word))
    )]

# Cache frequently used code
@functools.lru_cache(maxsize=None)
def word_score(word):
    # Calculate frequency score
    frequency_score = sum(LETTER_FREQ[letter] for letter in set(word))

    # Calculate uniqueness score
    uniqueness_score = len(set(word)) / len(word)

    # Combine scores with weighting
    return (frequency_score * 0.7) + (uniqueness_score * 0.3)


def get_best_word(possible_words):
    return max(possible_words, key=word_score)

def generate_possible_words(length):
    import itertools
    return [''.join(word) for word in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=length)]

def main():
    render_mode = "ansi"
    num_episodes = 1000
    success_count = 0
    guesses_left = 0
    total_guesses = 0
    global s
    global word_list

    for episode in range(num_episodes):
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


