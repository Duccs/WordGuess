#!/usr/bin/env python3

import gymnasium as gym
import wordguess

def agent_function():
    """
    state: A uniform_coins.UniformCoinsState object. The current state of the environment.

    returns: An integer, the coin to turn over.
    """
    action = input("Action: ")
    return action


def main():
    render_mode = "ansi"

    env = gym.make('wordguess/WordGuess-v0', render_mode=render_mode, letter_count=5,
                   max_episode_steps=20)
    observation, info = env.reset()
    terminated = truncated = False
    if render_mode == "ansi":
        print("Current state:", env.render())
    while not (terminated or truncated):
        action = agent_function()
        if render_mode == "ansi":
            print()
        observation, reward, terminated, truncated, info = env.step(action)
        if render_mode == "ansi":
            print("Current state:", env.render())
            print("Guesses left:", info['guesses_left'])
    if terminated:
        print("Congratulations! You guessed the word!")
    elif truncated:
        print(f"Game over! The correct answer was: {info['correct_answer']}")
    env.close()
    return


if __name__ == "__main__":
    main()


