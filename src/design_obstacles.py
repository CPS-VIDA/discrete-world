"""
 Example program to show using an array to back a grid on-screen.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/mdTeqiWyFnc
"""
import pygame, os, argparse, csv, json, pickle
import grid
# from collections import Collection


def getAction(s1, s2):
    x1, y1 = s1
    x2, y2 = s2
    if (x1 == x2):
        if y2 > y1: return 'R'
        else: return 'L'
    elif (y1 == y2):
        if x2 > x1: return 'D'
        else: return 'U'


def mapping(states):
    N = len(states)
    s = states[0]
    action_list = []
    for i in range(1, N):
        s_ = states[i]
        action_list.append(getAction(s, s_))
        s = s_
    return action_list


def createWorld(grid_world, filepath):
    # Define some colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    NAVY = (150, 150, 255)
    LIGHTB = (75, 75, 255)

    state_colors = {
        'road': WHITE,
        'goal': NAVY,
        'start': LIGHTB,
        'obs': RED,
        'occ': GREEN
    }

    START = 1  # Start
    GOAL = 2  # Goal
    OBS = 3  # Obstacle
    OCC = 10  # Occupy demonstration state

    # This sets the WIDTH and HEIGHT of each grid location
    WIDTH = 20
    HEIGHT = 20

    # This sets the margin between each cell
    MARGIN = 5

    # Create a 2 dimensional array. A two dimensional
    # array is simply a list of lists.
    sz = grid_world.rows
    grid = []
    for row in range(sz):
        # Add an empty array that will hold each cell
        # in this row
        grid.append([])
        for column in range(sz):
            grid[row].append(0)  # Append a cell

    # Set row 1, cell 5 to one. (Remember rows and
    # column numbers start at zero.)
    obs_locs = grid_world.obstacles
    goals = grid_world.goals
    N_GOAL = len(goals)
    counter = 0
    start_loc = grid_world.init_pos

    grid[start_loc[0]][start_loc[1]] = START
    for goal_loc in goals:
        grid[goal_loc[0]][goal_loc[1]] = GOAL

    for obs in obs_locs:
        grid[obs[0]][obs[1]] = OBS

    visited = []

    # Initialize pygame
    pygame.init()

    # Set the HEIGHT and WIDTH of the screen
    WINDOW_SIZE = [255, 255]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    # Set title of screen
    pygame.display.set_caption("Array Backed Grid")

    # Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                done = True  # Flag that we are done so we exit this loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] // (HEIGHT + MARGIN)
                # Set that location to one
                grid[row][column] = OBS
                visited.append((row, column))
                # print("Click ", pos, "Grid coordinates: ", row, column)
            # if (row, column) in goals:
            #     done = True

        # Set the screen background
        screen.fill(BLACK)

        # Draw the grid
        for row in range(sz):
            for column in range(sz):
                color = state_colors['road']
                if grid[row][column] == OCC:
                    color = state_colors['occ']
                elif grid[row][column] == START:
                    color = state_colors['start']
                elif grid[row][column] == GOAL:
                    color = state_colors['goal']
                elif grid[row][column] == OBS:
                    color = state_colors['obs']
                pygame.draw.rect(
                    screen,
                    color, [(MARGIN + WIDTH) * column + MARGIN,
                            (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()
    grid_world.obstacles = visited
    for state in grid_world.obstacles:
        x, y = state
        grid_world.grid[x][y] = 'O'

    # Save the environment using pickle
    with open(filepath, 'wb') as data_file:
        # json.dump(grid_world.__dict__, foo, ensure_ascii=False)
        pickle.dump(grid_world, data_file)


def readWorld(fp):
    with open(fp, 'rb') as data_file:
        data = pickle.load(data_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Creating a grid-world environment with obstacles')
    parser.add_argument('--n', default=3, type=int, help='Size of grid')
    parser.add_argument('--cr',
                        action='store_true',
                        help='Create a grid-world')
    parser.add_argument('f', type=str, help='File name')
    args = parser.parse_args()

    SZ = args.n
    filename = args.f
    create = False
    if args.cr: create = True

    start = (SZ-1, 0)
    goals = [(0, SZ-1), (SZ-1, SZ-1)]
    obstacles = []
    G = grid.GridWorld(SZ, SZ, start, goals, obstacles)

    env_dir = 'envs'
    if not os.path.exists(env_dir):
        os.makedirs(env_dir)
    env_path = os.path.join(os.getcwd(), env_dir)
    filepath = os.path.join(env_path, filename)

    if create:
        createWorld(G, filepath)

    readWorld(filepath)
