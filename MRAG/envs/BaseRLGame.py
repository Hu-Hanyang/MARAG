'''Base environment class module for the reach-avoid game.

This module also contains enumerations for cost functions, tasks, disturbances, and quadrotor types.
'''


import os
import numpy as np
import pybullet as p
from gymnasium import spaces
from collections import deque

from MRAG.envs.BaseGame import BaseGameEnv, Dynamics


class BaseRLGameEnv(BaseGameEnv):
    """Base single and multi-agent environment class for reinforcement learning."""
    
    ################################################################################

    def __init__(self,
                 num_attackers: int=1,
                 num_defenders: int=1,
                 attackers_dynamics=Dynamics.SIG,  
                 defenders_dynamics=Dynamics.FSIG,
                 initial_attacker: np.ndarray=None,  # shape (num_atackers, state_dim)
                 initial_defender: np.ndarray=None,  # shape (num_defenders, state_dim)
                 ctrl_freq: int = 200,
                 output_folder='results',
                 ):
        """Initialization of a generic aviary environment.

        Parameters
        ----------
        num_attackers : int, optional
            The number of attackers in the environment.
        num_defenders : int, optional
            The number of defenders in the environment.
        initial_attacker : np.ndarray, optional
            The initial states of the attackers.
        initial_defender : np.ndarray, optional
            The initial states of the defenders.
        attacker_physics : Physics instance
            A dictionary contains the dynamics of the attackers.
        defender_physics : Physics instance
            A dictionary contains the dynamics of the defenders.
        ctrl_freq : int, optional
            The control frequency of the environment.
        output_folder : str, optional
            The folder where to save logs.

        """
           
        super().__init__(num_attackers=num_attackers, num_defenders=num_defenders, 
                         attackers_dynamics=attackers_dynamics, defenders_dynamics=defenders_dynamics, 
                         initial_attacker=initial_attacker, initial_defender=initial_defender, 
                         ctrl_freq=ctrl_freq, output_folder=output_folder
                         )
       

    ################################################################################

   
    def _actionSpace(self):
        """Returns the action space of the environment.
        Formulation: [attackers' action spaces, defenders' action spaces]
        Returns
        -------
        spaces.Box
            A Box of size NUM_PLAYERS x 2, or 1, depending on the action type.

        """
        
        if self.ATTACKER_PHYSICS == Dynamics.SIG or self.ATTACKER_PHYSICS == Dynamics.FSIG:
            attacker_lower_bound = np.array([-1.0, -1.0])
            attacker_upper_bound = np.array([+1.0, +1.0])
        elif self.ATTACKER_PHYSICS == Dynamics.DUB3D:
            attacker_lower_bound = np.array([-1.0])
            attacker_upper_bound = np.array([+1.0])
        else:
            print("[ERROR] in Attacker Action Space, BaseRLGameEnv._actionSpace()")
            exit()
        
        if self.DEFENDER_PHYSICS == Dynamics.SIG or self.DEFENDER_PHYSICS == Dynamics.FSIG:
            defender_lower_bound = np.array([-1.0, -1.0])
            defender_upper_bound = np.array([+1.0, +1.0])
        elif self.DEFENDER_PHYSICS == Dynamics.DUB3D:
            defender_lower_bound = np.array([-1.0])
            defender_upper_bound = np.array([+1.0])
        else:
            print("[ERROR] in Defender Action Space, BaseRLGameEnv._actionSpace()")
            exit()
        
        attackers_lower_bound = np.array([attacker_lower_bound for i in range(self.NUM_ATTACKERS)])
        attackers_upper_bound = np.array([attacker_upper_bound for i in range(self.NUM_ATTACKERS)])
        defenders_lower_bound = np.array([defender_lower_bound for i in range(self.NUM_DEFENDERS)])
        defenders_upper_bound = np.array([defender_upper_bound for i in range(self.NUM_DEFENDERS)])
        
        act_lower_bound = np.concatenate((attackers_lower_bound, defenders_lower_bound), axis=0)
        act_upper_bound = np.concatenate((attackers_upper_bound, defenders_upper_bound), axis=0)

        return spaces.Box(low=act_lower_bound, high=act_upper_bound, dtype=np.float32)
 

    ################################################################################

    def _observationSpace(self):
        """Returns the observation space of the environment.
        Formulation: [attackers' obs spaces, defenders' obs spaces]
        Returns
        -------
        ndarray
            A Box() of shape NUM_PLAYERS x 2, or 3 depending on the observation type.

        """
        
        if self.ATTACKER_PHYSICS == Dynamics.SIG or self.ATTACKER_PHYSICS == Dynamics.FSIG:
            attacker_lower_bound = np.array([-1.0, -1.0])
            attacker_upper_bound = np.array([+1.0, +1.0])
        elif self.ATTACKER_PHYSICS == Dynamics.DUB3D:
            attacker_lower_bound = np.array([-1.0, -1.0, -1.0])
            attacker_upper_bound = np.array([+1.0, +1.0, +1.0])
        else:
            print("[ERROR] Attacker Obs Space in BaseRLGameEnv._observationSpace()")
            exit()
        
        if self.DEFENDER_PHYSICS == Dynamics.SIG or self.DEFENDER_PHYSICS == Dynamics.FSIG:
            defender_lower_bound = np.array([-1.0, -1.0])
            defender_upper_bound = np.array([+1.0, +1.0])
        elif self.DEFENDER_PHYSICS == Dynamics.DUB3D:
            defender_lower_bound = np.array([-1.0, -1.0, -1.0])
            defender_upper_bound = np.array([+1.0, +1.0, +1.0])
        else:
            print("[ERROR] in Defender Obs Space, BaseRLGameEnv._observationSpace()")
            exit()
        
        attackers_lower_bound = np.array([attacker_lower_bound for i in range(self.NUM_ATTACKERS)])
        attackers_upper_bound = np.array([attacker_upper_bound for i in range(self.NUM_ATTACKERS)])
        defenders_lower_bound = np.array([defender_lower_bound for i in range(self.NUM_DEFENDERS)])
        defenders_upper_bound = np.array([defender_upper_bound for i in range(self.NUM_DEFENDERS)])
        
        obs_lower_bound = np.concatenate((attackers_lower_bound, defenders_lower_bound), axis=0)
        obs_upper_bound = np.concatenate((attackers_upper_bound, defenders_upper_bound), axis=0)
        
        return spaces.Box(low=obs_lower_bound, high=obs_upper_bound, dtype=np.float32)
    
    ################################################################################

    def _computeObs(self):
        """Returns the current observation of the environment.

        Returns
        -------
        ndarray
            A Box() of shape (NUM_PLAYERS, dim), concatenate the attackers' and defenders' observations.

        """
        return self.state
