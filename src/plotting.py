import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def gen_plots(agent, fig_dir, env_name):
    # plt.matshow(global_rewards, cmap='viridis'), plt.colorbar()

    n_rows = agent.world.rows
    n_cols = agent.world.cols
    reward = np.array(agent.world.reward)

    G = np.zeros_like(agent.world.grid, dtype=float)
    # This is just to set the color intensity level for the state features
    G[agent.world.init_pos[0]][agent.world.init_pos[1]] = 2
    for goal_pos in agent.world.goals:
        G[goal_pos[0]][goal_pos[1]] = 10
    for state in agent.world.obstacles:
        G[state[0]][state[1]] = -10

    # Store 
    visit_path = []
    for state in agent.states:
        visit_path.append(state)

    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(16, 12))
    fig.suptitle("Policy", fontsize=20)

    h1 = axs[0].imshow(reward, cmap='Blues', extent=[0, n_rows, 0, n_cols])
    axs[0].set_title('Reward', fontsize=20)
    # Major ticks
    axs[0].set_xticks(np.arange(0, n_rows, 1))
    axs[0].set_yticks(np.arange(0, n_cols, 1))
    axs[0].grid(which='major', color='k', linewidth=2)
    fig.colorbar(h1, ax=axs[0], fraction=0.046, pad=0.04)

    h2 = axs[1].matshow(G, cmap='RdBu', extent=[0, n_rows, 0, n_cols])
    axs[1].set_title('Grid World', fontsize=20)
    axs[1].set_xticks(np.arange(0, n_rows, 1))
    axs[1].set_yticks(np.arange(0, n_cols, 1))
    axs[1].grid(which='major', color='k', linewidth=2)
    visit_path = np.array(visit_path, dtype=float)
    x = visit_path[:, 0]
    y = visit_path[:, 1]
    x_ = y
    y_ = n_rows - 1 - x
    x_ += 0.5
    y_ += 0.5
    axs[1].plot(x_, y_, '-g^', linewidth=5, markersize=15, label='policy')
    # fig.colorbar(h2, ax=axs[1])

    # Optional plot: For more explicit indication of the agent states
    # h3 = axs[2].matshow(visited, cmap='Greys', extent=[0, n_rows, 0, n_cols])
    # axs[2].set_title('Trace')
    # axs[2].set_xticks(np.arange(0, n_rows, 1))
    # axs[2].set_yticks(np.arange(0, n_cols, 1))
    # axs[2].grid(which='major', color='k', linewidth=2)
    # fig.colorbar(h3, ax=axs[2])
    plt.legend()
    fig_path = os.path.join(fig_dir, env_name+".png")
    plt.savefig(fig_path)