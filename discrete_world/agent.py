import numpy as np
np.random.seed(0)


class Agent:
    def __init__(self, world):
        self.world = world
        self.q_table = np.zeros((self.world.rows*self.world.cols, self.world.action_space.n))
        self.policy = [['_' for j in range(self.world.cols)] for i in range(self.world.rows)]

    def gen_policy(self, option=2):
        """ Generates a policy for the agent. """

        # Option 1: Generate a random policy
        # Option 2: Generate a deterministic policy from the Q-Table
        # Option 3: Generates a stochastic policy from Q-Table
        self.states = []
        if option == 1: 
            env = self.world
            env.reset()
            s = env.init_pos
            for i in range(5):
                self.states.append(s)
                a = env.action_space.sample()
                s_, r, done = env.step(a)
                print(f"State: {s}, Action: {a}, Reward: {r}")
                s = s_
        elif option == 2:
            s = self.world.init_pos
            self.states.append(s)
            done = False
            while not done:
                a = self.policy[s[0]][s[1]]
                s_ = self.world.nextState(s, a)
                if s_ in self.states:
                    done = True
                self.states.append(s_)
                s = s_
        elif option == 3:
            print(self.q_table)
            total_reward = []
            goal_reach = 0
            env = self.world
            N_ITERS = 100
            for i in range(N_ITERS):
                ep_reward = 0
                env.reset()
                s = env.init_pos
                states = [s]
                done = False
                while not done:
                    a = self.policy[s[0]][s[1]]
                    s_, r, done = env.step(a)
                    ep_reward += r
                    if s_ in states:
                        done = True
                    else:
                        states.append(s_)
                    s = s_
                if env.isGoal(s):
                    goal_reach += 1
                total_reward.append(ep_reward)
            print("Goal reach percentage: %.3f"%(goal_reach*100/N_ITERS))
            print("Average reward: %.3f"%(sum(total_reward)/N_ITERS))
            self.states = [s]
        print("States: ", self.states)

    def get_action(self, state, eps, min_eps):
        s = self.states_to_num(state)
        if np.random.random() >= max(eps, min_eps):
            return np.argmax(self.q_table[s,:])
        return np.random.randint(len(self.world.action_space))
    
    def get_action_v2(self, state, eps):
        s = self.states_to_num(state)
        return np.argmax(self.q_table[s,:] + np.random.randn(1, len(self.world.action_space))*(1./(eps+1)))
    
    def maxAction(self, state):
        s = self.states_to_num(state)
        return np.max(self.q_table[s,:])

    def learner(self, params):
        """ Q-Learning agent. """
        self.states = []
        env = self.world
        min_eps = params['min_eps']
        gamma = params['gamma']
        n_episodes = params['n_episodes']
        alpha = params['alpha']
        eps = 1
        eps_decay = 0.995
        for i in range(n_episodes):
            env.reset()
            s = env.init_pos
            done = False
            maxSteps = 0
            while not done:
                a = self.get_action(s, eps, min_eps)
                # a = self.get_action_v2(s, i)
                s_, r, done = env.step(self.world.action_space[a])
                s_number = self.states_to_num(s)
                # For Q-Learning
                # self.q_table[s_number,a] += alpha * (r + gamma * self.maxAction(s_) - self.q_table[s_number,a])
                # For SARSA
                nexts_number = self.states_to_num(s_)
                a_next = self.get_action(s_, eps, min_eps)
                self.q_table[s_number,a] += alpha * (r + gamma * self.q_table[nexts_number,a_next] - self.q_table[s_number,a])
                s = s_
                if maxSteps >= (self.world.rows * self.world.cols * 10):
                    done = True
                maxSteps += 1

            if (i % 2000 == 0) or (i == n_episodes-1):
                print("Episode: ", i, eps)

            if (i % 25 == 0):
                eps *= eps_decay
        
        # Get the policy from learned Q-Table
        for i in range(self.world.rows):
            for j in range(self.world.cols):
                s = self.states_to_num((i, j))
                a = np.argmax(self.q_table[s,:])
                self.policy[i][j] = self.world.action_space[a]

    def states_to_num(self, state):
        # print(state)
        x, y = state
        return (self.world.cols*x + y) 

    def __str__(self):
        """ Printing stuff. """
        # print(self.world.reward)
        print("---------- GRID WORLD ----------")
        for i in range(self.world.rows):
            for j in range(self.world.cols):
                print("%3s" % self.world.grid[i][j], end=" ")
            print("\n")
        
        print("---------- POLICY MAP ----------")
        for i in range(self.world.rows):
            for j in range(self.world.cols):
                print("%3s" % self.policy[i][j], end=" ")
            print("\n")
        return ""  
    
