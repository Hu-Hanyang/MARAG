import numpy as np
from enum import Enum
from MRAG.dynamics.SingleIntegrator import SingleIntegrator
from MRAG.envs.ReachAvoidGame import RAG1vs1

class Physics:
    """Physics implementations enumeration class."""

    SIG = {'id': 'sig', 'action_dim': 2, 'state_dim': 2}                         # Base single integrator dynamics
    DUB3D = {'id': 'dub3d', 'action_dim': 1, 'state_dim': 3}                     # 3D Dubins car dynamics

# Bound tests
# num_attckers = 2
# size1 = 2
# num_defenders = 1
# num_players = num_attckers + num_defenders

# original_bound = np.array([+1*np.ones(size1) for i in range(num_players)])
# print(f"The shape of the original_bound is {original_bound.shape}. \n")
# print(f"The original_bound is \n{original_bound} \n")

# attacker_bound = np.array([+1*np.ones(size1) for i in range(num_attckers)])
# defender_bound = np.array([+1*np.ones(size1) for i in range(num_defenders)])

# new_bound = np.concatenate((attacker_bound, defender_bound), axis=0)
# print(f"The shape of the new_bound is {new_bound.shape}. \n")
# print(f"The new_bound is \n{new_bound} \n")

# one_attacker_bound = np.array([+1.0, +1.0])
# latest_bound = np.hstack([[one_attacker_bound for i in range(num_players)]])
# print(f"The shape of the latest_bound is {latest_bound.shape}. \n")
# print(f"The latest_bound is \n{latest_bound} \n")

# Physics test
# attacker_physics = Physics.SIG
# print(f"The attacker_physics id is {attacker_physics['id']}. \n")
# print(f"The attacker_physics action_dim is {attacker_physics['action_dim']}. \n")

# # actions test in 2 attackers and 1 defender
# num_attackers = 2
# num_defenders = 3
# num_players = num_attackers + num_defenders 

# action_generated_attacker = np.asarray([(+1., -0.5), (-1., +0.5)]) 
# print(f"The shape of the action_generated_attacker is {action_generated_attacker.shape}. \n")
# action_generated_defender = np.asarray([(+0.5, -0.5), (-0.5, +0.5), (+0.5, +0.5)])
# print(f"The shape of the action_generated_defender is {action_generated_defender.shape}. \n")

# action = np.concatenate((action_generated_attacker, action_generated_defender), axis=0)
# print(f"The shape of the action is {action.shape}. \n")

# action_split_attacker = action[:num_attackers]
# print(f"The shape of the action_split_attacker is {action_split_attacker.shape}. \n")
# action_split_defender = action[-num_defenders:]
# print(f"The shape of the action_split_defender is {action_split_defender.shape}. \n")
# # print(f"The action_split_defender is \n{action_split_defender} \n")
# print(action_split_defender[0].shape)


# # Dynamics test
# number = 2
# initials = np.asarray([[-1, 0.5], [0.3, 0.2]])
# frequncy = 200
# uMin = -1
# uMax = 1
# speed = 1.0

# attackers = SingleIntegrator(number=number, initials=initials, frequncy=frequncy, uMin=uMin, uMax=uMax, speed=speed)
# print(f"The initial states is {attackers.state}. \n")
# # print(f"The shape of the initial states is {attackers.state.shape}. \n")

# action = np.array([[+1.0, -0.5], [-1.0, +0.5]])

# attackers.step(action)
# print(f"The updated states is {attackers.state}. \n")
    
## Attacker Status test
# new_status = np.ones(4)
# print(f"The new_status is {new_status}. \n")
# print(f"The shape of the new_status is {new_status.shape}. \n")
# print(new_status[1])

## Check function test
# def _check_area(state, area):
#         """Check if the state is inside the area.

#         Parameters:
#             state (np.ndarray): the state to check
#             area (dict): the area dictionary to be checked.
        
#         Returns:
#             bool: True if the state is inside the area, False otherwise.
#         """
#         x, y = state  # Unpack the state assuming it's a 2D coordinate

#         for bounds in area.values():
#             x_lower, x_upper, y_lower, y_upper = bounds
#             if x_lower <= x <= x_upper and y_lower <= y <= y_upper:
#                 return True

#         return False
# # Example usage
# state = np.array([0.7, 0.2])
# des = {
#     'goal0': [0.6, 0.8, 0.1, 0.3],
#     'goal1': [1.0, 1.2, 0.5, 0.7],
#     'goal2': [0.2, 0.4, 0.0, 0.2]
# }

# print(_check_area(state, des))  # Should print: True

# state2 = np.array([1.1, 0.6])
# print(_check_area(state2, des))  # Should print: True

# state3 = np.array([0.5, 0.5])
# print(_check_area(state3, des))  # Should print: False

# ## Reward function test
# # In status, 0 stands for free, -1 stands for captured (+10), 1 stands for arrived (-10)
# last_attacker_status = np.array([0, 1, 0, 0])
# current_attacker_status = np.array([1, 1, -1, 1])
# num_attacker = 4
# reward = -1.0

# # for num in range(num_attacker):
# #     reward += (current_attacker_status[num] - last_attacker_status[num]) * -10
# # print(f"The reward is {reward}. \n")
# done = np.all((current_attacker_status == 1) | (current_attacker_status == -1))
# print(f"The done is {done}. \n")

## RAG1VS1 test
# initial_attacker = np.array([[-1, 0.5]])
initial_defender = np.array([[0.3, 0.2]])
print(initial_defender[0].shape)
print(list(initial_defender[0]))
# env = RAG1VS1(initial_attacker=initial_attacker, initial_defender=initial_defender)

# Attacker status test
current_attackers_status = np.array([ 0,  0,  0,  0, -1,  0.])
num_attacker = 6
num_free_attackers = np.count_nonzero(current_attackers_status == 0)
free_attackers_positions = np.where(current_attackers_status == 0)[0]
print(f"The free_attackers_positions is {free_attackers_positions}. \n")
print(f"The position of the attacker 5 in free_attackers_positions is {np.where(free_attackers_positions == 5)[0][0]}. \n")

# number_of_zeros = np.count_nonzero(attackers_status == 0)
# zero_positions = np.where(attackers_status == 0)[0]
# print(f"The shape of the attackers_status is {attackers_status.shape}. \n")
# print(f"The number of zeros is {number_of_zeros}. \n")
# print(f"The zero_positions is {zero_positions}. \n")
# print(zero_positions[0])
# for num in range(num_attacker):
#     if not attackers_status[num]:
#         print(f"The attacker {num} is free.")

