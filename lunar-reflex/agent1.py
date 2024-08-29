import gymnasium as gym

# Start environment
env = gym.make("LunarLander-v2")
observation, info = env.reset()

# Simple Reflex Agent
# First Agent: Keep descent at a safe speed and avoid tilting
# Will pass some cases
# Average Score over 1000 episodes: ~ -65
def CurrAction(observation):
    # Extract relevant information from the observation
    x, y, vel_x, vel_y, angle, angular_velocity, left_leg_contact, right_leg_contact = observation

    # Initialize action to do nothing
    action = 0

    # Fire main engine if falling too fast
    if vel_y < -0.2:
        action = 2

    # Fire left engine if tilting to the right
    if angle > 0.1:
        action = 3

    # Fire right engine if tilting to the left
    if angle < -0.1:
        action = 1

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