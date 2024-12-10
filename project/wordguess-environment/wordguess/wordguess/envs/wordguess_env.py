import gymnasium
import numpy as np
from gymnasium import Env
from gymnasium import spaces
from gymnasium.error import DependencyNotInstalled
from wordguess.envs.wordguess_model import WordGuessState, WordGuessModel

try:
    import pygame
except ImportError as e:
    raise DependencyNotInstalled(
        "pygame is not installed, `pip install` must have failed."
    ) from e


class WordGuessEnv(Env):
    metadata = {
        "render_modes": ["human", "rgb_array", "ansi"],
        "render_fps": 1,
    }

    def __init__(self, render_mode=None, letter_count=5, difficulty=0):
        self.render_mode = render_mode
        self.letter_count = letter_count
        self.difficulty = difficulty
        self.action_space = spaces.Discrete(len(WordGuessState().fetch_legal_words()))
        self.observation_space = spaces.Text(min_length=letter_count, max_length=letter_count)

        # display support
        self.cell_size = (800 // letter_count, 60)
        self.window_size = (
            self.letter_count * self.cell_size[0],
            1 * self.cell_size[1],
        )
        self.window_surface = None
        self.clock = None
        self.head_color = (255, 0, 0)
        self.tail_color = (0, 0, 255)
        self.background_color = (170, 170, 170)
        return

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.state = WordGuessState(self.letter_count, self.difficulty)
        self.state.randomize(seed)

        observation = self.state.observation.decode('utf-8')  # Convert bytearray to string
        info = {}
        return observation, info

    def step(self, action):
        state = self.state
        try:
            state1 = WordGuessModel.RESULT(state, action)
        except Exception as e:
            print(e)
            observation = self.state.observation.decode('utf-8')
            reward = 0
            terminated = WordGuessModel.GOAL_TEST(state)
            info = {}
            info['guesses_left'] = self.state._guesses
            return observation, reward, terminated, False, info
        self.state = state1

        observation = self.state.observation.decode('utf-8')
        reward = WordGuessModel.STEP_COST(state, action, state1)
        terminated = WordGuessModel.GOAL_TEST(state1)
        info = {}
        truncated = False
        info['guesses_left'] = self.state._guesses
        if self.state._guesses == 0:
            truncated = True
            info['correct_answer'] = self.state._letters.decode('utf-8')

        # display support
        if self.render_mode == "human":
            self.render()

        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode is None:
            assert self.spec is not None
            gymnasium.logger.warn(
                "You are calling render method without specifying any render mode. "
                "You can specify the render_mode at initialization, "
                f'e.g. gym.make("{self.spec.id}", render_mode="rgb_array")'
            )
            return

        if self.render_mode == "ansi":
            return self._render_text()
        else:
            return self._render_gui(self.render_mode)

    def _render_text(self):
        return str(self.state)

    def _render_gui(self, mode):
        if self.window_surface is None:
            pygame.init()
            pygame.display.set_caption("WordGuess")
            self.window_surface = pygame.display.set_mode(self.window_size)
            self.clock = pygame.time.Clock()

        self.window_surface.fill(self.background_color)

        for i, letter in enumerate(self.state.observation):
            color = self.head_color if letter == 0 else self.tail_color
            rect = pygame.Rect(
                i * self.cell_size[0], 0, self.cell_size[0], self.cell_size[1]
            )
            pygame.draw.rect(self.window_surface, color, rect)
        pygame.display.flip()
        self.clock.tick(self.metadata["render_fps"])

        if mode == "human":
            pygame.event.pump()
            pygame.display.update()
            self.clock.tick(self.metadata["render_fps"])
        else:  # rgb_array
            return np.transpose(
                np.array(pygame.surfarray.pixels3d(self.window_surface)), axes=(1, 0, 2)
            )

    def close(self):
        if self.window_surface is not None:
            pygame.display.quit()
            pygame.quit()
        return

# For testing
if __name__ == "__main__":
    env = WordGuessEnv()
    env.reset()
    for _ in range(1000):
        action = input("Action: ")
        observation, reward, terminated, truncated, info = env.step(action)
        print(observation, reward, terminated, truncated, info)
        print(env.state)
