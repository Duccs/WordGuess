#!/usr/bin/env python3
import numpy as np
import copy

ACTION_1 = 0
ACTION_2 = 1
ACTION_3 = 2
ACTION_4 = 3
ACTION_5 = 4
ACTION_6 = 5
ACTION_7 = 6
ALL_ACTIONS = [ACTION_1, ACTION_2, ACTION_3, ACTION_4, ACTION_5, ACTION_6, ACTION_7]

class ConnectFourModel:

    def __init__(self):
        self.reset()
        return

    def reset(self):
        return

    def ACTIONS(self, state):
        """Cannot place tokens in a full column."""
        actions = []
        if state["action_mask"][3] == 1:
            actions.append(ACTION_4)
        if state["action_mask"][5] == 1:
            actions.append(ACTION_6)
        if state["action_mask"][1] == 1:
            actions.append(ACTION_2)
        if state["action_mask"][2] == 1:
            actions.append(ACTION_3)
        if state["action_mask"][4] == 1:
            actions.append(ACTION_5)
        if state["action_mask"][0] == 1:
            actions.append(ACTION_1)
        if state["action_mask"][6] == 1:
            actions.append(ACTION_7)
        return actions

    def RESULT(self, state, action, player):
        # Illegal action handling
        s1 = copy.deepcopy(state)
        if action >= 7 or action < 0:
            raise Exception("Unexpected action: {}".format(action))

        observation = s1["observation"]
        for i in range(5, -1, -1):
            if observation[i][action][0] == 1 or observation[i][action][1] == 1:
                if i == 0:
                    raise Exception("Impossible action top of column reached: {}".format(action))
                continue
            else:
                if i == 0:
                    s1["action_mask"][action] = 0
                if player == "Me":
                    observation[i][action] = [1, 0]
                else:
                    observation[i][action] = [0, 1]
                break
        s1["observation"] = observation
        return s1

    # Check if game is over
    #   - Check for a win state
    #   - Check for a full board
    def GAME_OVER(self, state):
        if state["action_mask"].sum() == 0:
            return True
        # Check for player win
        piece = [1, 0]
        if self.Check_for_Winner(state, piece):
            return True
        # Check for opponent win
        piece = [0, 1]
        if self.Check_for_Winner(state, piece):
            return True
        return False

    # Check all possible win states and return
    # piece is either [1, 0] for Player or [0, 1] for Opponent
    # "Me" if a win state is found for the current player
    # "Opponent" if a win state is found for the opponent
    def Check_for_Winner(self, state, piece):
        # Check horizontal locations for win
        board = state["observation"]

        column_count = 7
        row_count = 6

        for c in range(column_count - 3):
            for r in range(row_count):
                if (
                        np.array_equal(board[r][c], piece)
                        and np.array_equal(board[r][c + 1], piece)
                        and np.array_equal(board[r][c + 2], piece)
                        and np.array_equal(board[r][c + 3], piece)
                ):
                    return True

        # Check vertical locations for win
        for c in range(column_count):
            for r in range(row_count - 3):
                if (
                        np.array_equal(board[r][c], piece)
                        and np.array_equal(board[r + 1][c], piece)
                        and np.array_equal(board[r + 2][c], piece)
                        and np.array_equal(board[r + 3][c], piece)
                ):
                    return True

        # Check positively sloped diagonals
        for c in range(column_count - 3):
            for r in range(row_count - 3):
                if (
                        np.array_equal(board[r][c], piece)
                        and np.array_equal(board[r + 1][c + 1], piece)
                        and np.array_equal(board[r + 2][c + 2], piece)
                        and np.array_equal(board[r + 3][c + 3], piece)
                ):
                    return True

        # Check negatively sloped diagonals
        for c in range(column_count - 3):
            for r in range(3, row_count):
                if (
                        np.array_equal(board[r][c], piece)
                        and np.array_equal(board[r - 1][c + 1], piece)
                        and np.array_equal(board[r - 2][c + 2], piece)
                        and np.array_equal(board[r - 3][c + 3], piece)
                ):
                    return True

        return False

    # Estimate the value of a state when the game is not over
    # Positive: indicating a good state for the player (e.g., a winning position)
    # Negative: indicating a bad state for the player (e.g., a losing position)
    def EVALUATE(self, state, player):
        # Initialize the score
        score = 0

        # Get the board from the state
        board = state["observation"]

        # Special Followup case
        if (state["observation"].sum() == 6 and np.array_equal(state["observation"][5][3], [1, 0])
                and np.array_equal(state["observation"][4][3], [0, 1])
                and np.array_equal(state["observation"][3][3], [1, 0])):
            return 10000

        # Check horizontal locations for score
        for r in range(6):
            for c in range(6):

                # Check for 2 pieces in a row
                if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r][c + 1], [1, 0]):
                    if player == "Me":
                        score += 1
                    else:
                        score -= 1
                elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r][c + 1], [0, 1]):
                    if player == "Me":
                        score -= 1
                    else:
                        score += 1

                # Check for 3 pieces in a row
                if c < 5:
                    if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r][c + 1], [1, 0]) and np.array_equal(
                            board[r][c + 2], [1, 0]):
                        if player == "Me":
                            score += 10
                        else:
                            score -= 10
                    elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r][c + 1], [0, 1]) and np.array_equal(
                            board[r][c + 2], [0, 1]):
                        if player == "Me":
                            score -= 10
                        else:
                            score += 10

                # Check for 4 pieces in a row
                if c < 4:
                    if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r][c + 1], [1, 0]) and np.array_equal(
                            board[r][c + 2], [1, 0]) and np.array_equal(board[r][c + 3], [1, 0]):
                        if player == "Me":
                            score += 1000
                        else:
                            score -= 1000
                    elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r][c + 1], [0, 1]) and np.array_equal(
                            board[r][c + 2], [0, 1]) and np.array_equal(board[r][c + 3], [0, 1]):
                        if player == "Me":
                            score -= 1000
                        else:
                            score += 1000

        # Check vertical locations for score
        for c in range(7):
            for r in range(5):

                # Check for 2 pieces in a row
                if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r + 1][c], [1, 0]):
                    if player == "Me":
                        score += 1
                    else:
                        score -= 1
                elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r + 1][c], [0, 1]):
                    if player == "Me":
                        score -= 1
                    else:
                        score += 1

                # Check for 3 pieces in a row
                if r < 4:
                    if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r + 1][c], [1, 0]) and np.array_equal(
                            board[r + 2][c], [1, 0]):
                        if player == "Me":
                            score += 10
                        else:
                            score -= 10
                    elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r + 1][c], [0, 1]) and np.array_equal(
                            board[r + 2][c], [0, 1]):
                        if player == "Me":
                            score -= 10
                        else:
                            score += 10

                # Check for 4 pieces in a row
                if r < 3:
                    if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r + 1][c], [1, 0]) and np.array_equal(
                            board[r + 2][c], [1, 0]) and np.array_equal(board[r + 3][c], [1, 0]):
                        if player == "Me":
                            score += 100
                        else:
                            score -= 100
                    elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r + 1][c], [0, 1]) and np.array_equal(
                            board[r + 2][c], [0, 1]) and np.array_equal(board[r + 3][c], [0, 1]):
                        if player == "Me":
                            score -= 100
                        else:
                            score += 100

        # Check positively sloped diagonals for score
        for c in range(6):
            for r in range(5):

                # Check for 2 pieces in a row
                if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r + 1][c + 1], [1, 0]):
                    if player == "Me":
                        score += 1
                    else:
                        score -= 1
                elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r + 1][c + 1], [0, 1]):
                    if player == "Me":
                        score -= 1
                    else:
                        score += 1

                # Check for 3 pieces in a row
                if r < 4 and c < 5:
                    if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r + 1][c + 1], [1, 0]) and np.array_equal(
                            board[r + 2][c + 2], [1, 0]):
                        if player == "Me":
                            score += 10
                        else:
                            score -= 10
                    elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r + 1][c + 1], [0, 1]) and np.array_equal(
                            board[r + 2][c + 2], [0, 1]):
                        if player == "Me":
                            score -= 10
                        else:
                            score += 10

                # Check for 4 pieces in a row
                if r < 3 and c < 4:
                    if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r + 1][c + 1],
                                                                              [1, 0]) and np.array_equal(
                            board[r + 2][c + 2], [1, 0]) and np.array_equal(board[r + 3][c + 3], [1, 0]):
                        if player == "Me":
                            score += 100
                        else:
                            score -= 100
                    elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r + 1][c + 1],
                                                                                [0, 1]) and np.array_equal(
                            board[r + 2][c + 2], [0, 1]) and np.array_equal(board[r + 3][c + 3], [0, 1]):
                        if player == "Me":
                            score -= 100
                        else:
                            score += 100

        # Check negatively sloped diagonals for score
        for c in range(6):
            for r in range(1, 6):

                # Check for 2 pieces in a row
                if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r - 1][c + 1], [1, 0]):
                    if player == "Me":
                        score += 1
                    else:
                        score -= 1
                elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r - 1][c + 1], [0, 1]):
                    if player == "Me":
                        score -= 1
                    else:
                        score += 1

                # Check for 3 pieces in a row
                if c in range(5) and r in range(2, 6):
                    if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r - 1][c + 1], [1, 0]) and np.array_equal(
                            board[r - 2][c + 2], [1, 0]):
                        if player == "Me":
                            score += 10
                        else:
                            score -= 10
                    elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r - 1][c + 1], [0, 1]) and np.array_equal(
                            board[r - 2][c + 2], [0, 1]):
                        if player == "Me":
                            score -= 10
                        else:
                            score += 10

                # Check for 4 pieces in a row
                if c in range(4) and r in range(3, 6):
                    if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r - 1][c + 1],
                                                                              [1, 0]) and np.array_equal(
                            board[r - 2][c + 2], [1, 0]) and np.array_equal(board[r - 3][c + 3], [1, 0]):
                        if player == "Me":
                            score += 100
                        else:
                            score -= 100
                    elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r - 1][c + 1],
                                                                                [0, 1]) and np.array_equal(
                            board[r - 2][c + 2], [0, 1]) and np.array_equal(board[r - 3][c + 3], [0, 1]):
                        if player == "Me":
                            score -= 100
                        else:
                            score += 100

        # Check for two pieces in a row
        for r in range(6):
            for c in range(5):
                if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r][c + 1], [1, 0]):
                    if player == "Me":
                        score += 10
                    else:
                        score -= 10
                elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r][c + 1], [0, 1]):
                    if player == "Me":
                        score -= 10
                    else:
                        score += 10

        # Check for two pieces in a column
        for c in range(7):
            for r in range(5):
                if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r + 1][c], [1, 0]):
                    if player == "Me":
                        score += 10
                    else:
                        score -= 10
                elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r + 1][c], [0, 1]):
                    if player == "Me":
                        score -= 10
                    else:
                        score += 10

        # Check for two pieces in a positively sloped diagonal
        for c in range(5):
            for r in range(5):
                if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r + 1][c + 1], [1, 0]):
                    if player == "Me":
                        score += 10
                    else:
                        score -= 10
                elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r + 1][c + 1], [0, 1]):
                    if player == "Me":
                        score -= 10
                    else:
                        score += 10

        # Check for two pieces in a negatively sloped diagonal
        for c in range(5):
            for r in range(1, 6):
                if np.array_equal(board[r][c], [1, 0]) and np.array_equal(board[r - 1][c + 1], [1, 0]):
                    if player == "Me":
                        score += 10
                    else:
                        score -= 10
                elif np.array_equal(board[r][c], [0, 1]) and np.array_equal(board[r - 1][c + 1], [0, 1]):
                    if player == "Me":
                        score -= 10
                    else:
                        score += 10

        return score


    # FIRST DRAFT EVALUATE BARE AND WEAK
    # def EVALUATE(self, state, player):
    #     value = 0
    #
    #     # Check for player win
    #     piece = [1, 0]
    #     if self.Check_for_Winner(state, piece):
    #         if player == "Me":
    #             value += 100
    #         else:
    #             value += -100
    #     # Check for opponent win
    #     piece = [0, 1]
    #     if self.Check_for_Winner(state, piece):
    #         if player == "Me":
    #             value += -100
    #         else:
    #             value += 100
    #     return value