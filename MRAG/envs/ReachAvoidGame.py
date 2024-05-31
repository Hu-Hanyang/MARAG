'''Base environment class module for the reach-avoid game.

This module also contains enumerations for cost functions, tasks, disturbances, and quadrotor types.
'''

import numpy as np

from MRAG.envs.BaseRLGame import BaseRLGameEnv
from MRAG.envs.BaseGame import Dynamics


class ReachAvoidGameEnv(BaseRLGameEnv):
    """Multi-agent reach-avoid games."""

    ################################################################################
    
    def __init__(self,
                 num_attackers: int=1,
                 num_defenders: int=1,
                 attackers_dynamics=Dynamics.SIG,  
                 defenders_dynamics=Dynamics.FSIG,
                 initial_attacker: np.ndarray=None,  # shape (num_atackers, state_dim)
                 initial_defender: np.ndarray=None,  # shape (num_defenders, state_dim)
                 ctrl_freq: int = 200,
                 uMode="min", 
                 dMode="max",
                 output_folder='results',
                 game_length_sec=20,
                 map={'map': [-1., 1., -1., 1.]},  # Hanyang: rectangele [xmin, xmax, ymin, ymax]
                 des={'goal0': [0.6, 0.8, 0.1, 0.3]},  # Hanyang: rectangele [xmin, xmax, ymin, ymax]
                 obstacles: dict = None,  
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
        uMode : str, optional
            The mode of the attacker, default is "min".
        dMode : str, optional
            The mode of the defender, default is "max".
        output_folder : str, optional
            The folder where to save logs.
        game_length_sec=20 : int, optional
            The maximum length of the game in seconds.
        map : dict, optional
            The map of the environment, default is rectangle.
        des : dict, optional
            The goal in the environment, default is a rectangle.
        obstacles : dict, optional
            The obstacles in the environment, default is rectangle.

        """
           
        super().__init__(num_attackers=num_attackers, num_defenders=num_defenders, 
                         attackers_dynamics=attackers_dynamics, defenders_dynamics=defenders_dynamics, 
                         initial_attacker=initial_attacker, initial_defender=initial_defender, 
                         ctrl_freq=ctrl_freq, output_folder=output_folder
                         )
        
        assert map is not None, "Map must be provided in the game."
        assert des is not None, "Destination must be provided in the game."
        assert initial_attacker is not None, "Initial attacker must be provided in the game."
        assert initial_defender is not None, "Initial defender must be provided in the game."
        
        self.map = map
        self.des = des
        self.obstacles = obstacles
        self.GAME_LENGTH_SEC = game_length_sec
        self.uMode = uMode
        self.dMode = dMode
    ################################################################################
    
    def _getAttackersStatus(self):
        """Returns the current status of all attackers.

        Returns
            ndarray, shape (num_attackers,)

        """
        new_status = np.zeros(self.NUM_ATTACKERS)
        if self.step_counter == 0:  # Befire the first step
            return new_status
        else:       
            last_status = self.attackers_status[-1]
            current_attacker_state = self.attackers._get_state()
            current_defender_state = self.defenders._get_state()

            for num in range(self.NUM_ATTACKERS):
                if last_status[num]:  # attacker has arrived or been captured
                    new_status[num] = last_status[num]
                else: # attacker is free last time
                    # check if the attacker arrive at the des this time
                    if self._check_area(current_attacker_state[num], self.des):
                        new_status[num] = 1
                    # # check if the attacker gets stuck in the obstacles this time (it won't usually)
                    # elif self._check_area(current_attacker_state[num], self.obstacles):
                    #     new_status[num] = -1
                    #     break
                    else:
                        # check if the attacker is captured
                        for j in range(self.NUM_DEFENDERS):
                            if np.linalg.norm(current_attacker_state[num] - current_defender_state[j]) <= 0.1:
                                new_status[num] = -1
                                break

            return new_status
    ################################################################################

    def _check_area(self, state, area):
        """Check if the state is inside the area.

        Parameters:
            state (np.ndarray): the state to check
            area (dict): the area dictionary to be checked.
        
        Returns:
            bool: True if the state is inside the area, False otherwise.
        """
        x, y = state  # Unpack the state assuming it's a 2D coordinate

        for bounds in area.values():
            x_lower, x_upper, y_lower, y_upper = bounds
            if x_lower <= x <= x_upper and y_lower <= y <= y_upper:
                return True

        return False
    ################################################################################
    
    def _computeReward(self):
        """Computes the current reward value.

        One attacker is captured: +10
        One attacker arrived at the goal: -10
        One step and nothing happens: -1
        In status, 0 stands for free, -1 stands for captured, 1 stands for arrived

        Returns
        -------
        float
            The reward.

        """
        last_attacker_status = self.attackers_status[-2]
        current_attacker_status = self.attackers_status[-1]
        reward = -1.0
        for num in range(self.NUM_ATTACKERS):
            reward += (current_attacker_status[num] - last_attacker_status[num]) * -10
            
        return reward

    ################################################################################
    
    def _computeTerminated(self):
        """Computes the current done value.
        done = True if all attackers have arrived or been captured.

        Returns
        -------
        bool
            Whether the current episode is done.

        """
        
        current_attacker_status = self.attackers_status[-1]
        done = np.all((current_attacker_status == 1) | (current_attacker_status == -1))
        
        return done
        
    ################################################################################
    
    def _computeTruncated(self):
        """Computes the current truncated value.

        Returns
        -------
        bool
            Whether the current episode timed out.

        """
        if self.step_counter/self.CTRL_FREQ > self.GAME_LENGTH_SEC:
            return True
        else:
            return False

    ################################################################################
    
    def _computeInfo(self):
        """Computes the current info dict(s).

        Unused.

        Returns
        -------
        dict[str, int]
            Dummy value.

        """
        info = {}
        info['current_steps'] = self.step_counter
        info['current_attackers_status'] = self.attackers_status[-1]
        
        return info 
    
    ################################################################################
    
    def optDistb_2vs1(self, spat_deriv):
        """Computes the optimal control (disturbance) for the defender in a 2 vs. 1 game.
        
        Parameters:
            spat_deriv (tuple): spatial derivative in all dimensions
        
        Returns:
            tuple: a tuple of optimal control of the defender (disturbances)
        """
        opt_d1 = self.defenders.uMax
        opt_d2 = self.defenders.uMax
        deriv5 = spat_deriv[4]
        deriv6 = spat_deriv[5]
        distb_len = np.sqrt(deriv5*deriv5 + deriv6*deriv6)
        if self.dMode == "max":
            if distb_len == 0:
                opt_d1 = 0.0
                opt_d2 = 0.0
            else:
                opt_d1 = self.defenders.speed * deriv5 / distb_len
                opt_d2 = self.defenders.speed * deriv6 / distb_len
        else:
            if distb_len == 0:
                opt_d1 = 0.0
                opt_d2 = 0.0
            else:
                opt_d1 = -self.defenders.speed * deriv5 / distb_len
                opt_d2 = -self.defenders.speed * deriv6 / distb_len
        return (opt_d1, opt_d2)
    
    ################################################################################
    
    def optDistb_1vs1(self, spat_deriv):
        """Computes the optimal control (disturbance) for the defender in a 1 vs. 1 game.
        
        Parameters:
            spat_deriv (tuple): spatial derivative in all dimensions
        
        Returns:
            tuple: a tuple of optimal control of the defender (disturbances)
        """
        opt_d1 = self.defenders.uMax
        opt_d2 = self.defenders.uMax
        deriv3 = spat_deriv[2]
        deriv4 = spat_deriv[3]
        distb_len = np.sqrt(deriv3*deriv3 + deriv4*deriv4)
        if self.dMode == "max":
            if distb_len == 0:
                opt_d1 = 0.0
                opt_d2 = 0.0
            else:
                opt_d1 = self.defenders.speed * deriv3 / distb_len
                opt_d2 = self.defenders.speed * deriv4 / distb_len
        else:
            if distb_len == 0:
                opt_d1 = 0.0
                opt_d2 = 0.0
            else:
                opt_d1 = -self.defenders.speed * deriv3 / distb_len
                opt_d2 = -self.defenders.speed * deriv4 / distb_len
        return (opt_d1, opt_d2)

    ################################################################################

    def optCtrl_1vs0(self, spat_deriv):
        """Computes the optimal control (disturbance) for the attacker in a 1 vs. 0 game.
        
        Parameters:
            spat_deriv (tuple): spatial derivative in all dimensions
        
        Returns:
            tuple: a tuple of optimal control of the defender (disturbances)
        """
        opt_a1 = self.attackers.uMax
        opt_a2 = self.attackers.uMax
        deriv1 = spat_deriv[0]
        deriv2 = spat_deriv[1]
        ctrl_len = np.sqrt(deriv1*deriv1 + deriv2*deriv2)
        if self.uMode == "min":
            if ctrl_len == 0:
                opt_a1 = 0.0
                opt_a2 = 0.0
            else:
                opt_a1 = - self.attackers.speed * deriv1 / ctrl_len
                opt_a2 = - self.attackers.speed * deriv2 / ctrl_len
        else:
            if ctrl_len == 0:
                opt_a1 = 0.0
                opt_a2 = 0.0
            else:
                opt_a1 = self.attackers.speed * deriv1 / ctrl_len
                opt_a2 = self.attackers.speed * deriv2 / ctrl_len
        return (opt_a1, opt_a2)
        
    ################################################################################

        

class RAG1vs1(ReachAvoidGameEnv):
    """1 vs. 1 reach-avoid game environment."""

    def __init__(self, 
                 num_attackers: int=1,
                 num_defenders: int=1,
                 attackers_dynamics=Dynamics.SIG, 
                 defender_dynamics=Dynamics.FSIG, 
                 initial_attacker=None, 
                 initial_defender=None, 
                 ctrl_freq=200): 

        super().__init__(num_attackers=num_attackers,
                         num_defenders=num_defenders,
                         attackers_dynamics=attackers_dynamics, 
                         defenders_dynamics=defender_dynamics, 
                         initial_attacker=initial_attacker, 
                         initial_defender=initial_defender,
                         ctrl_freq=ctrl_freq)


class RAG2vs1(ReachAvoidGameEnv):
    """1 vs. 1 reach-avoid game environment."""

    def __init__(self, 
                 num_attackers: int=2,
                 num_defenders: int=1,
                 attackers_dynamics=Dynamics.SIG, 
                 defender_dynamics=Dynamics.FSIG, 
                 initial_attacker=None, 
                 initial_defender=None, 
                 ctrl_freq=200): 

        super().__init__(num_attackers=num_attackers,
                         num_defenders=num_defenders,
                         attackers_dynamics=attackers_dynamics, 
                         defenders_dynamics=defender_dynamics, 
                         initial_attacker=initial_attacker, 
                         initial_defender=initial_defender,
                         ctrl_freq=ctrl_freq)