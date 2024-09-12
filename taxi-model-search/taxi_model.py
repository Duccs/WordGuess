#!/usr/bin/env python3

ACTION_MOVE_DOWN = 0
ACTION_MOVE_UP = 1
ACTION_MOVE_RIGHT = 2
ACTION_MOVE_LEFT = 3
ACTION_PICK_UP = 4
ACTION_DROP_OFF = 5
ALL_ACTIONS = [ACTION_MOVE_DOWN, ACTION_MOVE_UP, ACTION_MOVE_RIGHT, ACTION_MOVE_LEFT, ACTION_PICK_UP, ACTION_DROP_OFF]

COLOR_POSITIONS = {
    0: (0, 0),  # Red
    1: (0, 4),  # Green
    2: (4, 0),  # Yellow
    3: (4, 3)  # Blue
}

OBSTACLES = [
(4, 0, '+'),
(4, 1, '-'),
(3, 0, '+'),
(3, 1, '-'),
(0, 1, '+'),
(0, 2, '-'),
(1, 1, '+'),
(1, 2, '-'),
(4, 2, '+'),
(4, 3, '-'),
(3, 2, '+'),
(3, 3, '-')
]

class TaxiModel:

    def __init__(self):
        self.x = None
        self.y = None
        self.pass_idx = None
        self.dest_idx = None
        self.state = None
        self.reset()
        return

    def reset(self):
        self.x, self.y, self.pass_idx, self.dest_idx, self.state = None, None, None, None, None
        self.time = 0
        return

    def decode_state(self, state):
        dest_idx = state % 4
        pass_idx = (state - dest_idx) // 4 % 5
        taxi_col = (state - pass_idx * 4 - dest_idx) // 20 % 5
        taxi_row = (state - taxi_col * 5 - pass_idx * 4 - dest_idx) // 100
        return taxi_row, taxi_col, pass_idx, dest_idx

    def encode_state(self, taxi_row, taxi_col, pass_idx, dest_idx):
        state = ((taxi_row * 5 + taxi_col) * 5 + pass_idx) * 4 + dest_idx
        return state

    def apply_decode(self, observation):
        self.x, self.y, self.pass_idx, self.dest_idx = self.decode_state(observation)
        return

    def get_color_index(self, color):
        return COLOR_POSITIONS.get(color, (0, 0))

    def get_taxi_position(self, state1):
        if state1 is None:
            return self.x, self.y
        return self.decode_state(state1)[0], self.decode_state(state1)[1]

    def is_move_blocked(self, current_row, current_col, move):
        for obstacle in OBSTACLES:
            obs_row, obs_col, direction = obstacle
            if move == 'right' and direction == '+' and current_row == obs_row and current_col == obs_col:
                return True
            if move == 'left' and direction == '-' and current_row == obs_row and current_col == obs_col:
                return True
        return False

    def ACTIONS(self, state):
        """Not allowed to move outside of the box, otherwise allowed."""
        row, column, pass_idx, dest_idx = self.decode_state(state)
        actions = []
        if column > 0 and not self.is_move_blocked(row, column, 'left'):
            actions.append(ACTION_MOVE_LEFT)
        if column < 4 and not self.is_move_blocked(row, column, 'right'):
            actions.append(ACTION_MOVE_RIGHT)
        if row > 0:
            actions.append(ACTION_MOVE_UP)
        if row < 4:
            actions.append(ACTION_MOVE_DOWN)
        return actions

    def GOAL_TEST(self, state):
        row, column, pass_idx, dest_idx = self.decode_state(state)
        return pass_idx == dest_idx

    def RESULT(self, state, action):
        row, column, pass_idx, dest_idx = self.decode_state(state)

        if action not in self.ACTIONS(state):
            return state

        if action == ACTION_MOVE_UP:
            row = max(0, row - 1)
        elif action == ACTION_MOVE_RIGHT:
            column = min(4, column + 1)
        elif action == ACTION_MOVE_LEFT:
            column = max(0, column - 1)
        elif action == ACTION_MOVE_DOWN:
            row = min(4, row + 1)
        else:
            raise Exception("Unexpected action: {}".format(action))

        return self.encode_state(row, column, pass_idx, dest_idx)
