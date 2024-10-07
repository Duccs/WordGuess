INFINITY = 1.e10

def RandomRestartHillClimbing(model, desired_restarts, desired_utility):
    """
    Repeatedly execute HillClimbing() on random starting states.
    """
    best_peak = model.RANDOM_STATE()
    while model.UTILITY(best_peak) < desired_utility:
        for i in range(desired_restarts):
            s0 = model.RANDOM_STATE()
            peak = HillClimbing(s0, model)
            if model.UTILITY(peak) > model.UTILITY(best_peak):
                best_peak = peak
    return best_peak

def HillClimbing(s0, model):
    """
    Find state with largest obtainable utility function value.
    """
    current_state = s0
    while True:
        best_utility = -INFINITY
        best_neighbor = None

        for neighbor in model.NEIGHBORS(current_state):
            if model.UTILITY(neighbor) > best_utility:
                best_utility = model.UTILITY(neighbor)
                best_neighbor = neighbor
        if best_utility > model.UTILITY(current_state):
            current_state = best_neighbor
        else:
            break
    return current_state