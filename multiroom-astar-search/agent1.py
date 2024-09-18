#!/usr/bin/env python3

from queue import PriorityQueue
import multiroom_model as multiroom
import logging


class Agent1:

    class Node:
        def __init__(self, state, parent, action, depth, cost, heuristic):
            self.state = state
            self.parent = parent
            self.action = action
            self.depth = depth
            self.cost = cost
            self.heuristic = heuristic

        def __lt__(self, other):
            return self.cost + self.heuristic < other.cost + other.heuristic

    def __init__(self):
        """required, with no arguments to initialize correctly"""
        self.model = multiroom.MultiRoomModel()
        self.actions = []
        return

    def reset(self):
        """required"""
        self.model.reset()
        self.actions = []
        return
    
    # A* Search
    # State is (agent_x,agent_y,direction, doors)
    # doors is a tuple of values every three values represent a door 4,0,1 or (type, color, state)
    # Duplicate doors may occur but should not affect the search
    # Node is (state, parent, action, depth, cost, heuristic)
    def astar_graph_search(self, s0):
        # Create a set to hold visited nodes
        visited = set()

        # Create a priority queue to hold nodes to be explored
        Q = PriorityQueue() # min-heap on cost+heuristic

        # Create a node for the initial state and add it to the queue
        # (state, parent, action, depth, cost, heuristic)
        n0 = self.Node(s0, None, None, 0, 0, self.model.HEURISTIC(s0))
        Q.put((n0.cost + n0.heuristic, n0)) # (priority, node)
        visited.add(s0)

        while(Q.qsize() > 0): # frontier not empty
            node = Q.get() # pops the node with the least heuristic
            # Separate node from the cost
            node = node[1]

            s, parent, action, depth, cost, heuristic = node.state, node.parent, node.action, node.depth, node.cost, node.heuristic
            # If the node is the goal state, reconstruct the path
            if self.model.GOAL_TEST(s):
                print("GOAL!")
                actions_taken = []
                while node.action is not None:
                    actions_taken.append(node.action)
                    # Go up the node tree
                    node = node.parent
                return actions_taken[::-1]

            for action in self.model.ACTIONS(s):
                s1 = self.model.RESULT(s, action)
                if s1 not in visited:
                    n1 = self.Node(s1, node, action, depth + 1, cost + self.model.STEP_COST(s, action, s1), self.model.HEURISTIC(s1))
                    Q.put((n1.cost + n1.heuristic, n1)) # (priority, node)
                    visited.add(s1)
        # If no path is found, return None
        return None

    def agent_function(self, state):
        """required"""
        if len(self.actions) == 0:
            # Process initial state into model
            self.model.state = state

            # Set agent position and identify doors to create a state
            agent_x, agent_y = self.model.find_agent_position(state)
            doors = self.model.identify_doors()

            # Initial state
            s0 = (agent_x, agent_y, state['direction'], doors)

            # Create path from initial state to taxi to goal
            actions_taken = self.astar_graph_search(s0)

            # Extend actions list with actions taken to reach a goal state
            print(actions_taken)
            print("debug_count: ", self.model.debug_count)
            self.actions.extend(actions_taken)

        if len(self.actions) == 0:
            raise Exception("A* Search failed.")

        action = self.actions.pop(0)
        if action is None:
            logging.warn("state: {}".format(state))
            raise Exception("Oof!")
        return action
