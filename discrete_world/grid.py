import enum
from typing import Set, List, Tuple, Union, Iterable, Optional

import numpy.random as npr
from gym.spaces import Discrete


@enum.unique
class States(enum.IntEnum):
    EMPTY = 0
    START = 1
    GOAL = 2
    OBSTACLE = 3


@enum.unique
class Actions(enum.IntEnum):
    # Actions are ordered this way to enable easy computation of orthogonal
    # directions.
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class GridWorld:

    # Grid Internals
    _rows: int
    _cols: int
    _init_pos: Tuple[int, int]
    _obstacles: Set[Tuple[int, int]]
    _goals: Set[Tuple[int, int]]
    _p_slip: float

    _grid: List[List[States]]

    # Transition Internals
    _reward: List[List[float]]
    _rng: npr.Generator

    # Current state
    _current_pos: Tuple[int, int]

    def __init__(
        self,
        rows: int,
        cols: int,
        init_pos: Tuple[int, int],
        goals: Iterable[Tuple[int, int]],
        obstacles: Iterable[Tuple[int, int]],
        p_slip: float,
        seed: Optional[Union[int, npr.Generator]] = None,
    ):
        """ Represents the grid-world.  """
        self._rows = rows
        self._cols = cols
        self._grid = [
            [States.EMPTY for i in range(self.cols)] for j in range(self.rows)
        ]

        self._init_pos = init_pos
        self._current_pos = init_pos
        self._goals = set(goals)
        self._obstacles = set(obstacles)
        self._p_slip = p_slip

        self._grid[init_pos[0]][init_pos[1]] = States.START

        for goal_pos in goals:
            self._grid[goal_pos[0]][goal_pos[1]] = States.GOAL

        for state in obstacles:
            self._grid[state[0]][state[1]] = States.OBSTACLE

        self._rng = npr.default_rng(seed=seed)

        self._initialize_rewards()
        self.reset()

    @property
    def cols(self) -> int:
        return self._cols

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def size(self) -> Tuple[int, int]:
        return self._rows, self._cols

    @property
    def grid(self) -> List[List[States]]:
        return self._grid

    @property
    def obstacles(self) -> Set[Tuple[int, int]]:
        return self._obstacles

    @property
    def goals(self) -> Set[Tuple[int, int]]:
        return self._goals

    @property
    def reward(self) -> List[List[float]]:
        return self._reward

    @property
    def init_pos(self) -> Tuple[int, int]:
        return self._init_pos

    @property
    def current_state(self) -> Tuple[int, int]:
        return self._current_pos

    @property
    def p_slip(self) -> float:
        return self._p_slip

    @p_slip.setter
    def p_slip(self, p: float):
        if 0 <= p <= 1:
            self._p_slip = p
        else:
            raise ValueError(
                "Slipping probability needs to in [0, 1]. Got {}".format(p)
            )

    def create_obstacles(self, obstacles: Iterable[Tuple[int, int]]):
        """Setup the obstacles by inputting a list of grid positions"""
        self._obstacles = set(obstacles)
        for state in self.obstacles:
            self.grid[state[0]][state[1]] = States.OBSTACLE
        self._initialize_rewards()
        self.reset()

    def _initialize_rewards(self):
        """Initialize the reward function.

        Reward function:
            Goals: +1
            Obstacles: -1
            Others: 0
        """

        def rew_fn(i, j) -> float:
            """Return the reward for a position i,j"""
            if self.grid[i][j] == States.GOAL:
                return 1.0
            elif self.grid[i][j] == States.OBSTACLE:
                return -1.0
            else:
                return 0.0

        # TODO(anand): Is the required? Can we not compute the rewards on the fly?
        self._reward = [
            [rew_fn(i, j) for j in range(self.cols)] for i in range(self.rows)
        ]

        # Sanity check for now
        for goal_pos in self.goals:
            assert (
                self._reward[goal_pos[0]][goal_pos[1]] == 1.0
            ), "Goal at {} does not have a reward of 1.0".format(goal_pos)

        for obstacle_pos in self.obstacles:
            assert (
                self._reward[obstacle_pos[0]][obstacle_pos[1]] == -1.0
            ), "Obstacle at {} does not have a reward of -1.0".format(obstacle_pos)

    def next_state(self, state: Tuple[int, int], action: Actions) -> Tuple[int, int]:
        """
        Returns next state as tuple (x, y).
        At the edges or corners, returns the same state if actions force it to go outside.
        """
        x, y = state
        if action == Actions.UP:
            if x == 0:
                return (x, y)
            neighbor = (x - 1, y)
        elif action == Actions.RIGHT:
            if y == self.cols - 1:
                return (x, y)
            neighbor = (x, y + 1)
        elif action == Actions.DOWN:
            if x == self.rows - 1:
                return (x, y)
            neighbor = (x + 1, y)
        elif action == Actions.LEFT:
            if y == 0:
                return (x, y)
            neighbor = (x, y - 1)
        return neighbor

    def neighbors(self, state: Tuple[int, int]) -> Set[Tuple[int, int]]:
        """ Gets list of all neighbors of a state. """
        l = set()
        for a in Actions:
            l.add(self.next_state(state, a))
        return l

    def choose_action(self, action: Actions) -> Actions:
        """Probabilistic action.
        With probability 'roll' >= p_slip, returns the same action,
        else uniformly chooses an orthogonal action.
        """
        action = Actions(action)  # Temporarily convert it to an `Action`
        idx = int(action)  # Get the integer value of the action

        # NOTE(anand): I don't think we need to generalize here.
        n_actions = len(Actions)

        # Since we are using IntEnum, we can easily convert from int to Actions and vice-versa.
        other_actions = [
            Actions((idx - 1) % n_actions),
            Actions((idx + 1) % n_actions),
        ]  # get orthogonal actions

        roll = self._rng.random()  # generates a random number [0.0, 1.0)
        if roll >= self._p_slip:
            return action
        else:
            return self._rng.choice(other_actions)

    def is_obstacle(self, state: Tuple[int, int]) -> bool:
        """ Checks if the state is an obstacle. """
        if state in self.obstacles:
            return True
        return False

    def is_goal(self, state: Tuple[int, int]) -> bool:
        """ Checks if the state is a goal. """
        if state in self.goals:
            return True
        return False

    def __str__(self):
        def print_fn(i, j) -> str:
            """Return the single char string representation of each state"""
            if self.grid[i][j] == States.GOAL:
                return "G"
            elif self.grid[i][j] == States.OBSTACLE:
                return "O"
            elif self.current_state == (i, j):
                return "C"
            else:
                return " "

        grid_lines = [
            "".join([print_fn(i, j) for j in range(self.cols)])
            for i in range(self.rows)
        ]

        return "\n".join(grid_lines)

    def step(self, action: Actions) -> Tuple[Tuple[int, int], float, bool]:
        """ Returns next state, observed reward and done. """
        action = Actions(action)
        p_action = self.choose_action(action)  # get the stochastic action
        next_state = self.next_state(self.current_state, p_action)  # next state
        reward = self.reward[next_state[0]][next_state[1]]  # reward observed
        self._current_pos = next_state  # update current state
        done = self.is_goal(next_state)  # check if goal is reached
        return (next_state, reward, done)

    def reset(self):
        self._current_pos = self.init_pos

    def render(self, mode="human"):
        return self.__str__()

    def seed(self, seed: Optional[Union[int, npr.Generator]] = None):
        self._rng = npr.default_rng(seed=seed)

    @property
    def action_space(self) -> Discrete:
        return Discrete(4)  # Actions are UP, DOWN, LEFT, RIGHT

    @property
    def observation_space(self) -> Discrete:
        return Discrete(2)  # Observations are the (row, col) position of agent

    # TODO(aniruddh): Make a load from json method.
