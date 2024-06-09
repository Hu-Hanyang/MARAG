'''Utility functions for the reach-avoid game.

'''

import math
import time
import numpy as np

from odp.Grid import Grid
from MRAG.dynamics.SingleIntegrator import SingleIntegrator
from MRAG.dynamics.DubinCar3D import DubinsCar


def make_agents(physics_info, numbers, initials, freqency):
    '''Make the agents with the given physics list, numbers and initials.
    
    Args:
        physics_info (dic): the physics info of the agent
        numbers (int): the number of agents
        initials (np.ndarray): the initial states of all agents
        freqency (int): the frequency of the simulation
    '''
    if physics_info['id'] == 'sig':
        return SingleIntegrator(number=numbers, initials=initials, frequency=freqency, speed=physics_info['speed'])
    elif physics_info['id'] == 'fsig':
        return SingleIntegrator(number=numbers, initials=initials, frequency=freqency, speed=physics_info['speed'])
    elif physics_info['id'] == 'dub3d':
        return DubinsCar(number=numbers, initials=initials, frequency=freqency, speed=physics_info['speed'])
    elif physics_info['id'] == 'fdub3d':
        return DubinsCar(number=numbers, initials=initials, frequency=freqency, speed=physics_info['speed'])
    else:
        raise ValueError("Invalid physics info while generating agents.")


def hj_preparations_sig():
    """ Loads all calculated HJ value functions for the single integrator agents.
    This function needs to be called before any game starts.
    
    Returns:
        value1vs0 (np.ndarray): the value function for 1 vs 0 game with all time slices
        value1vs1 (np.ndarray): the value function for 1 vs 1 game
        value2vs1 (np.ndarray): the value function for 2 vs 1 game
        value1vs2 (np.ndarray): the value function for 1 vs 2 game
        grid1vs0 (Grid): the grid for 1 vs 0 game
        grid1vs1 (Grid): the grid for 1 vs 1 game
        grid2vs1 (Grid): the grid for 2 vs 1 game
        grid1vs2 (Grid): the grid for 1 vs 2 game
    """
    start = time.time()
    value1vs0 = np.load('MRAG/values/1vs0AttackDefend_g100_speed1.0.npy')
    value1vs1 = np.load('MRAG/values/1vs1AttackDefend_g45_dspeed1.5.npy')
    value2vs1 = np.load('MRAG/values/2vs1AttackDefend_g30_speed1.5.npy')
    # value1vs2 = np.load('MRAG/values/1vs2AttackDefend_g35_dspeed1.5.npy')
    # value1vs2 = np.load('MRAG/values/1vs2AttackDefend_g35_dspeed1.5_defender.npy')
    value1vs2 = np.load('MRAG/values/1vs2AttackDefend_g35_dspeed1.5_attacker_test1.npy')
    end = time.time()
    print(f"============= HJ value functions loaded Successfully! (Time: {end-start :.4f} seconds) =============")
    grid1vs0 = Grid(np.array([-1.0, -1.0]), np.array([1.0, 1.0]), 2, np.array([100, 100])) 
    grid1vs1 = Grid(np.array([-1.0, -1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0, 1.0]), 4, np.array([45, 45, 45, 45]))
    grid2vs1 = Grid(np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]), 6, np.array([30, 30, 30, 30, 30, 30]))
    grid1vs2 = Grid(np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]), 6, np.array([35, 35, 35, 35, 35, 35]))
    print(f"============= Grids created Successfully! =============")

    return value1vs0, value1vs1, value2vs1, value1vs2, grid1vs0, grid1vs1, grid2vs1, grid1vs2


def po2slice1vs1(attacker, defender, grid_size):
    """ Convert the position of the attacker and defender to the slice of the value function for 1 vs 1 game.

    Args:
        attacker (np.ndarray): the attacker's state
        defender (np.ndarray): the defender's state
        grid_size (int): the size of the grid
    
    Returns:
        joint_slice (tuple): the joint slice of the joint state using the grid size

    """
    joint_state = (attacker[0], attacker[1], defender[0], defender[1])  # (xA1, yA1, xD1, yD1)
    joint_slice = []
    grid_points = np.linspace(-1, +1, num=grid_size)
    for i, s in enumerate(joint_state):
        idx = np.searchsorted(grid_points, s)
        if idx > 0 and (
            idx == len(grid_points)
            or math.fabs(s - grid_points[idx - 1])
            < math.fabs(s - grid_points[idx])
        ):
            joint_slice.append(idx - 1)
        else:
            joint_slice.append(idx)

    return tuple(joint_slice)


