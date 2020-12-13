# Python defaults
import os
import argparse
import pickle
import random

# Custom imports
import design_obstacles as DO
import plotting as P
from agent import Agent
from grid import GridWorld as G

def readWorld(fp):
    """ Reads a grid-world from an .env file. """
    with open(fp, 'rb') as data_file:
        data = pickle.load(data_file)
    return data

def main(env_name, create_obstacles=False):
    # Define the grid-world start and goal locations
    rows = 5
    cols = 5
    init_pos = (0, 0)
    goals = [(rows-1, cols-1)]
    obstacles = []
    p_slip = 0.1
    env_file = os.path.join(env_dir, env_name+".env")
    g = G(rows, cols, init_pos, goals, obstacles, p_slip)

    # Design the obstacles and save it in the env_file
    if create_obstacles:
        DO.create_world(g, env_file)

    # Read the saved env_file
    g = readWorld(env_file)
    # Show the grid-world
    # g.render()

    # Define an agent or robot for the grid-world
    robot = Agent(g)

    # ----- This is where you define your RL agent. I just chose a random policy ----
    params = {'min_eps': 0.01, 'n_episodes': 5000, 'gamma': 0.999, 'alpha': 0.5}
    # robot.learner(params)
    # robot.gen_policy(option=3)
    # print(robot.q_table)
    print(robot)
    a = robot.world.choose_action('L')
    print('L', random.choice(a))

    # Show the plots of the grid-world and its reward 
    # Image available in the fig_dir under parent.
    # P.gen_plots(robot, fig_dir, env_name)

if __name__ == '__main__':
    # All environment files are saved in the 'env' folder
    env_dir = os.path.join(os.pardir, "envs")
    if not os.path.exists(env_dir):
        os.makedirs(env_dir)
    
    # All figures are saved in 'figs' folder and then go figure
    fig_dir = os.path.join(os.pardir, "figs")
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)

    parser = argparse.ArgumentParser(
        description='Grid-World setup')
    parser.add_argument('f', type=str, help='filename of environment; automatically appends .env extension: Example: env1')
    parser.add_argument('--d',
                        action='store_true',
                        help='design obstacles in PyGame')
    args = parser.parse_args()

    env_name = args.f
    create_obstacles = args.d
    main(env_name, create_obstacles)