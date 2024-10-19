# pseudo code
INFINITY = 1.e10
cutoff_depth = 4

def MINIMAX(initial_state, model, player):
    alpha = -INFINITY
    beta = INFINITY
    best_value = -INFINITY
    best_action = None
    for action in model.ACTIONS(initial_state):
        next_state = model.RESULT(initial_state, action, "Me")
        value = MIN(next_state, model, 0 + 1, alpha, beta, "Opponent")
        if value > best_value:
            best_value = value
            best_action = action
            if best_value > beta:
                break
            if best_value > alpha:
                alpha = best_value
    return best_action


def MAX(current_state, model, depth, alpha, beta, player):
    if depth >= cutoff_depth or model.GAME_OVER(current_state):
        return model.EVALUATE(current_state, player)
    best_value = -INFINITY
    for action in model.ACTIONS(current_state):
        next_state = model.RESULT(current_state, action, "Me")
        value = MIN(next_state, model, depth + 1, alpha, beta, "Opponent")
        if value > best_value:
            best_value = value
            if best_value > beta:
                break
            if best_value > alpha:
                alpha = best_value
    return best_value


def MIN(current_state, model, depth, alpha, beta, player):
    if depth >= cutoff_depth or model.GAME_OVER(current_state):
        return model.EVALUATE(current_state, player)
    best_value = INFINITY
    for action in model.ACTIONS(current_state):
        next_state = model.RESULT(current_state, action, "Opponent")
        value = MAX(next_state, model, depth + 1, alpha, beta, "Me")
        if value < best_value:
            best_value = value
            if best_value < alpha:
                break
            if best_value < beta:
                beta = best_value
    return best_value



