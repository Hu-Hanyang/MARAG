'''Base environment class module for the reach-avoid game.

This module also contains enumerations for cost functions, tasks, disturbances, and quadrotor types.
'''

import numpy as np
import gymnasium as gym
from MRAG.utilities import make_agents


class Dynamics:
    """Physics implementations enumeration class."""

    SIG = {'id': 'sig', 'action_dim': 2, 'state_dim': 2, 'speed': 1.0}           # Base single integrator dynamics
    FSIG = {'id': 'fsig', 'action_dim': 2, 'state_dim': 2, 'speed': 1.5}         # Faster single integrator dynamics with feedback
    DUB3D = {'id': 'dub3d', 'action_dim': 1, 'state_dim': 3, 'speed': 1.0}       # 3D Dubins car dynamics
    FDUB3D = {'id': 'fdub3d', 'action_dim': 1, 'state_dim': 3, 'speed': 1.5}     # Faster 3D Dubins car dynamics with feedback
    
    
class BaseGameEnv(gym.Env):
    """Base class for the multi-agent reach-avoid game Gym environments."""
    
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
        #### Constants #############################################
        self.CTRL_FREQ = ctrl_freq
        self.SIM_TIMESTEP = 1. / self.CTRL_FREQ  # 0.005s
        #### Parameters ############################################
        self.NUM_ATTACKERS = num_attackers
        self.NUM_DEFENDERS = num_defenders
        self.NUM_PLAYERS = self.NUM_ATTACKERS + self.NUM_DEFENDERS
        #### Options ###############################################
        self.ATTACKER_PHYSICS = attackers_dynamics
        self.DEFENDER_PHYSICS = defenders_dynamics
        self.OUTPUT_FOLDER = output_folder
        #### Input initial states ####################################
        self.init_attackers = initial_attacker
        self.init_defenders = initial_defender
        #### Create action and observation spaces ##################
        self.action_space = self._actionSpace()
        self.observation_space = self._observationSpace()
        #### Housekeeping ##########################################
        self._housekeeping()
        #### Update and all players' information #####
        self._updateAndLog()
    
    ################################################################################

    def _housekeeping(self):
        """Housekeeping function.

        Initialize all loggers, counters, and variables that need to be reset at the beginning of each episode
        in the `reset()` function.

        """
        #### Set attackers and defenders ##########################
        self.attackers = make_agents(self.ATTACKER_PHYSICS, self.NUM_ATTACKERS, self.init_attackers, self.CTRL_FREQ)
        self.defenders = make_agents(self.DEFENDER_PHYSICS, self.NUM_DEFENDERS, self.init_defenders, self.CTRL_FREQ)
        #### Initialize/reset counters, players' trajectories and attackers status ###
        self.step_counter = 0
        self.attackers_traj = []
        self.defenders_traj = []
        self.attackers_status = []  # 0 stands for free, -1 stands for captured, 1 stands for arrived 
        self.attackers_actions = []
        self.defenders_actions = []

    ################################################################################

    def _updateAndLog(self):
        """Update and log all players' information after inialization, reset(), or step.

        """
        # Update the state
        self.state = np.vstack([self.attackers._get_state().copy(), self.defenders._get_state().copy()])
        # Log the state and trajectory information
        self.attackers_traj.append(self.attackers._get_state().copy())
        self.defenders_traj.append(self.defenders._get_state().copy())
        self.attackers_status.append(self._getAttackersStatus().copy())
    
    ################################################################################

    def reset(self, seed : int = None):
        """Resets the environment.

        Parameters
        ----------
        seed : int, optional
            Random seed.
        options : dict[..], optional
            Additinonal options, unused

        Returns
        -------
        ndarray | dict[..]
            The initial observation, check the specific implementation of `_computeObs()`
            in each subclass for its format.
        dict[..]
            Additional information as a dictionary, check the specific implementation of `_computeInfo()`
            in each subclass for its format.

        """        
        #### Housekeeping ##########################################
        self._housekeeping()
        #### Update and all players' information #####
        self._updateAndLog()
        
        return self.state
    
    ################################################################################

    def step(self,
             action
             ):
        """Advances the environment by one simulation step.

        Parameters
        ----------
        action : ndarray | (num_players, dim_action)
            The input action for all players (in the sequence of attackers + defenders).

        Returns
        -------
        ndarray | dict[..]
            The step's observation, check the specific implementation of `_computeObs()`
            in each subclass for its format.
        float | dict[..]
            The step's reward value(s), check the specific implementation of `_computeReward()`
            in each subclass for its format.
        bool | dict[..]
            Whether the current episode is over, check the specific implementation of `_computeTerminated()`
            in each subclass for its format.
        bool | dict[..]
            Whether the current episode is truncated, check the specific implementation of `_computeTruncated()`
            in each subclass for its format.
        bool | dict[..]
            Whether the current episode is trunacted, always false.
        dict[..]
            Additional information as a dictionary, check the specific implementation of `_computeInfo()`
            in each subclass for its format.

        """
        
        #### Step the simulation using the desired physics update ##
        assert action.shape[0] == self.NUM_PLAYERS, \
            "The action dimension does not match the attackers and defenders."
        
        action = action.copy()
        attackers_action = action[:self.NUM_ATTACKERS]  # ndarray, shape (num_attackers, dim_action)
        defenders_action = action[-self.NUM_DEFENDERS:]  # ndarray, shape (num_defenders, dim_action)
        self.attackers.step(attackers_action)
        self.defenders.step(defenders_action)
        #### Update and all players' information #####
        self._updateAndLog()
        #### Prepare the return values #############################
        obs = self._computeObs()
        reward = self._computeReward()
        terminated = self._computeTerminated()
        truncated = self._computeTruncated()
        info = self._computeInfo()
        
        #### Advance the step counter ##############################
        self.step_counter += 1
        #### Log the actions taken by the attackers and defenders ################
        self.attackers_actions.append(attackers_action)
        self.defenders_actions.append(defenders_action)
        
        return obs, reward, terminated, truncated, info
    
    ################################################################################

    def _getAttackersStatus(self):
        """Returns the current status of all attackers.
        -------
        Must be implemented in a subclass.

        """
        raise NotImplementedError
    
    ################################################################################
    
    def _actionSpace(self):
        """Returns the action space of the environment.

        Must be implemented in a subclass.

        """
        raise NotImplementedError
           
    ################################################################################

    def _observationSpace(self):
        """Returns the observation space of the environment.

        Must be implemented in a subclass.

        """
        raise NotImplementedError
    
    ################################################################################
    
    def _computeObs(self):
        """Returns the current observation of the environment.

        Must be implemented in a subclass.

        """
        raise NotImplementedError
    
    ################################################################################

    def _computeReward(self):
        """Computes the current reward value(s).

        Must be implemented in a subclass.

        Parameters
        ----------
        clipped_action : ndarray | dict[..]
            The input clipped_action for one or more drones.

        """
        raise NotImplementedError

    ################################################################################

    def _computeTerminated(self):
        """Computes the current terminated value(s).

        Must be implemented in a subclass.

        """
        raise NotImplementedError
    
    ################################################################################

    def _computeTruncated(self):
        """Computes the current truncated value(s).

        Must be implemented in a subclass.

        """
        raise NotImplementedError

    ################################################################################

    def _computeInfo(self):
        """Computes the current info dict(s).

        Must be implemented in a subclass.

        """
        raise NotImplementedError

    ################################################################################