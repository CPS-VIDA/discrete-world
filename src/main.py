# Python defaults
import os
import sys
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

def main(env_file, create_obstacles=False):
    # Define the grid-world start and goal locations
    rows = 5
    cols = 5
    init_pos = (rows-1, 0)
    goals = [(0, cols-1), (rows-1, cols-1)]
    obstacles = []
    env_name = os.path.join(env_dir, env_file)
    g = G(rows, cols, init_pos, goals, obstacles)

    # Design the obstacles and save it in the env_file
    if create_obstacles:
        DO.create_world(g, env_name)

    # Read the saved env_file
    g = readWorld(env_name)
    # Show the grid-world
    # g.render()

    # Define an agent or robot for the grid-world
    robot = Agent(g)
    robot.gen_policy()

    # Show the plots of the grid-world and its reward 
    # Image available in the fig_dir under parent.
    P.gen_plots(robot, fig_dir)
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
        description='Grid-World setup to provide demonstrations')
    parser.add_argument('f', type=str, help='filename of environment with extension. Example: env1.env')
    parser.add_argument('--d',
                        action='store_true',
                        help='design obstacles in PyGame')
    args = parser.parse_args()

    env_file = args.f
    create_obstacles = args.d
    main(env_file, create_obstacles)