def po2slice2vs1(attacker_i, attacker_k, defender, grid_size):
    """ Convert the position of the attackers and defender to the slice of the value function for 2 vs 1 game.

    Args:
        attackers (np.ndarray): the attackers' states
        defender (np.ndarray): the defender's state
        grid_size (int): the size of the grid
    
    Returns:
        joint_slice (tuple): the joint slice of the joint state using the grid size

    """
    joint_state = (attacker_i[0], attacker_i[1], attacker_k[0], attacker_k[1], defender[0], defender[1])  # (xA1, yA1, xA2, yA2, xD1, yD1)
    joint_slice = []
    grid_points = np.linspace(-1, +1, num=grid_size)
    for i, s in enumerate(joint_state):
        idx = np.searchsorted(grid_points, s)
        if idx > 0 and (
            idx == len(grid_points)
            or math.fabs(s - grid_points[idx - 1])
            < math.fabs(s - grid_points[idx])
        ):
            joint_slice.append(idx - 1)
        else:
            joint_slice.append(idx)

    return tuple(joint_slice)


def check_1vs1(attacker, defender, value1vs1):
    """ Check if the attacker could escape from the defender in a 1 vs 1 game.

    Args:
        attacker (np.ndarray): the attacker's state
        defender (np.ndarray): the defender's state
        value1vs1 (np.ndarray): the value function for 1 vs 1 game
    
    Returns:
        bool: False, if the attacker could escape (the attacker will win)
    """
    joint_slice = po2slice1vs1(attacker, defender, value1vs1.shape[0])

    return value1vs1[joint_slice] > 0


def check_2vs1(attacker_i, attacker_k, defender, value2vs1):
    """ Check if the attackers could escape from the defender in a 2 vs 1 game.
    Here escape means that at least one of the attackers could escape from the defender.

    Args:
        attacker_i (np.ndarray): the attacker_i's states
        attacker_j (np.ndarray): the attacker_j's states
        defender (np.ndarray): the defender's state
        value2vs1 (np.ndarray): the value function for 2 vs 1 game
    
    Returns:
        bool: False, if the attackers could escape (the attackers will win)
    """
    joint_slice = po2slice2vs1(attacker_i, attacker_k, defender, value2vs1.shape[0])

    return value2vs1[joint_slice] > 0


def check_1vs2(attacker, defender_j, defender_k, value1vs2, epsilon=0.035):
    """ Check if the attacker could escape from the defenders in a 1 vs 2 game.

    Args:
        attacker (np.ndarray): the attacker's state
        defender_j (np.ndarray): the defender_i's state
        defender_k (np.ndarray): the defender_k's state
        value1vs2 (np.ndarray): the value function for 1 vs 2 game
        epsilon (float): the threshold for the attacker to escape
    
    Returns:
        bool: False, if the attacker could escape (the attacker will win)
    """
    joint_slice = po2slice2vs1(attacker, defender_j, defender_k, value1vs2.shape[0])

    return value1vs2[joint_slice] > epsilon


def judge_1vs1(attackers, defenders, current_attackers_status, value1vs1):
    """ Check the result of the 1 vs 1 game for those free attackers.

    Args:  
        attackers (np.ndarray): the attackers' states
        defenders (np.ndarray): the defenders' states
        attackers_status (np.ndarray): the current moment attackers' status, 0 stands for free, -1 stands for captured, 1 stands for arrived
        value1vs1 (np.ndarray): the value function for 1 vs 1 game
    
    Returns:
        EscapedAttacker1vs1 (a list of lists): the attacker that could escape from the defender in a 1 vs 1 game
    """
    num_attackers, num_defenders = len(attackers), len(defenders)
    EscapedAttacker1vs1 = [[] for _ in range(num_defenders)]

    for j in range(num_defenders):
        for i in range(num_attackers):
            if not current_attackers_status[i]:  # the attcker[i] is free now
                if not check_1vs1(attackers[i], defenders[j], value1vs1):  # the attacker could escape
                    EscapedAttacker1vs1[j].append(i)

    return EscapedAttacker1vs1
    

def judge_2vs1(attackers, defenders, current_attackers_status, value2vs1):
    """ Check the result of the 2 vs 1 game for those free attackers.
    
    Args:
        attackers (np.ndarray): the attackers' states
        defenders (np.ndarray): the defenders' states
        current_attackers_status (np.ndarray): the current moment attackers' status, 0 stands for free, -1 stands for captured, 1 stands for arrived
        value2vs1 (np.ndarray): the value function for 2 vs 1 game
    
    Returns:
        EscapedPairs2vs1 (a list of lists): the pair of attackers that could escape from the defender in a 2 vs 1 game
    """
    num_attackers, num_defenders = len(attackers), len(defenders)
    EscapedPairs2vs1 = [[] for _ in range(num_defenders)]
    for j in range(num_defenders):
        for i in range(num_attackers):
            if not current_attackers_status[i]:  # the attcker[i] is free now
                for k in range(i+1, num_attackers):
                    if not current_attackers_status[k]:
                        if not check_2vs1(attackers[i], attackers[k], defenders[j], value2vs1):
                            EscapedPairs2vs1[j].append([i, k])
    
    return EscapedPairs2vs1


