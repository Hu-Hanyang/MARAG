'''Base environment class module for the reach-avoid game with DubinCar dynamics.

'''

import numpy as np
import heterocl as hcl

from MRAG.envs.BaseRLGame import BaseRLGameEnv
from MRAG.envs.BaseGame import Dynamics


class DubinCarGameEnv(BaseRLGameEnv):
    """Multi-agent reach-avoid games class for DubinCar dynamics.

    """
    def __init__(self,
                 num_attackers: int=1,
                 num_defenders: int=1,
                 attackers_dynamics=Dynamics.DUB3D,  
                 defenders_dynamics=Dynamics.DUB3D,
                 initial_attacker: np.ndarray=None,  # shape (num_atackers, state_dim)
                 initial_defender: np.ndarray=None,  # shape (num_defenders, state_dim)
                 ctrl_freq: int = 200,
                 uMode="min", 
                 dMode="max",
                 output_folder='results',
                 game_length_sec=20,
                 map={'map': [-1.0, 1.0, -1.0, 1.0]},  # Hanyang: rectangele [xmin, xmax, ymin, ymax]
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
                            if np.linalg.norm(current_attacker_state[num][:3] - current_defender_state[j][:3]) <= 0.30:
                                new_status[num] = -1
                                break

            return new_status
    

    def _check_area(self, state, area):
        """Check if the state is inside the area.

        Parameters:
            state (np.ndarray): the state to check
            area (dict): the area dictionary to be checked.
        
        Returns:
            bool: True if the state is inside the area, False otherwise.
        """
        x, y, theta = state  # Unpack the state assuming it's a 2D coordinate

        for bounds in area.values():
            x_lower, x_upper, y_lower, y_upper = bounds
            if x_lower <= x <= x_upper and y_lower <= y <= y_upper:
                return True

        return False
    
    
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
    
    
    def optDistb_1vs1(self, spat_deriv):
        """Computes the optimal control (disturbance) for the defender in a 1 vs. 1 game.
        
        Parameters:
            spat_deriv (tuple): spatial derivative in all dimensions
        
        Returns:
            tuple: a tuple of optimal control of the defender (disturbances)
        """
        opt_d = self.defenders.uMax

        if spat_deriv[5] > 0:
            if self.dMode == "min":
                opt_d = - self.defenders.uMax
        else:
            if self.dMode == "max":
                opt_d = - self.defenders.uMax
        
        return opt_d


    def optCtrl_1vs0(self, spat_deriv):
        """Computes the optimal control (disturbance) for the attacker in a 1 vs. 0 game.
        
        Parameters:
            spat_deriv (tuple): spatial derivative in all dimensions
        
        Returns:
            tuple: a tuple of optimal control of the defender (disturbances)
        """
        opt_u = self.attackers.uMax

        if spat_deriv[2] > 0:
            if self.uMode == "min":
                opt_u = - self.attackers.uMax
        else:
            if self.uMode == "max":
                opt_u = - self.attackers.uMax
        
        return opt_u
        


class DubinCar1vs0(DubinCarGameEnv):
    """1 vs. 0 reach-avoid game class with 1 DubinCar3D dynamics."""
    def __init__(self, 
                 num_attackers: int=1,
                 num_defenders: int=0,
                 attackers_dynamics=Dynamics.DUB3D, 
                 defender_dynamics=Dynamics.DUB3D, 
                 initial_attacker=None, 
                 initial_defender=None, 
                 uMax=2.84,
                 dMax=2.84,
                 uMode="min", 
                 dMode="max",
                 ctrl_freq=200): 
        
        if initial_attacker is None:
            initial_attacker = np.zeros((num_attackers, 3))
        if initial_defender is None:
            initial_defender = np.zeros((num_defenders, 3))

        super().__init__(num_attackers=num_attackers,
                         num_defenders=num_defenders,
                         attackers_dynamics=attackers_dynamics, 
                         defenders_dynamics=defender_dynamics, 
                         initial_attacker=initial_attacker, 
                         initial_defender=initial_defender,
                         uMode=uMode, dMode=dMode,
                         ctrl_freq=ctrl_freq)
        
        self.x = np.vstack((initial_attacker, initial_defender))

        self.uMax = uMax
        assert self.uMax == self.attackers.uMax, "The maximum control input for the attacker is not correct."
      

    def dynamics(self, t, state, uOpt, dOpt):
        xA_dot = hcl.scalar(0, "xA_dot")
        yA_dot = hcl.scalar(0, "yA_dot")
        thetaA_dot = hcl.scalar(0, "thetaA_dot")

        xA_dot[0] = self.attackers.speed*hcl.cos(state[2])
        yA_dot[0] = self.attackers.speed*hcl.sin(state[2])
        thetaA_dot[0] = uOpt[0]
       
        return (xA_dot[0], yA_dot[0], thetaA_dot[0])  
    

    def opt_ctrl(self, t, state, spat_deriv):
        """Computes the optimal control for the attacker in a 1 vs. 0 game.
        
        Parameters:
            spat_deriv (tuple): spatial derivative in all dimensions
        
        Returns:
            tuple: a tuple of optimal control of the defender (disturbances)
        """
        opt_u = hcl.scalar(self.uMax, "opt_w")
        # Just create and pass back, even though they're not used
        in2 = hcl.scalar(0, "in2")
        in3 = hcl.scalar(0, "in3")

        with hcl.if_(spat_deriv[2] > 0):
            with hcl.if_(self.uMode == "min"):
                opt_u[0] = - opt_u
        with hcl.elif_(spat_deriv[2] < 0):
            with hcl.if_(self.uMode == "max"):
                opt_u[0] = - opt_u
                
        return (opt_u[0], in2[0], in3[0])


    def opt_dstb(self, t, state, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal disturbances
        """
        opt_d = hcl.scalar(0, "d1")
        # Just create and pass back, even though they're not used
        d2 = hcl.scalar(0, "d2")
        d3 = hcl.scalar(0, "d3")

        return (opt_d, d2[0], d3[0])
    

    def optCtrl_1vs0(self, spat_deriv):
        """Computes the optimal control (disturbance) for the attacker in a 1 vs. 0 game.
        
        Parameters:
            spat_deriv (tuple): spatial derivative in all dimensions
        
        Returns:
            tuple: a tuple of optimal control of the defender (disturbances)
        """
        opt_u = self.attackers.uMax

        if spat_deriv[2] > 0:
            if self.uMode == "min":
                opt_u = - self.attackers.uMax
        else:
            if self.uMode == "max":
                opt_u = - self.attackers.uMax
        
        return opt_u

    
    
class DubinCar1vs1(DubinCarGameEnv):
    """1 vs. 1 reach-avoid game class with 2 DubinCar3D dynamics."""
    def __init__(self, 
                 num_attackers: int=1,
                 num_defenders: int=1,
                 attackers_dynamics=Dynamics.DUB3D, 
                 defender_dynamics=Dynamics.DUB3D, 
                 initial_attacker=None, 
                 initial_defender=None, 
                 uMax=2.84, 
                 dMax=2.84,
                 uMode="min", 
                 dMode="max",
                 ctrl_freq=200): 
        
        if initial_attacker is None:
            initial_attacker = np.zeros((num_attackers, 3))
        if initial_defender is None:
            initial_defender = np.zeros((num_defenders, 3))

        super().__init__(num_attackers=num_attackers,
                         num_defenders=num_defenders,
                         attackers_dynamics=attackers_dynamics, 
                         defenders_dynamics=defender_dynamics, 
                         initial_attacker=initial_attacker, 
                         initial_defender=initial_defender,
                         uMode=uMode, dMode=dMode,
                         ctrl_freq=ctrl_freq)
        
        self.x = np.vstack((initial_attacker, initial_defender))

        self.uMax = uMax
        self.dMax = dMax
        assert self.uMax == self.attackers.uMax, "The maximum control input for the attacker is not correct."
        assert self.dMax == self.defenders.uMax, "The maximum disturbance input for the attacker is not correct."


    def dynamics(self, t, state, uOpt, dOpt):
        xA_dot = hcl.scalar(0, "xA_dot")
        yA_dot = hcl.scalar(0, "yA_dot")
        thetaA_dot = hcl.scalar(0, "thetaA_dot")
        xD_dot = hcl.scalar(0, "xD_dot")
        yD_dot = hcl.scalar(0, "yD_dot")
        thetaD_dot = hcl.scalar(0, "thetaD_dot")

        xA_dot[0] = self.attackers.speed*hcl.cos(state[2])
        yA_dot[0] = self.attackers.speed*hcl.sin(state[2])
        thetaA_dot[0] = uOpt[0]
        xD_dot[0] = self.defenders.speed*hcl.cos(state[5])
        yD_dot[0] = self.defenders.speed*hcl.sin(state[5])
        thetaD_dot[0] = dOpt[0]

        return (xA_dot[0], yA_dot[0], thetaA_dot[0], xD_dot[0], yD_dot[0], thetaD_dot[0])  
    

    def opt_ctrl(self, t, state, spat_deriv):
        """Computes the optimal control for the attacker in a 1 vs. 1 game.
        
        Parameters:
            spat_deriv (tuple): spatial derivative in all dimensions
        
        Returns:
            tuple: a tuple of optimal control of the defender (disturbances)
        """
        opt_u = hcl.scalar(self.uMax, "opt_w")
        # Just create and pass back, even though they're not used
        in2 = hcl.scalar(0, "in2")
        in3 = hcl.scalar(0, "in3")
        in4 = hcl.scalar(0, "in4")

        with hcl.if_(spat_deriv[2] > 0):
            with hcl.if_(self.uMode == "min"):
                opt_u[0] = -opt_u
        with hcl.elif_(spat_deriv[2] < 0):
            with hcl.if_(self.uMode == "max"):
                opt_u[0] = -opt_u
                
        return (opt_u[0], in2[0], in3[0], in4[0])


    def opt_dstb(self, t, state, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal disturbances
        """
        opt_d = hcl.scalar(self.dMax, "opt_d")
        # Just create and pass back, even though they're not used
        d2 = hcl.scalar(0, "d2")
        d3 = hcl.scalar(0, "d3")
        d4 = hcl.scalar(0, "d4")
        
        with hcl.if_(spat_deriv[5] > 0):
            with hcl.if_(self.dMode == "min"):
                opt_d[0] = -opt_d
        with hcl.elif_(spat_deriv[5] < 0):
            with hcl.if_(self.dMode == "max"):
                opt_d[0] = -opt_d

        return (opt_d, d2[0], d3[0], d4[0])
    

    def optDistb_1vs1(self, spat_deriv):
        """Computes the optimal control (disturbance) for the defender in a 1 vs. 1 game.
        
        Parameters:
            spat_deriv (tuple): spatial derivative in all dimensions
        
        Returns:
            tuple: a tuple of optimal control of the defender (disturbances)
        """
        opt_d = self.defenders.uMax

        if spat_deriv[5] > 0:
            if self.dMode == "min":
                opt_d = - self.defenders.uMax
        else:
            if self.dMode == "max":
                opt_d = - self.defenders.uMax
        
        return opt_d
    
    
    def capture_set(self, grid, capture_radius, mode):
        xa, ya, xd, yd = np.meshgrid(grid.grid_points[0], grid.grid_points[1],
                                     grid.grid_points[3], grid.grid_points[4], indexing='ij')
        data = np.power(xa - xd, 2) + np.power(ya - yd, 2)
        if mode == "capture":
            return np.sqrt(data) - capture_radius
        if mode == "escape":
            return capture_radius - np.sqrt(data)
