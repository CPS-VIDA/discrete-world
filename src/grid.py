import random
random.seed(0)

class GridWorld:
    '''
        Creates a grid-world environment.
    '''
    def __init__(self, rows: int, cols: int, init_pos: tuple, goals, obstacles, p_slip: float=0.0):
        """
        Defines grid-world with following properties:
            rows: integer
            cols: integer
            init_pos: tuple (x, y)
            goals: list of tuples
            obstacles: list of tuples
            p_slip: slip probability
        """
        self.rows = rows
        self.cols = cols
        self.obstacles = obstacles
        self.p_slip = p_slip
        self.grid = [['_' for i in range(self.cols)] for j in range(self.rows)]
        self.init_pos = init_pos
        self.goals = goals
        self.action_space = ['U', 'R', 'D', 'L']
        self.grid[init_pos[0]][init_pos[1]] = 'S'

        for goal_pos in goals:
            self.grid[goal_pos[0]][goal_pos[1]] = 'G'
        
        for state in obstacles:
            self.grid[state[0]][state[1]] = 'O'

        self.observation_space = []
        for i in range(self.rows):
            for j in range(self.cols):
                self.observation_space.append((i, j))
        
        self.initialize_rewards()
        self.reset()

    def update_obstacles(self, obstacles):
        """ Once you design obstacles, update it back in the grid-world. """
        self.obstacles = obstacles
        for state in obstacles:
            self.grid[state[0]][state[1]] = 'O'
        self.initialize_rewards()
        self.reset()
        
    def initialize_rewards(self):
        """
        Reward function:
            Goals: +1
            Obstacles: -1
            Others: 0
        """
        self.reward = [[0.0 for i in range(self.cols)] for j in range(self.rows)]
        for goal_pos in self.goals:
            self.grid[goal_pos[0]][goal_pos[1]] = 'G'
            self.reward[goal_pos[0]][goal_pos[1]] = 1.0
        
        for state in self.obstacles:
            self.grid[state[0]][state[1]] = 'O'
            self.reward[state[0]][state[1]] = -1.0

    def reset(self):
        self.current_state = self.init_pos

    def nextState(self, state: tuple, action):
        """
        Returns next state as tuple (x, y). 
        At the edges or corners, returns the same state if actions force it to go outside.
        """
        x, y = state
        if action == 'U':
            if x == 0:
                return (x, y)
            neighbor = (x - 1, y)
        elif action == 'R':
            if y == self.cols - 1:
                return (x, y)
            neighbor = (x, y + 1)
        elif action == 'D':
            if x == self.rows - 1:
                return (x, y)
            neighbor = (x + 1, y)
        elif action == 'L':
            if y == 0:
                return (x, y)
            neighbor = (x, y - 1)
        return neighbor

    def getNeighbors(self, state):
        """ Gets list of all neighbors of a state. """
        l = []
        for a in self.actions:
            l.append(self.nextState(state, a))
        return l

    def isObstacle(self, state):
        """ Checks if the state is an obstacle. """
        if state in self.obstacles:
            return True
        return False

    def isGoal(self, state):
        """ Checks if the state is a goal. """
        if state in self.goals:
            return True
        return False

    def __str__(self):
        x, y = self.current_state
        self.grid[x][y] = 'H'
        """ Printing stuff. """
        for i in range(self.rows):
            for j in range(self.cols):
                print("%3s" % self.grid[i][j], end=" ")
            print("\n")
        return ""        

    def choose_action(self, action):
        """ Probabilistic action. 
            With probability 'roll' >= p_slip, returns the same action,
            else uniformly chooses an orthogonal action.
        """
        roll = random.random() # generates a random number [0.0, 1.0)
        idx = self.action_space.index(action)
        n_actions = len(self.action_space) # for the sake of generalization
        other_actions = [self.action_space[(idx-1) % n_actions], self.action_space[(idx+1) % n_actions]] # get orthogonal actions
        if roll >= self.p_slip:
            return action
        else:
            return random.choice(other_actions)


    def step(self, action):
        """ Returns next state, observed reward and done. """
        p_action = self.choose_action(action) # get the stochastic action
        next_state = self.nextState(self.current_state, p_action) # next state
        reward = self.reward[next_state[0]][next_state[1]] # reward observed
        self.current_state = next_state # update current state
        done = self.isGoal(next_state) or self.isObstacle(next_state) # check if goal is reached
        return (next_state, reward, done)

    def render(self):
        """ Printing wrapper. """
        self.__str__()
