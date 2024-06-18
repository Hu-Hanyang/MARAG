import numpy as np

from MRAG.envs.DubinCars import DubinCar1vs0, DubinCar1vs1
from MRAG.solvers import mip_solver, extend_mip_solver
from MRAG.utilities import *
from MRAG.dub_controllers import hj_contoller_attackers_dub, hj_contoller_defenders_dub_1vs1
from MRAG.plots_dub import check_current_value_dub, plot_value_1vs1_dub
from MRAG.plots import animation

#TODO: The 1vs1 value function is wrong, need to recompute it
#### Game Settings ####
value1vs0_dub, grid1vs0_dub, value1vs1_dub, grid1vs1_dub = hj_preparations_dub()

num_attackers = 1
num_defenders = 1
initial_attacker = np.array([[-0.8, 0.0, math.pi/2]])
initial_defender = np.array([[0.3, 0.0, 3*math.pi/2]])

assert num_attackers == initial_attacker.shape[0], "The number of attackers should be equal to the number of initial attacker states."
assert num_defenders == initial_defender.shape[0], "The number of defenders should be equal to the number of initial defender states."
T = 10.0  # time for the game
ctrl_freq = 200  # control frequency
total_steps = int(T * ctrl_freq)

#### Game Initialization ####
game = DubinCar1vs1(num_attackers=num_attackers, num_defenders=num_defenders, 
                         initial_attacker=initial_attacker, initial_defender=initial_defender, 
                         ctrl_freq=ctrl_freq)

plot_value_1vs1_dub(game.attackers.state, game.defenders.state, 0, 0, 1, value1vs1_dub, grid1vs1_dub)


print(f"The initial value of the initial states is {check_current_value_dub(game.attackers.state, game.defenders.state, value1vs1_dub)}")

#### Game Loop ####
value1vs0_counter, value1vs1_counter = 0, 0
controller_usage = []
print(f"================ The game starts now. ================")
for step in range(total_steps):

    # current_state_slice = po2slice1vs1(game.attackers.state[0], game.defenders.state[0], value1vs1.shape[0])
    # current_value = value1vs1[current_state_slice]
    
    
    # # if current_value >= 0.0:
    control_attackers = hj_contoller_attackers_dub(game, value1vs0_dub, grid1vs0_dub)
    # #     value1vs0_counter += 1
    # #     controller_usage.append(0)
    # # else:
    # #     control_attackers = hj_contoller_attackers_test(game, value1vs1_attacker, grid1vs1)
    # #     value1vs1_counter += 1
    # #     controller_usage.append(1)
    # # control_attackers = np.array([[0.0, 0.0]])
    
    # # control_defenders = single_1vs1_controller_defender(game, value1vs1, grid1vs1)
    control_defenders = hj_contoller_defenders_dub_1vs1(game, value1vs1_dub, grid1vs1_dub)
    
    obs, reward, terminated, truncated, info = game.step(np.vstack((control_attackers, control_defenders)))
    
    if terminated or truncated:
        break
    
print(f"================ The game is over at the {step} step ({step / ctrl_freq} seconds). ================ \n")
current_status_check(game.attackers_status[-1], step)

#### Animation ####
animation(game.attackers_traj, game.defenders_traj, game.attackers_status)
# print(f"The number of value1vs0_counter is {value1vs0_counter}, and the number of value1vs1_counter is {value1vs1_counter}. \n")
# print(f"The controller usage is {controller_usage}.")

# record_video(game.attackers_traj, game.defenders_traj, game.attackers_status, "1vs1_test.mp4")