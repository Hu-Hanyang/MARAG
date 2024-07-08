import numpy as np

from MRAG.envs.DubinCars import DubinCar1vs0
from MRAG.solvers import mip_solver, extend_mip_solver
from MRAG.utilities import *
from MRAG.dub_controllers import hj_contoller_attackers_dub
from MRAG.plots_dub import check_current_value_dub, plot_value_1vs0_dub, animation_dub

#### Game Settings ####
value1vs0_dub, grid1vs0_dub, value1vs1_dub, grid1vs1_dub = hj_preparations_dub()
print(f"The shape of value1vs0_dub is {value1vs0_dub.shape}.")
num_attackers = 1
num_defenders = 0
# TODO np.array([[-0.5, -0.4, -math.pi/2]]) the attacker hits the obstalce; np.array([[-0.5, -0.5, -math.pi/2]]) the attacker hits the boundary
# initial_attacker = np.array([[0.5, 0.0, -math.pi]]) 
initial_attacker = np.array([[-0.5, -0.5, -math.pi/4]])  #  np.array([[-0.5, -0.4, -math.pi/2]])  # np.array([[-0.5, -0.5, -math.pi/2]])
initial_defender = None #  np.array([[-0.8, 0.8, 0.0]])

initial_attacker, initial_defender = dubin_inital_check(initial_attacker, initial_defender)
print(f"The initial attacker states are {initial_attacker}, and the initial defender states are {initial_defender}.")

assert num_attackers == initial_attacker.shape[0], "The number of attackers should be equal to the number of initial attacker states."
# assert num_defenders == initial_defender.shape[0], "The number of defenders should be equal to the number of initial defender states."
T = 12  # time for the game
ctrl_freq = 200  # control frequency
total_steps = int(T * ctrl_freq)
value_threshold = -0.0

#### Game Initialization ####
game = DubinCar1vs0(num_attackers=num_attackers, num_defenders=num_defenders, 
                         initial_attacker=initial_attacker, initial_defender=initial_defender, 
                         ctrl_freq=ctrl_freq, uMode="min", dMode="max", uMax=1.0, dMax=1.0,)

plot_value_1vs0_dub(game.attackers.state, value1vs0_dub, grid1vs0_dub)

# TODO debugging
# print(f"The speed of the DubinCar is {game.attackers.speed}.")
# print(f"The maximum control of the DubinCar is {game.attackers.uMax}.")
# print(f"The obs are {game.obstacles}.")
# print(f"The initial value of the initial states is {check_current_value_dub(game.attackers.state, game.defenders.state, value1vs0_dub[..., 0], grid1vs0_dub)}")
# test_pos = np.array([0.0, 0.5, -math.pi])
# print(f"The test_pos is in the obs:{game._check_area(test_pos, game.obstacles)}")

#### Game Loop ####
value1vs0_counter, value1vs1_counter = 0, 0
controller_usage = []
value_functions_logs = []
value_functions_logs.append(check_current_value_dub(game.attackers.state, game.defenders.state, value1vs0_dub[..., 0], grid1vs0_dub))

print(f"================ The game starts now. ================")
for step in range(total_steps):

    # current_state_slice = po2slice1vs1(game.attackers.state[0], game.defenders.state[0], value1vs1.shape[0])
    # current_value = value1vs1[current_state_slice]
    
    current_value = check_current_value_dub(game.attackers.state, game.defenders.state, value1vs0_dub[..., 0], grid1vs0_dub)
    print(f"Step {step}: the current 1vs0 value function is {current_value}. ")
    
    # if value_functions_logs[-1] != current_value:
    #     value_functions_logs.append(current_value)
    
    # if current_value < value_threshold:  # -0.15 works, -0.10 does not work
    #     control_attackers = hj_contoller_attackers_dub(game, value1vs0_dub, grid1vs0_dub)
    # else:
    #     control_attackers = last_control
    # print(f"=========== Step {step}: the attacker state is {game.attackers.state}. ===========")
    control_attackers = hj_contoller_attackers_dub(game, value1vs0_dub, grid1vs0_dub)
    # print(f"Step {step}: the control of the attacker is {control_attackers}.")
    
    # print(f"The shape of control_attackers is {control_attackers.shape}.")
    # #     value1vs0_counter += 1
    # #     controller_usage.append(0)
    # # else:
    # #     control_attackers = hj_contoller_attackers_test(game, value1vs1_attacker, grid1vs1)
    # #     value1vs1_counter += 1
    # #     controller_usage.append(1)
    # # control_attackers = np.array([[0.0, 0.0]])
    
    # # control_defenders = single_1vs1_controller_defender(game, value1vs1, grid1vs1)
    # control_defenders = np.array([[0.0]])
    
    obs, reward, terminated, truncated, info = game.step(control_attackers)
    # print(f"The current value of the current state is {check_current_value_dub(game.attackers.state, game.defenders.state, value1vs0_dub[..., 0], grid1vs0_dub)}")
    last_control = control_attackers
    
    if terminated or truncated:
        break
    
print(f"================ The game is over at the {step} step ({step / ctrl_freq} seconds). ================ \n")
current_status_check(game.attackers_status[-1], step)

#### Animation ####
animation_dub(game.attackers_traj, game.defenders_traj, game.attackers_status)
# print(f"The value functions is {value_functions_logs}.")
