import numpy as np

from MRAG.envs.DubinCars import DubinCar1vs0, DubinCar1vs1
from MRAG.solvers import mip_solver, extend_mip_solver
from MRAG.utilities import *
from MRAG.dub_controllers import hj_contoller_attackers_dub, hj_contoller_defenders_dub_1vs1
from MRAG.plots_dub import check_current_value_dub, plot_value_1vs1_dub, animation_dub

#### Game Settings ####
grid_size = 100
grid_size_theta = 200
boundary = 2.0
angularv = 0.4
ctrl_freq = 20

start = time.time()
value1vs0_dub_extend = np.load('MRAG/values/DubinCar1vs0_grid100_medium_0.4angularv_20hz_1.0map.npy')
# value1vs1_dub_extend = np.load('MRAG/values/DubinCar1vs1_grid28_medium_0.4angularv_ctrl20hz_1.0map.npy')
value1vs1_dub_extend = np.load('MRAG/values/DubinCar1vs1_grid28_medium_1.0angularv_ctrl20hz_1.0map.npy')
# grid1vs0_dub_extend = Grid(np.array([-boundary, -boundary, -math.pi]), np.array([boundary, boundary, math.pi]), 3, np.array([grid_size, grid_size, grid_size_theta]), [2])
grid1vs0_dub_extend = Grid(np.array([-1.0, -1.0, -math.pi]), np.array([1.0, 1.0, math.pi]), 3, np.array([grid_size, grid_size, grid_size_theta]), [2])
# grid1vs1_dub_extend = Grid(np.array([-boundary, -boundary, -math.pi, -boundary, -boundary, -math.pi]), np.array([boundary, boundary, math.pi, boundary, boundary, math.pi]),
#              6, np.array([28, 28, 28, 28, 28, 28]), [2, 5])
grid1vs1_dub_extend = Grid(np.array([-1.0, -1.0, -math.pi, -1.0, -1.0, -math.pi]), np.array([1.0, 1.0, math.pi, 1.0, 1.0, math.pi]),
             6, np.array([28, 28, 28, 28, 28, 28]), [2, 5])
end = time.time()
print(f"============= HJ value functions loaded Successfully! (Time: {end-start :.4f} seconds) =============")
# value1vs0_dub, grid1vs0_dub, value1vs1_dub, grid1vs1_dub = hj_preparations_dub()
print(f"========== The shape of value1vs0_dub is {value1vs0_dub_extend.shape}. ========== \n")
# value1vs0_dub, grid1vs0_dub, value1vs1_dub, grid1vs1_dub = hj_preparations_dub()
num_attackers = 1
num_defenders = 1
initial_attacker = np.array([[-0.5, -0.5, 1.57]])
initial_defender = np.array([[0.5, 0.5, -1.57]])  
# initial_attacker = np.array([[-0.5000639954463644, -0.5000304876598463, 0.7071731094834994]])
# initial_defender = np.array([[0.5000640550373561, 0.500030621390162, -0.7064660827550182]])  

initial_attacker, initial_defender = dubin_inital_check(initial_attacker, initial_defender)
print(f"The initial attacker states are {initial_attacker}, and the initial defender states are {initial_defender}.")

assert num_attackers == initial_attacker.shape[0], "The number of attackers should be equal to the number of initial attacker states."
assert num_defenders == initial_defender.shape[0], "The number of defenders should be equal to the number of initial defender states."
T = 15.0  # time for the game
ctrl_freq = 20 # control frequency
total_steps = int(T * ctrl_freq)
# threshold_1vs0 = -0.15
# threshold_1vs1 = 0.0
#### Game Initialization ####
game = DubinCar1vs1(num_attackers=num_attackers, num_defenders=num_defenders, 
                         initial_attacker=initial_attacker, initial_defender=initial_defender, 
                         ctrl_freq=ctrl_freq, uMax=angularv, dMax=angularv)

plot_value_1vs1_dub(game.attackers.state, game.defenders.state, 0, 0, 1, value1vs1_dub_extend, grid1vs1_dub_extend)


print(f"The initial value of the initial states is {check_current_value_dub(game.attackers.state, game.defenders.state, value1vs1_dub_extend, grid1vs1_dub_extend)}")
print(f"The control frequency of the dynamics is {game.attackers.frequency} hz. \n")
#### Game Loop ####
value1vs0_counter, value1vs1_counter = 0, 0
controller_usage = []
print(f"================ The game starts now. ================")
for step in range(total_steps):

    current_1vs1_value = check_current_value_dub(game.attackers.state, game.defenders.state, value1vs1_dub_extend, grid1vs1_dub_extend)
    print(f"Step {step}: the current 1vs1 value function is {current_1vs1_value}. ")
    # current_1vs0_value = check_current_value_dub(game.attackers.state, game.defenders.state, value1vs0_dub[..., 0], grid1vs0_dub)
    # print(f"Step {step}: the current 1vs0 value function is {current_1vs0_value}. ")
    
    # # Compute the control for the attacker
    # if current_1vs0_value < threshold_1vs0:
    #     control_attackers = hj_contoller_attackers_dub(game, value1vs0_dub, grid1vs0_dub)
    # else:
    #     control_attackers = last_attacker_control
    
    control_attackers = hj_contoller_attackers_dub(game, value1vs0_dub_extend, grid1vs0_dub_extend)
    # control_attackers = np.array([[0.0]])
    
    
    # # Compute the control for the defender
    # if current_1vs1_value >= threshold_1vs1:
    #     control_defenders = hj_contoller_defenders_dub_1vs1(game, value1vs1_dub, grid1vs1_dub)
    # else:
    #     assert last_defender_control is not None, "In such initial joint state, the defender won't win."
    #     control_defenders = last_defender_control
        
    # control_defenders = hj_contoller_defenders_dub_1vs1(game, value1vs1_dub, grid1vs1_dub)
    control_defenders = hj_contoller_defenders_dub_1vs1(game, value1vs1_dub_extend, grid1vs1_dub_extend)

    # print(f"The control for the defender is {control_defenders}. \n")
    
    
    # #     value1vs0_counter += 1
    # #     controller_usage.append(0)
    # # else:
    # #     control_attackers = hj_contoller_attackers_test(game, value1vs1_attacker, grid1vs1)
    # #     value1vs1_counter += 1
    # #     controller_usage.append(1)
    
    # # control_defenders = single_1vs1_controller_defender(game, value1vs1, grid1vs1)
    # control_defenders = hj_contoller_defenders_dub_1vs1(game, value1vs1_dub, grid1vs1_dub)
    
    # print(f"The relative distance is {np.linalg.norm(game.attackers.state[0][:2] - game.defenders.state[0][:2])}. \n")
    
    obs, reward, terminated, truncated, info = game.step(np.vstack((control_attackers, control_defenders)))

    last_attacker_control = control_attackers
    last_defender_control = control_defenders
    # print(f"Step {step}: the current value function is {check_current_value_dub(game.attackers.state, game.defenders.state, value1vs1_dub, grid1vs1_dub)}. ")
    
    if terminated or truncated:
        break
    
print(f"================ The game is over at the {step} step ({step / ctrl_freq} seconds). ================ \n")
current_status_check(game.attackers_status[-1], step)

#### Animation ####
animation_dub(game.attackers_traj, game.defenders_traj, game.attackers_status)

# print(f"The number of value1vs0_counter is {value1vs0_counter}, and the number of value1vs1_counter is {value1vs1_counter}. \n")
# print(f"The controller usage is {controller_usage}.")

# record_video(game.attackers_traj, game.defenders_traj, game.attackers_status, "1vs1_test.mp4")