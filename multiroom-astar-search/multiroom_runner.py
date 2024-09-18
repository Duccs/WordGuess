#!/usr/bin/env python3

from __future__ import annotations

import gymnasium as gym
import my_minigrids
from gymnasium import Env
from minigrid.core.actions import Actions
from minigrid.minigrid_env import MiniGridEnv
from minigrid.wrappers import ImgObsWrapper, RGBImgPartialObsWrapper
from minigrid.wrappers import FullyObsWrapper

import argparse
import logging
import sys

def create_environment(env_id, tile_size, render_mode, seed, max_episode_steps):
    env = gym.make(env_id, render_mode=render_mode, tile_size=tile_size,
                   agent_view_size=7,
                   screen_size=640)
    if seed:
        env.reset(seed=seed)
    if max_episode_steps:
        env = gym.wrappers.TimeLimit(env, max_episode_steps=max_episode_steps)

    return env

def fully_observable_env(env, tilesize):
    # env = RGBImgPartialObsWrapper(env, tilesize)
    # env = ImgObsWrapper(env)
    env = FullyObsWrapper(env)
    return env

def destroy_environment(env):
    env.close()
    return

def run_one_episode(env, agent):
    observation, info = env.reset()
    agent.reset()
    terminated = False
    truncated = False
    total_reward = 0
    while not (terminated or truncated):
        action = agent.agent_function(observation)
        observation, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
    return total_reward

def run_many_episodes(env, episode_count, agent):
    reward_sum = 0
    for i in range(episode_count):
        reward_sum += run_one_episode(env, agent)
    destroy_environment(env)
    reward = reward_sum / episode_count
    return reward

def parse_args(argv):
    parser = argparse.ArgumentParser(prog=argv[0], description='Run Taxi')
    parser.add_argument(
        "--episode-count",
        "-c",
        type=int,
        help="number of episodes to run",
        default=1
    )
    parser.add_argument(
        "--max-episode-steps",
        "-s",
        type=int,
        help="maximum number of episode steps (defaults to environment default)",
        default=0
    )
    parser.add_argument(
        "--logging-level",
        "-l",
        type=str,
        help="logging level: warn, info, debug",
        choices=("warn", "info", "debug"),
        default="warn",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="random seed to generate the environment with",
        default=None
    )
    parser.add_argument(
        "--render-mode",
        "-r",
        type=str,
        help="display style (render mode): human, none",
        choices=("human", "none"),
        default="human",
    )
    parser.add_argument(
        "--agent",
        "-a",
        type=str,
        help="agent function: random, agent1",
        choices=("agent1"),
        default="agent1",
    )
    parser.add_argument(
        "--env-id",
        type=str,
        help="gym environment to load",
        choices=gym.envs.registry.keys(),
        default="MiniGrid-MultiRoom-N6-S6-v0",
    )
    parser.add_argument(
        "--tile-size", type=int, help="size at which to render tiles", default=32
    )


    my_args = parser.parse_args(argv[1:])
    if my_args.logging_level == "warn":
        my_args.logging_level = logging.WARN
    elif my_args.logging_level == "info":
        my_args.logging_level = logging.INFO
    elif my_args.logging_level == "debug":
        my_args.logging_level = logging.DEBUG

    if my_args.render_mode == "none":
        my_args.render_mode = None
    return my_args

from agent1 import Agent1

def select_agent(agent_name):
    if agent_name == "agent1":
        agent_function = Agent1()
    else:
        raise Exception(f"unknown agent name: {agent_name}")
    return agent_function

def main(argv):
    args = parse_args(argv)
    logging.basicConfig(level=args.logging_level)

    env = create_environment(args.env_id, args.tile_size, args.render_mode, args.seed, args.max_episode_steps)
    env = fully_observable_env(env, args.tile_size)
    agent = select_agent(args.agent)
    reward = run_many_episodes(env, args.episode_count, agent)
    print(f"Reward: {reward}")
    return

if __name__ == "__main__":
    main(sys.argv)



