# Python defaults
import pickle
import argparse
from typing import List, Tuple
from pathlib import Path

# Custom imports
import discrete_world.plotting as P
import discrete_world.design_obstacles as DO
from discrete_world import GridWorld as G
from discrete_world.agent import Agent

def readWorld(fp):
    """ Reads a grid-world from an .env file. """
    with open(fp, "rb") as data_file:
        data = pickle.load(data_file)
    return data


def main(env_file: Path, fig_dir: Path, create_obstacles: bool = False):
    # Define the grid-world start and goal locations
    rows = 5
    cols = 5
    init_pos = (rows - 1, 0)
    goals = [(0, cols - 1), (rows - 1, cols - 1)]
    goals = []
    obstacles = []  # type: List[Tuple[int, int]]
    p_slip = 0.8

    g = G(rows, cols, init_pos, goals, obstacles, p_slip)

    # Design the obstacles and save it in the env_file
    if create_obstacles:
        DO.create_world_wrapper(g, env_file)

    # Read the saved env_file
    g = readWorld(env_file)
    # Show the grid-world
    # g.render()

    # Define an agent or robot for the grid-world
    robot = Agent(g)

    # ----- This is where you define your RL agent. I just chose a random policy ----
    robot.gen_policy(1)

    # Show the plots of the grid-world and its reward
    # Image available in the fig_dir under parent.
    P.gen_plots(robot, fig_dir, env_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grid-World setup")
    parser.add_argument(
        "env_file", type=lambda p: Path(p).absolute(), help="Path to environment file",
    )
    parser.add_argument(
        "fig_dir",
        type=lambda p: Path(p).absolute(),
        default=Path(__file__).absolute().parent / "figs",
        help="Path to directory where figures should be stored",
    )
    parser.add_argument(
        "-d", "--design", action="store_true", help="design obstacles in PyGame"
    )
    args = parser.parse_args()

    fig_dir = args.fig_dir
    if not fig_dir.is_dir():
        fig_dir.mkdir(parents=True, exists_ok=True)

    create_obstacles = args.design

    env_file = args.env_file
    if not env_file.is_file() and not create_obstacles:
        raise ValueError("The given file {} does not exist".format(env_file))

    main(env_file, fig_dir, create_obstacles)
