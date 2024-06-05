import numpy as np

from MRAG.envs.ReachAvoidGame import ReachAvoidGameEnv
from MRAG.solvers import mip_solver, extend_mip_solver
from MRAG.utilities import *
from MRAG.controllers import hj_contoller_attackers, hj_controller_defenders
from MRAG.plots import animation, plot_scene


#### Game Settings ####
value1vs0, value1vs1, value2vs1, value1vs2, grid1vs0, grid1vs1, grid2vs1, grid1vs2  = hj_preparations_sig()
num_attackers = 2
num_defenders = 1
initial_attacker = np.array([[-0.5, 0.0], [0.0, 0.8]])   # np.array([[-0.8, -0.5], [-0.8, 0.5]])
initial_defender = np.array([[0.3, -0.3]]) #np.array([[0.8, 0.0]])
assert num_attackers == initial_attacker.shape[0], "The number of attackers should be equal to the number of initial attacker states."
assert num_defenders == initial_defender.shape[0], "The number of defenders should be equal to the number of initial defender states."
T = 10.0  # time for the game
ctrl_freq = 200  # control frequency
total_steps = int(T * ctrl_freq)

#### Game Initialization ####
game = ReachAvoidGameEnv(num_attackers=num_attackers, num_defenders=num_defenders, 
                         initial_attacker=initial_attacker, initial_defender=initial_defender, 
                         ctrl_freq=ctrl_freq)

#### Game Loop ####
print(f"================ The game starts now. ================")
for step in range(total_steps):
    EscapedAttacker1vs1, EscapedPairs2vs1, EscapedAttackers1vs2, EscapedTri1vs2 = judges(game.attackers.state, game.defenders.state, game.attackers_status[-1], value1vs1, value2vs1, value1vs2)
    assignments = mip_solver(num_defenders, game.attackers_status[-1],  EscapedAttacker1vs1, EscapedPairs2vs1)
    control_defenders = hj_controller_defenders(game, assignments, value1vs1, value2vs1, grid1vs1, grid2vs1)
    control_attackers = hj_contoller_attackers(game, value1vs0, grid1vs0)
    obs, reward, terminated, truncated, info = game.step(np.vstack((control_attackers, control_defenders)))
    
    if terminated or truncated:
        break
    
print(f"================ The game is over at the {step} step ({step / ctrl_freq} seconds). ================ \n")
current_status_check(game.attackers_status[-1], step)

#### Animation ####
animation(game.attackers_traj, game.defenders_traj, game.attackers_status)
# plot_scene(game.attackers_traj, game.defenders_traj, game.attackers_status, step=40, save=True)
plot_scene(game.attackers_traj, game.defenders_traj, game.attackers_status, step=40)

