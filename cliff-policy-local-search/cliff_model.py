#!/usr/bin/env python3
import gymnasium as gym
from gymnasium.wrappers import TimeLimit
import numpy as np

ACTION_MOVE_UP = 0
ACTION_MOVE_RIGHT = 1
ACTION_MOVE_DOWN = 2
ACTION_MOVE_LEFT = 3
ALL_ACTIONS = [ACTION_MOVE_UP, ACTION_MOVE_RIGHT, ACTION_MOVE_DOWN, ACTION_MOVE_LEFT]

class CliffWalkingModel:

    def __init__(self):
        self.env = gym.make("CliffWalking-v0", render_mode="none")
        self.env = TimeLimit(self.env, max_episode_steps=37)
        self.num_states = 37
        self.num_actions = 4
        self.reset()
        return

    def reset(self):
        self.time = 0
        self.env.reset()
        self.num_states = 37
        self.num_actions = 4
        return

    def decode_state(self, state):
        column = state % 12
        row = (state - column) // 12
        return (row, column)

    def encode_state(self, row, column):
        state = row * 12 + column
        return state

    def ACTIONS(self, state):
        """Not allowed to move outside of the box, otherwise allowed."""
        row, column = self.decode_state(state)
        actions = []
        if column > 0:
            actions.append(ACTION_MOVE_LEFT)
        if column < 11:
            actions.append(ACTION_MOVE_RIGHT)
        if row > 0:
            actions.append(ACTION_MOVE_UP)
        if row < 3:
            actions.append(ACTION_MOVE_DOWN)
        return actions

    def GOAL_TEST(self, state):
        return state == 47

    def RESULT(self, state, action):
        row, column = self.decode_state(state)
        if action == ACTION_MOVE_UP:
            row = max(0, row - 1)
        elif action == ACTION_MOVE_RIGHT:
            column = min(11, column + 1)
        elif action == ACTION_MOVE_LEFT:
            column = max(0, column - 1)
        elif action == ACTION_MOVE_DOWN:
            row = min(3, row + 1)
        else:
            raise Exception("Unexpected action: {}".format(action))
        
        if row == 3 and 0 < column < 11:
            row = 3
            column = 0

        state1 = self.encode_state(row, column)
        return state1

    def STEP_COST(self, state, action, next_state):
        if next_state in range(37, 47):
            return -100
        return 1

    # Factor in
    # - Steps to reach goal from state 36
    #                                (If policy cannot reach goal, massively penalize)
    #  + Number of Locations that can reach goal
    # - The total sum of steps to reach goal from every possible state
    #                                (if state fails to reach goal, moderately penalize)
    def UTILITY(self, policy):
        self.env.reset()
        # Optimal is 36
        # Priority : 2nd
        locations_that_goal = 0
        # Optimal is 13
        # Priority : 1st
        steps_from_36 = 0
        # Optimal is 283
        # Priority : 4th
        total_steps_to_goal = 0
        # Optimal is 0
        # Priority : 3rd
        total_falls = 0


        # Set up the game starting from every possible state
        for i in range(self.num_states):
            observation, info = self.env.reset()
            self.env.unwrapped.s = i

            round_steps = 0
            truncated = True
            # Play until the end of the episode
            done = False
            while not done:
                action = policy[observation]
                observation, reward, done, truncated, info = self.env.step(action)
                if reward == -100:
                    total_falls += 1
                round_steps += 1
                if round_steps >= 37:
                    truncated = True
                    break

            if not truncated:
                if i == 36:
                    steps_from_36 += round_steps
                total_steps_to_goal += round_steps
                locations_that_goal += 1
            # Failure to reach goal penalty
            if truncated:
                if i == 36:
                    steps_from_36 += 10000
                total_steps_to_goal += 100

        # Might raise exception
        self.env.close()

        utility = (locations_that_goal * 100 )- steps_from_36 - total_steps_to_goal - total_falls

        # Optimal jackpot hit
        if steps_from_36 == 13:
            # Blow up utility
            utility += 10000
        return utility

    # Return a random policy
    def RANDOM_STATE(self):
        policy = np.random.randint(0, self.num_actions, size=self.num_states)
        return policy

    def NEIGHBORS(self, policy):
        """Return all possible neighbors of the given policy."""
        neighbors = []
        for i in range(len(policy)):
            for action in ALL_ACTIONS:
                if policy[i] == action:
                    continue
                new_policy = policy.copy()
                new_policy[i] = action
                neighbors.append(new_policy)
        return neighbors