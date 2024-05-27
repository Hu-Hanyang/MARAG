import numpy as np

from MRAG.envs.ReachAvoidGame import RAG1vs1, RAG2vs1
from MRAG.solvers import mip_solver, extend_mip_solver
from MRAG.utilities import *


#### Game Settings ####
value1vs1, value2vs1, value1vs2 = hj_preparations_sig()
initial_attacker = np.array([[-0.8, -0.5], [-0.8, 0.5]])
initial_defender = np.array([[0.8, 0.0]])
T = 10.0  # time for the game
ctrl_freq = 200  # control frequency
total_steps = int(T * ctrl_freq)
#### Controller ####


env = RAG2vs1(initial_attacker=initial_attacker, initial_defender=initial_defender, ctrl_freq=ctrl_freq)

print(f"Initial Attacker State: {env.attackers.state}")
print(f"Initial Defender State: {env.defenders.state}")
print(f"Initial Attacker Status: {env.attackers_status}")

EscapedAttacker2vs1 = judge_2vs1(env.attackers.state, env.defenders.state, env.attackers_status[-1], value2vs1)
print(f"EscapedAttacker2vs1: {EscapedAttacker2vs1}")



