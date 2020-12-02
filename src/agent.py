import random

class Agent:
    def __init__(self, world):
        self.world = world

    def gen_policy(self):
        """ Generates a random policy for the agent. """
        self.states = []
        env = self.world
        env.reset()
        s = env.init_pos
        for i in range(5):
            self.states.append(s)
            a = random.choice(env.action_space)
            s_, r, done = env.step(a)
            print(f"State: {s}, Action: {a}, Reward: {r}")
            s = s_

    def __str__(self):
        """ Printing stuff. """
        print(self.world.reward)
        for i in range(self.world.rows):
            for j in range(self.world.cols):
                print("%3s" % self.world.grid[i][j], end=" ")
            print("\n")
        return ""  
    