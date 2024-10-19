from connect_four_model import ConnectFourModel
from alphabeta import MINIMAX

class ConnectFourAgent:
    def __init__(self):
        self.model = None
        self.reset()
        return

    def reset(self):
        self.model = ConnectFourModel()
        return

    def alphabeta(self, state):
        return MINIMAX(state, self.model, "Red")

    def agent_function(self, state, player):
        print("action mask: {}".format(state["action_mask"]))
        action = self.alphabeta(state)
        if state["action_mask"][action] == 0:
            raise Exception("Illegal action returned: {}".format(action))
        print("action: {}".format(action))
        if action not in range(7):
            raise Exception("Illegal action returned: {}".format(action))
        return action