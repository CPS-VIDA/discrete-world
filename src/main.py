# Python defaults
import os
import sys
import argparse
import pickle
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

import itertools

# Custom imports
from grid import GridWorld as G

# def create_demos(filename):
#     '''
#         Creates a dataset of demonstrations
#     '''
#     demo_list = []
#     curr_dir = os.getcwd()
#     filepath = os.path.join(curr_dir, filename)
#     with open(filepath, 'r') as foo:
#         contents = foo.readlines()
#     N = len(contents)
#     for line in contents:
#         l = line.strip()
#         demo_list.append(list(l.split(',')))
#     return N, demo_list

def test():
    rows = 5
    cols = 3
    init_pos = (rows-1, 0)
    goals = [(0, cols-1)]
    obstacles = []
    g = G(rows, cols, init_pos, goals, obstacles)
    g.render()
    g.reset()
    s = g.current_state
    for i in range(5):
        a = random.choice(g.action_space)
        s_, r, done = g.step(a)
        s = s_


if __name__ == '__main__':

    test()
    exit()
    parser = argparse.ArgumentParser(
        description='Grid-World setup to provide demonstrations')
    parser.add_argument('f', type=str, help='File name of environment')
    parser.add_argument('--d',
                        action='store_true',
                        help='Create a demonstration')
    args = parser.parse_args()

    give_demo = False
    if args.d: give_demo = args.d

    env_file = os.path.join(os.getcwd(), args.f)
    with open(env_file, "rb") as e_fp:
        data = pickle.load(e_fp)

    # Create a grid world
    n_rows = data.rows  # rows in grid
    n_cols = data.cols  # columns in grid
    print("Grid-world size: %d x %d" % (n_rows, n_cols))
    init_pos = data.init_pos  # initial position
    goals = data.goals  # goal position
    obstacles = data.obstacles
    grid_world = grid.GridWorld(n_rows, n_cols, init_pos, goals, obstacles)

    # p, c, pc = utilities.bfs(grid_world)
    # print("Path: ", p)
    # print("Path cost: ", c+1)
    # print("Coordinates: ", pc)

    demo_fname = args.f
    if sys.platform == 'win32':
        demo_fname = demo_fname.split("\\")[1]
    else:
        demo_fname = demo_fname.split('/')[1]
    demo_fname = demo_fname.split('.')[0]
    if not os.path.exists("demos"):
        os.makedirs("demos")

    # If you want to create a demo
    if give_demo: getDemo(grid_world, demo_fname)
    # Point to the demonstration file
    demo_file = "human_demos_{}.txt".format(demo_fname)
    demo_file = os.path.join(os.getcwd(), "demos", demo_file)
    fig_dir = "figures_{}".format(demo_fname)
    if not os.path.exists(fig_dir):
        os.makedirs(fig_dir)
