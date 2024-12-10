from gymnasium.envs.registration import register

from wordguess.envs.wordguess_env import WordGuessEnv
from wordguess.envs.wordguess_model import WordGuessModel
from wordguess.envs.wordguess_model import WordGuessState

register(
    id="wordguess/WordGuess-v0",

    entry_point="wordguess.envs:WordGuessEnv",

    max_episode_steps=20,
)
