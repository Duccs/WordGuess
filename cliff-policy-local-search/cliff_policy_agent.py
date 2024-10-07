from policy_search import policy_search

class PolicyAgent:
    def __init__(self, policy):
        self.policy = policy

    def reset(self):
        self.policy = []
        return

    def agent_function(self, state):
        if len(self.policy) == 0:
            self.policy = policy_search()

        if len(self.policy) == 0:
            raise Exception("Policy Search failed.")

        action = self.policy[state]
        return action