import numpy as np

from MRAG.envs.ReachAvoidGame import RAG1vs1
from MRAG.solvers import mip_solver, extend_mip_solver
from MRAG.utilities import hj_preparations_sig, judge_1vs1


#### Game Settings ####
value1vs1, value2vs1, value1vs2 = hj_preparations_sig()
initial_attacker = np.array([[-0.4, 0.0]])
initial_defender = np.array([[0.5, 0.0]])
T = 10.0  # time for the game
ctrl_freq = 200  # control frequency
total_steps = int(T * ctrl_freq)
#### Controller ####


env = RAG1vs1(initial_attacker=initial_attacker, initial_defender=initial_defender, ctrl_freq=ctrl_freq)

# print(f"Initial Attacker State: {env.attackers.state}")
# print(f"Initial Defender State: {env.defenders.state}")
# print(f"Initial Attacker Status: {env.attackers_status}")

EscapedAttacker1vs1 = judge_1vs1(env.attackers.state, env.defenders.state, env.attackers_status[-1], value1vs1)
print(f"EscapedAttacker1vs1: {EscapedAttacker1vs1}")



