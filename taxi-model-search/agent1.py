#!/usr/bin/env python3

import taxi_model as taxi
import logging

class Agent1:

    def __init__(self):
        """required, with no arguments to initialize correctly"""
        self.model = taxi.TaxiModel()
        self.actions = []
        return

    def reset(self):
        """required"""
        self.model.reset()
        self.actions = []
        return

    def dfs(self, s0):
        logging.info("DFS: s0: ", s0)
        goal_node = None
        # NODE: (state, parent_node, action, depth)
        frontier = [ (s0, None, None, 0) ]
        while len(frontier) > 0:
            node = frontier.pop()
            state, parent, action, depth = node
            if self.model.GOAL_TEST(state):
                goal_node = node
                break
            elif depth >= self.max_depth:
                # do not generate children
                continue
            for action in self.model.ACTIONS(state):
                state1 = self.model.RESULT(state, action)
                node1 = (state1, node, action, depth+1)
                frontier.append(node1)
        action_sequence = []
        if goal_node:
            node = goal_node
            while node[1] is not None and node[1][1] is not None:
                node = node[1]
                action_sequence.append(node[2])
            if node[1][1] is None:
                action_sequence.append(node[2])
        logging.info("Action sequence: {}".format(action_sequence))
        logging.info("DFS: actions: ", action_sequence)
        return action_sequence
    
    def ids(self, state, goal):
        if self.model.GOAL_TEST(state):
            return
        depth = 0
        while True:
            result = self.dls(state, depth, goal)
            if result is not None:
                last_state, path = result
                self.model.state = last_state
                return path
            depth += 1

    def dls(self, state, depth_limit, goal):
        first_position = self.model.get_taxi_position(state)
        return self.recursive_dls(state, depth_limit, goal, [first_position])
    
    def recursive_dls(self, state, depth_limit, goal, path):
        position = self.model.get_taxi_position(state)
        if position == goal:
            return state, path + [position]
        elif depth_limit == 0:
            return None
        else:
            for action in self.model.ACTIONS(state):
                state1 = self.model.RESULT(state, action)
                position = self.model.get_taxi_position(state1)
                if position not in path:  # Avoid cycles
                    result = self.recursive_dls(state1, depth_limit - 1, goal, path + [position])
                    if result is not None:
                        return result
            return None
        
    def convert_path_to_actions(self, path):
        action_list = []
        for i in range(len(path) - 1):
            current = path[i]
            next = path[i + 1]
            if next[0] == current[0] - 1:
                action_list.append(1)  # Up
            elif next[0] == current[0] + 1:
                action_list.append(0)  # Down
            elif next[1] == current[1] - 1:
                action_list.append(3)  # Left
            elif next[1] == current[1] + 1:
                action_list.append(2)  # Right

        last_position = path[-1] if path else None
        return action_list
        
    def agent_function(self, state):
        """required"""
        if len(self.actions) == 0:

            # Process initial state into model
            self.model.apply_decode(state)

            # Create path from initial position to taxi to passenger
            path = self.ids(state, self.model.get_color_index(self.model.pass_idx))

            # Convert path to actions
            actions = self.convert_path_to_actions(path)

            # Append actions to passenger to action list
            self.actions.extend(actions)

            # Append Pick up action
            self.actions.append(4)

            # Update state with last state stored
            state = self.model.state

            # Create path from last state to destination
            path = self.ids(state, self.model.get_color_index(self.model.dest_idx))

            # Process for path to destination
            actions= self.convert_path_to_actions(path)
            self.actions.extend(actions)
            self.actions.append(5)
        if len(self.actions) == 0:
            raise Exception("IDS Search failed.")

        action = self.actions.pop(0)
        if action is None:
            logging.warn("state: {}".format(state))
            raise Exception("Oof!")
        return action
