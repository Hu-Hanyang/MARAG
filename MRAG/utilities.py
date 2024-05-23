'''Utility functions for the reach-avoid game.

'''

import numpy as np
from MRAG.dynamics.SingleIntegrator import SingleIntegrator
from MRAG.dynamics.DubinCar3D import DubinsCar

value1vs1 = np.load('MRAG/values/1v1AttackDefend_g45_dspeed1.5.npy')


def make_agents(physics_info, numbers, initials, freqency):
    '''Make the agents with the given physics list, numbers and initials.
    
    Args:
        physics_info (dic): the physics info of the agent
        numbers (int): the number of agents
        initials (np.ndarray): the initial states of all agents
        freqency (int): the frequency of the simulation
    '''
    if physics_info['id'] == 'sig':
        return SingleIntegrator(number=numbers, initials=initials, frequncy=freqency, speed=physics_info['speed'])
    elif physics_info['id'] == 'fsig':
        return SingleIntegrator(number=numbers, initials=initials, frequncy=freqency, speed=physics_info['speed'])
    elif physics_info['id'] == 'dub3d':
        return DubinsCar(number=numbers, initials=initials)
    else:
        raise ValueError("Invalid physics info while generating agents.")


def hj_preparations():
    pass

def judge_1vs1(attackers, defenders, attackers_status, value1vs1):
    pass

def judge_2vs1(attackers, defenders, attackers_status, value2vs1):
    pass

def judge_1vs2(attackers, defenders, attackers_status, value1vs2):
    pass

def judges(attackers, defenders, attackers_status, value1vs1, value2vs1, value1vs2):
    pass





