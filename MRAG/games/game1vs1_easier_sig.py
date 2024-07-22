import numpy as np

from MRAG.envs.AttackerDefender import AttackerDefender1vs1
from MRAG.solvers import mip_solver, extend_mip_solver
from MRAG.utilities import *
from MRAG.sig_controllers import hj_controller_attackers_1vs0, hj_contoller_attackers_1vs1, single_1vs1_controller_defender, single_1vs1_controller_defender_noise
from MRAG.plots import animation, plot_value_1vs1_easier_sig, record_video

#### Game Settings ####
value1vs0, value1vs1, value2vs1, value1vs2, grid1vs0, grid1vs1, grid2vs1, grid1vs2  = hj_preparations_sig()

value1vs1_easier = np.load('/localhome/hha160/projects/safe-control-gym/safe_control_gym/envs/gym_game/values/1vs1Defender_easier.npy')
value1vs1_attacker = np.load('/localhome/hha160/projects/safe-control-gym/safe_control_gym/envs/gym_game/values/1vs1Attacker_easier.npy')
value1vs0_easier = np.load('/localhome/hha160/projects/safe-control-gym/safe_control_gym/envs/gym_game/values/1vs0Attacker_easier.npy')

# print(f"================ The shape of the value1vs1_attacker is {value1vs1_easier.shape}. ================")
num_attackers = 1
num_defenders = 1
initial_attacker = np.array([[0.0, 0.0]])
initial_defender = np.array([[-0.5, -0.5]]) 
assert num_attackers == initial_attacker.shape[0], "The number of attackers should be equal to the number of initial attacker states."
assert num_defenders == initial_defender.shape[0], "The number of defenders should be equal to the number of initial defender states."
T = 10.0  # time for the game
ctrl_freq = 200  # control frequency
total_steps = int(T * ctrl_freq)

#### Game Initialization ####
game = AttackerDefender1vs1(num_attackers=num_attackers, num_defenders=num_defenders, 
                         initial_attacker=initial_attacker, initial_defender=initial_defender, 
                         ctrl_freq=ctrl_freq)

print(f"The initial value of the initial states is {check_current_value(game.attackers.state, game.defenders.state, value1vs1_easier, grid1vs1)}")


plot_value_1vs1_easier_sig(game.attackers.state, game.defenders.state, 
                plot_attacker=0, plot_defender=0, 
                fix_agent=1, value1vs1=value1vs1_easier, grid1vs1=grid1vs1)

print(f"The initial value of the initial states is {check_current_value(game.attackers.state, game.defenders.state, value1vs1, grid1vs1)}")

#### Game Loop ####
value1vs0_counter, value1vs1_counter = 0, 0
controller_usage = []
print(f"================ The game starts now. ================")
for step in range(total_steps):

    # current_state_slice = po2slice1vs1(game.attackers.state[0], game.defenders.state[0], value1vs1_easier.shape[0])
    current_joint_state = np.concatenate((game.attackers.state[0], game.defenders.state[0]))
    current_state_slice = grid1vs1.get_index(current_joint_state)
    current_value = value1vs1_easier[current_state_slice]
    
    
    # if current_value >= 0.0: # the attacker will fail in theory, then use the 1vs0 policy
    #     control_attackers = hj_controller_attackers_1vs0(game, value1vs0_easier, grid1vs0)
    #     value1vs0_counter += 1
    #     controller_usage.append(0)
    # else:
    #     control_attackers = hj_contoller_attackers_1vs1(game, value1vs1_attacker, grid1vs1)
    #     value1vs1_counter += 1
    #     controller_usage.append(1)
    # control_attackers = np.array([[0.0, 0.0]])
    control_attackers = hj_controller_attackers_1vs0(game, value1vs0_easier, grid1vs0)
    
    # 
    control_defenders = single_1vs1_controller_defender(game, value1vs1_easier, grid1vs1)
    # control_defenders = np.array([[0.0, 0.0]])
    
    obs, reward, terminated, truncated, info = game.step(np.vstack((control_attackers, control_defenders)))
    
    if terminated or truncated:
        break
    
print(f"================ The game is over at the {step} step ({step / ctrl_freq} seconds). ================ \n")
current_status_check(game.attackers_status[-1], step)

#### Animation ####
animation(game.attackers_traj, game.defenders_traj, game.attackers_status)
print(f"The number of value1vs0_counter is {value1vs0_counter}, and the number of value1vs1_counter is {value1vs1_counter}. \n")
print(f"The controller usage is {controller_usage}.")

# record_video(game.attackers_traj, game.defenders_traj, game.attackers_status, "1vs1_test.mp4")