#!/usr/bin/env python3
import minigrid.core.constants as cons
import numpy as np
import math

ACTION_TURN_LEFT = 0
ACTION_TURN_RIGHT = 1
ACTION_MOVE_FORWARD = 2
ACTION_TOGGLE = 5
ALL_ACTIONS = [ACTION_TURN_LEFT, ACTION_TURN_RIGHT, ACTION_MOVE_FORWARD, ACTION_TOGGLE]

class MultiRoomModel:

    def __init__(self):
        self.state = None
        self.debug_count = 0
        self.reset()
        return

    def reset(self):
        self.state = None
        self.debug_count = 0
        self.time = 0
        return

    # Return legal actions in the current state
    def ACTIONS(self, state):
        actions = []
        # Agent can turn left or right at all times
        actions.append(ACTION_TURN_LEFT)
        actions.append(ACTION_TURN_RIGHT)
        
        # look ahead to the next cell
        _type, _, _state = self.look_ahead(state)

        # If facing a door add toggle, if door is open allow movement
        if _type == cons.OBJECT_TO_IDX['door']:
            if _state == 0:
                actions.append(ACTION_MOVE_FORWARD)
            else:
                actions.append(ACTION_TOGGLE)
        # If next cell is empty/goal/deprecated_agent allow movement
        if _type == cons.OBJECT_TO_IDX['empty'] or _type == cons.OBJECT_TO_IDX['goal'] or _type == cons.OBJECT_TO_IDX['agent']:
            actions.append(ACTION_MOVE_FORWARD)

        return actions
    
    # Return the next state after taking the action
    def RESULT(self, state, action):
        # Check if action is valid, this should never happen in the first place
        if action not in self.ACTIONS(state):
            return state
        
        x, y, direction, doors = state
        # Use cosine for xdif and sine for ydif
        # Add value to x or y to move cell in faced direction
        xdif = int(math.cos(math.pi / 2 * direction))
        ydif = int(math.sin(math.pi / 2 * direction))
        if action == ACTION_TURN_RIGHT:
            direction = (direction + 1) % 4
            return x, y, direction, doors
        elif action == ACTION_TURN_LEFT:
            direction = (direction - 1) % 4
            return x, y, direction, doors
        elif action == ACTION_MOVE_FORWARD:
            x = x + xdif
            y = y  + ydif
            return x, y, direction, doors
        elif action == ACTION_TOGGLE:
            # Get the door values
            _type, _color, _state = self.look_ahead(state)

            if _state == 0:
                raise Exception("Locked myself in !!!! Door was already open?!")

            # Mark door cell as empty
            self.state['image'][x + xdif, y + ydif] = [1, 0, 0]
            # Remove door from tuple
            doors = self.remove_door(doors, _type, _color, _state)
            return x, y, direction, doors
        else:
            raise Exception("Unexpected action: {}".format(action))
        
    # Check if the goal has been reached
    def GOAL_TEST(self, state):
        goal_position = self.find_goal_position()
        x, y, d, _ = state
        if x == goal_position[0] and y == goal_position[1]:
            return True
        return False
    
    # Cost of taking action a in state s and ending up in state s1
    def STEP_COST(self, state, action, next_state):
        return 1
    
    # Estimated cost of reaching a goal state from state s.
    def HEURISTIC(self, state):
        # Calculate the Manhattan distance between the agent's current position and the goal
        agent_x, agent_y, _, _ = state
        goal_x, goal_y = self.find_goal_position()
        distance = abs(agent_x - goal_x) + abs(agent_y - goal_y)

        self.debug_count += 1
        return distance

    # Find the position of the agent in the image
    # State passed must be the environment observation
    # Should only be used to initialize first state
    def find_agent_position(self, observation):
        image = observation['image']
        
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                if image[x, y, 0] == cons.OBJECT_TO_IDX['agent']:
                    return x, y
        return None

    # Find the position of an object in the image using its 3 values
    # Duplicates exist, will return first find only
    def find_object_position(self, obj_type, obj_color, obj_state):
        image = self.state['image']
        
        obj = (obj_type, obj_color, obj_state)
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                if tuple(image[x, y]) == obj:
                    return x, y
        return None
    
    def find_goal_position(self):
        return self.find_object_position(cons.OBJECT_TO_IDX['goal'], cons.COLOR_TO_IDX['green'], 0)

    # Return the 3 values of the cell facing the agent
    # (Type, Color, State)
    def look_ahead(self, state):
        image = self.state['image']

        x, y, direction, _ = state
        if direction == 0:
            return image[x + 1, y]
        elif direction == 1:
            return image[x, y + 1]
        elif direction == 2:
            return image[x - 1, y]
        elif direction == 3:
            return image[x , y - 1]
        else:
            raise Exception("Unexpected direction: {}".format(direction))

    # Look up doors in the image
    # for use to initialize the first state
    # doors toggled in RESULT() may be marked as empty cell in the image
    def identify_doors(self):
        image = self.state['image']
        doors = ()
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                if image[x, y][0] == cons.OBJECT_TO_IDX['door']:
                    door = image[x, y][0], image[x, y][1], image[x, y][2] # type, color, state
                    doors = doors + door
        return doors

    # Remove a door from the doors tuple used in state
    def remove_door(self, doors,_type, _color, _state):
        new_doors = ()
        # One remove per call only
        one_remove_flag = False
        # Every three tuples represent a door
        for i in range(0, len(doors), 3):
            door = doors[i:i+3]
            door_type, door_color, door_state = door

            # If the door is a match do not include in new tuple
            if door_type == _type and door_color == _color and door_state == _state and not one_remove_flag:
                one_remove_flag = True
                continue
            else:
                new_doors = new_doors + door
        return new_doors