import gymnasium as gym

# Start environment
env = gym.make("LunarLander-v2")
observation, info = env.reset()

# Simple Reflex Agent
# Second Agent: Aim for the center and consider angular velocity, adjust some details
# Scores much higher. Will pass occasionally
# Average Score over 1000 episodes: ~ +85
def CurrAction(observation):
    # Extract relevant information from the observation
    x, y, vel_x, vel_y, angle, angular_velocity, left_leg_contact, right_leg_contact = observation

    # Check if both legs are in contact with the ground
    if left_leg_contact and right_leg_contact:
        return 0

    # Initialize action to do nothing
    action = 0

    # TODO: Adjust to either lean left or lean right depending on x position

    if x > 0:
        action = 1
    elif x < 0:
        action = 3

    # Fire left engine if tilting to the right
    if angle > 0.1 or angular_velocity > 0.2:
        action = 3

    # Fire right engine if tilting to the left
    if angle < -0.1 or angular_velocity < -0.2:
        action = 1

    # Fire main engine if falling too fast
    if vel_y < -0.2 and abs(angle) < 0.5:
        action = 2

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