def judge_1vs2(attackers, defenders, current_attackers_status, value1vs2):
    """ Check the result of the 1 vs 2 game for those free attackers.

    Args:
        attackers (np.ndarray): the attackers' states
        defenders (np.ndarray): the defenders' states
        current_attackers_status (np.ndarray): the current moment attackers' status, 0 stands for free, -1 stands for captured, 1 stands for arrived
        value1vs2 (np.ndarray): the value function for 1 vs 2 game

    Returns:
        EscapedAttackers1vs2 (a list of lists): the attacker that could escape from the defenders in a 1 vs 2 game
        EscapedTri1vs2 (a list of lists): the triad of the attacker and defenders that could escape from the defenders in a 1 vs 2 game
    """
    num_attackers, num_defenders = len(attackers), len(defenders)
    EscapedAttackers1vs2 = [[] for _ in range(num_defenders)]
    EscapedTri1vs2 = [[] for _ in range(num_defenders)]  #
    for j in range(num_defenders):
        for k in range(j+1, num_defenders):
            for i in range(num_attackers):
                if not current_attackers_status[i]:
                    if not check_1vs2(attackers[i], defenders[j], defenders[k], value1vs2):
                        EscapedAttackers1vs2[j].append(i)
                        EscapedAttackers1vs2[k].append(i)
                        EscapedTri1vs2[j].append([i, j, k])
                        EscapedTri1vs2[k].append([i, j, k])
                        
    return EscapedAttackers1vs2, EscapedTri1vs2


def judges(attackers, defenders, current_attackers_status, value1vs1, value2vs1, value1vs2):
    """ Check the result of 1 vs. 1, 2 vs. 1 and 1 vs. 2 games for those free attackers.

    Args:
        attackers (np.ndarray): the attackers' states
        defenders (np.ndarray): the defenders' states
        current_attackers_status (np.ndarray): the current moment attackers' status, 0 stands for free, -1 stands for captured, 1 stands for arrived
        value1vs1 (np.ndarray): the value function for 1 vs 1 game
        value2vs1 (np.ndarray): the value function for 2 vs 1 game
        value1vs2 (np.ndarray): the value function for 1 vs 2 game

    Returns:
        EscapedAttacker1vs1 (a list of lists): the attacker that could escape from the defender in a 1 vs 1 game
        EscapedPairs2vs1 (a list of lists): the pair of attackers that could escape from the defender in a 2 vs 1 game
        EscapedAttackers1vs2 (a list of lists): the attacker that could escape from the defenders in a 1 vs 2 game
        EscapedTri1vs2 (a list of lists): the triad of the attacker and defenders that could escape from the defenders in a 1 vs 2 game
    """
    EscapedAttacker1vs1 = judge_1vs1(attackers, defenders, current_attackers_status, value1vs1)
    EscapedPairs2vs1 = judge_2vs1(attackers, defenders, current_attackers_status, value2vs1)
    EscapedAttackers1vs2, EscapedTri1vs2 = judge_1vs2(attackers, defenders, current_attackers_status, value1vs2)
    
    return EscapedAttacker1vs1, EscapedPairs2vs1, EscapedAttackers1vs2, EscapedTri1vs2


def current_status_check(current_attackers_status, step=None):
    """ Check the current status of the attackers.

    Args:
        current_attackers_status (np.ndarray): the current moment attackers' status, 0 stands for free, -1 stands for captured, 1 stands for arrived
        step (int): the current step of the game
    
    Returns:
        status (dic): the current status of the attackers
    """
    num_attackers = len(current_attackers_status)
    num_free, num_arrived, num_captured = 0, 0, 0
    status = {'free': [], 'arrived': [], 'captured': []}
    
    for i in range(num_attackers):
        if current_attackers_status[i] == 0:
            num_free += 1
            status['free'].append(i)
        elif current_attackers_status[i] == 1:
            num_arrived += 1
            status['arrived'].append(i)
        elif current_attackers_status[i] == -1:
            num_captured += 1
            status['captured'].append(i)
        else:
            raise ValueError("Invalid status for the attackers.")
    
    print(f"================= Step {step}: {num_captured}/{num_attackers} attackers are captured \t"
      f"{num_arrived}/{num_attackers} attackers have arrived \t"
      f"{num_free}/{num_attackers} attackers are free =================")

    print(f"================= The current status of the attackers: {status} =================")

    return status