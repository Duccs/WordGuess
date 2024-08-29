import gymnasium as gym

# Start environment
env = gym.make("LunarLander-v2")
observation, info = env.reset()

# Simple Reflex Agent
# Third Agent: Many adjustments and handling for several edge cases.
# Passes most cases, except some edge cases where it gets stuck. 
# Average Score over 100 episodes: ~ +160
def CurrAction(observation):

    # Extract relevant information from the observation
    x, y, vel_x, vel_y, angle, angular_velocity, left_leg_contact, right_leg_contact = observation

    # Check if both legs are in contact with the ground
    if y <= 0 and x > -0.1 and x < 0.1:
        return 0

    # Initialize action to do nothing
    action = 0

    # TODO: Adjust to either lean left or lean right depending on x position

    # Always aim for center
    if x > 0:
        action = 1
    elif x < 0:
        action = 3

    if x > 0.8:
        if angle > 0.1 or angular_velocity > 0.2:
            action = 3
        if angle < -0.2 or angular_velocity < -0.3:
            action = 1
    elif x < -0.8:
        if angle < -0.2 or angular_velocity < -0.3:
            action = 1
        if angle > 0.1 or angular_velocity > 0.2:
            action = 3
    else:
        # Fire left engine if tilting too much to the right
        if angle > 0.1 or angular_velocity > 0.2:
            action = 3

        # Fire right engine if tilting too much to the left
        if angle < -0.1 or angular_velocity < -0.2:
            action = 1

    # Fire main engine if falling too fast
    if y > 0.5 and x > -0.2 and x < 0.2:
        if vel_y < -0.5 and abs(angle) < 0.5:
            action = 2
    elif vel_y < -0.15 and abs(angle) < 0.5:
        action = 2

    #print(f"Debug: {x}")

    return action

# Initialize score
score = 0
average = 0
t = 1000

# Game loop
while t != 0:
    action = CurrAction(observation)
    observation, reward, terminated, truncated, info = env.step(action)

    score += reward

    if terminated or truncated:
        print(f"Score: {score}")
        average += score
        score = 0
        t -= 1
        observation, info = env.reset()

print(f"Average Score: {average/1000}")
env.close()

