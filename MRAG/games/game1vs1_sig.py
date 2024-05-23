import numpy as np

from MRAG.envs.ReachAvoidGame import RAG1vs1


#### Game Settings ####
initial_attacker = np.array([[0.0, 0.0]])
initial_defender = np.array([[0.0, 0.0]])
T = 10.0  # time for the game
ctrl_freq = 200  # control frequency
total_steps = int(T * ctrl_freq)
#### Controller ####


game = RAG1vs1(initial_attacker=initial_attacker, initial_defender=initial_defender, ctrl_freq=ctrl_freq)



