#!/usr/bin/env python3

import cliff_model
import local_search

def policy_search():
    policy = hillclimb(1, -3700)
    return policy.tolist()

def hillclimb(desired_restarts, desired_utility):
    model = cliff_model.CliffWalkingModel()
    solution = local_search.RandomRestartHillClimbing(model, desired_restarts, desired_utility)
    print(f"Best policy found: {model.UTILITY(solution)} {solution}")
    print_policy(solution)
    return solution

def print_policy(solution):
    translate = {0: "U", 1: "R", 2: "D", 3: "L"}

    output = ""
    for i in range(12):
        output = output + translate[solution[i]] + " "
    print(output)
    output = ""
    for i in range(12, 24):
        output = output + translate[solution[i]] + " "
    print(output)
    output = ""
    for i in range(24, 36):
        output = output + translate[solution[i]] + " "
    print(output)
    output = ""
    for i in range(36, 47):
        if i == 36:
            output = output + translate[solution[i]] + " "
        if i == 46:
            output = output + "G"
        else:
            output = output + "C "
    print(output)
    return