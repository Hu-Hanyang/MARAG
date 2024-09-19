'''Environment class module for the multi-agent reach-avoid game.

'''

import numpy as np
import heterocl as hcl

from MRAG.envs.BaseGame import Dynamics
from MRAG.envs.ReachAvoidGame import ReachAvoidGameEnv


class AttackerDefender1vs0(ReachAvoidGameEnv):
    """1 vs. 0 reach-avoid game environment."""

    def __init__(self, 
                 num_attackers: int=1,
                 num_defenders: int=0,
                 attackers_dynamics=Dynamics.SIG, 
                 defender_dynamics=Dynamics.FSIG, 
                 initial_attacker=None, 
                 initial_defender=None, 
                 uMax=1.0,
                 dMax=1.0,
                 uMode="min", 
                 dMode="max",
                 ctrl_freq=200): 
        
        if initial_attacker is None:
            initial_attacker = np.zeros((num_attackers, 2))
        if initial_defender is None and num_defenders > 0:
            initial_defender = np.zeros((num_defenders, 2))

        super().__init__(num_attackers=num_attackers,
                         num_defenders=num_defenders,
                         attackers_dynamics=attackers_dynamics, 
                         defenders_dynamics=defender_dynamics, 
                         initial_attacker=initial_attacker, 
                         initial_defender=initial_defender,
                         uMode=uMode, dMode=dMode,
                         ctrl_freq=ctrl_freq)
        
        if num_defenders == 0:
            self.x = initial_attacker
        else:
            self.x = np.vstack((initial_attacker, initial_defender))

        self.uMax = uMax
        self.dMax = dMax
        assert self.uMax == self.attackers.uMax, "The maximum control input for the attacker is not correct."
        assert self.dMax == self.defenders.uMax, "The maximum disturbance input for the attacker is not correct."
    

    def dynamics(self, t, state, uOpt, dOpt):

        xA1_dot = hcl.scalar(0, "xA1_dot")
        xA2_dot = hcl.scalar(0, "xA2_dot")
    
        xA1_dot[0] = self.attackers.speed * uOpt[0]
        xA2_dot[0] = self.attackers.speed * uOpt[1]

        return xA1_dot[0], xA2_dot[0]


    def opt_ctrl(self, t, state, spat_deriv):
        """
        :param t: time t
        :param state: tuple of coordinates
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: optimal control for the attacker
        """
        opt_a1 = hcl.scalar(0, "opt_a1")
        opt_a2 = hcl.scalar(0, "opt_a2")
        # Just create and pass back, even though they're not used
        in3 = hcl.scalar(0, "in3")
        in4 = hcl.scalar(0, "in4")
        # declare the hcl scalars for relevant spat_derivs
        deriv1 = hcl.scalar(0, "deriv1")
        deriv2 = hcl.scalar(0, "deriv2")
        deriv1[0] = spat_deriv[0]
        deriv2[0] = spat_deriv[1]
        ctrl_len = hcl.sqrt(deriv1[0] * deriv1[0] + deriv2[0] * deriv2[0])        
        if self.uMode == "min":
            with hcl.if_(ctrl_len == 0):
                opt_a1[0] = 0.0
                opt_a2[0] = 0.0
            with hcl.else_():
                opt_a1[0] = -1.0 * deriv1[0] / ctrl_len
                opt_a2[0] = -1.0 * deriv2[0] / ctrl_len
        else:
            with hcl.if_(ctrl_len == 0):
                opt_a1[0] = 0.0
                opt_a2[0] = 0.0
            with hcl.else_():
                opt_a1[0] = deriv1[0] / ctrl_len
                opt_a2[0] = deriv2[0] / ctrl_len
        
        return opt_a1[0], opt_a2[0]


    def opt_dstb(self, t, state, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal disturbances
        """
        d1 = hcl.scalar(0, "d1")
        d2 = hcl.scalar(0, "d2")

        return d1[0], d2[0]


    def optCtrl_1vs0(self, spat_deriv):
        """Computes the optimal control for the attacker in a 1 vs. 0 game.
        
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
    

    def optDistb_1vs0(self, spat_deriv):
        """Computes the optimal disturbance for the attacker in a 1 vs. 0 game.
        
        Parameters:
            spat_deriv (tuple): spatial derivative in all dimensions
        
        Returns:
            tuple: zeros since no defender in this game
        """

        return 0, 0


class AttackerDefender1vs1(ReachAvoidGameEnv):
    """1 vs. 1 reach-avoid game environment."""

    def __init__(self, 
                 num_attackers: int=1,
                 num_defenders: int=1,
                 attackers_dynamics=Dynamics.SIG, 
                 defender_dynamics=Dynamics.FSIG, 
                 initial_attacker=None, 
                 initial_defender=None, 
                 uMax=1.0,
                 dMax=1.0,
                 uMode="min", 
                 dMode="max",
                 ctrl_freq=200): 
        
        if initial_attacker is None:
            initial_attacker = np.zeros((num_attackers, 2))
        if initial_defender is None:
            initial_defender = np.zeros((num_defenders, 2))

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
        xA1_dot = hcl.scalar(0, "xA1_dot")
        xA2_dot = hcl.scalar(0, "xA2_dot")
        xD1_dot = hcl.scalar(0, "xD1_dot")
        xD2_dot = hcl.scalar(0, "xD2_dot")

        xA1_dot[0] = self.attackers.speed * uOpt[0]
        xA2_dot[0] = self.attackers.speed * uOpt[1]
        xD1_dot[0] = self.defenders.speed * dOpt[0]
        xD2_dot[0] = self.defenders.speed * dOpt[1]
    
        return xA1_dot[0], xA2_dot[0], xD1_dot[0], xD2_dot[0]
    

    def opt_ctrl(self, t, state, spat_deriv):
        """
        :param t: time t
        :param state: tuple of coordinates
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return:
        """
        # In 1v1AttackerDefender, a(t) = [a1, a2]^T
        opt_a1 = hcl.scalar(0, "opt_a1")
        opt_a2 = hcl.scalar(0, "opt_a2")
        # Just create and pass back, even though they're not used
        in3 = hcl.scalar(0, "in3")
        in4 = hcl.scalar(0, "in4")
        # declare the hcl scalars for relevant spat_derivs
        deriv1 = hcl.scalar(0, "deriv1")
        deriv2 = hcl.scalar(0, "deriv2")
        deriv1[0] = spat_deriv[0]
        deriv2[0] = spat_deriv[1]
        ctrl_len = hcl.sqrt(deriv1[0] * deriv1[0] + deriv2[0] * deriv2[0])        
        if self.uMode == "min":
            with hcl.if_(ctrl_len == 0):
                opt_a1[0] = 0.0
                opt_a2[0] = 0.0
            with hcl.else_():
                opt_a1[0] = -deriv1[0] / ctrl_len
                opt_a2[0] = -deriv2[0] / ctrl_len
        else:
            with hcl.if_(ctrl_len == 0):
                opt_a1[0] = 0.0
                opt_a2[0] = 0.0
            with hcl.else_():
                opt_a1[0] = deriv1[0] / ctrl_len
                opt_a2[0] = deriv2[0] / ctrl_len
        # return 3, 4 even if you don't use them
        return opt_a1[0], opt_a2[0], in3[0], in4[0]


    def opt_dstb(self, t, state, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal disturbances
        """
        # Graph takes in 4 possible inputs, by default, for now
        d1 = hcl.scalar(0, "d1")
        d2 = hcl.scalar(0, "d2")
        # Just create and pass back, even though they're not used
        d3 = hcl.scalar(0, "d3")
        d4 = hcl.scalar(0, "d4")
        # the same procedure in opt_ctrl
        deriv1 = hcl.scalar(0, "deriv1")
        deriv2 = hcl.scalar(0, "deriv2")
        deriv1[0] = spat_deriv[2]
        deriv2[0] = spat_deriv[3]
        dstb_len = hcl.sqrt(deriv1[0] * deriv1[0] + deriv2[0] * deriv2[0])
        if self.dMode == 'max':
            with hcl.if_(dstb_len == 0):
                d1[0] = 0.0
                d2[0] = 0.0
            with hcl.else_():
                d1[0] = deriv1[0] / dstb_len
                d2[0] = deriv2[0] / dstb_len
        else:
            with hcl.if_(dstb_len == 0):
                d1[0] = 0.0
                d2[0] = 0.0
            with hcl.else_():
                d1[0] = deriv1[0]/ dstb_len
                d2[0] = deriv2[0] / dstb_len

        return d1[0], d2[0], d3[0], d4[0]


    def optCtrl_1vs1(self, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal control of the attacker
        """
        opt_a1 = self.uMax
        opt_a2 = self.uMax
        deriv1 = spat_deriv[0]
        deriv2 = spat_deriv[1]
        ctrl_len = np.sqrt(deriv1*deriv1 + deriv2*deriv2)
        # The initialized control only change sign in the following cases
        if self.uMode == "min":
            if ctrl_len == 0:
                opt_a1 = 0.0
                opt_a2 = 0.0
            else:
                opt_a1 = -deriv1 / ctrl_len
                opt_a2 = -deriv2 / ctrl_len
        else:
            if ctrl_len == 0:
                opt_a1 = 0.0
                opt_a2 = 0.0
            else:
                opt_a1 = deriv1 / ctrl_len
                opt_a2 = deriv2 / ctrl_len
        return (opt_a1, opt_a2)
    

    def optDistb_1vs1(self, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal control of the defender (disturbances)
        """
        opt_d1 = self.dMax
        opt_d2 = self.dMax
        deriv3 = spat_deriv[2]
        deriv4 = spat_deriv[3]
        dstb_len = np.sqrt(deriv3*deriv3 + deriv4*deriv4)
        # The initialized control only change sign in the following cases
        if self.dMode == "max":
            if dstb_len == 0:
                opt_d1 = 0.0
                opt_d2 = 0.0
            else:
                opt_d1 = self.defenders.speed*deriv3 / dstb_len
                opt_d2 = self.defenders.speed*deriv4 / dstb_len
        else:
            if dstb_len == 0:
                opt_d1 = 0.0
                opt_d2 = 0.0
            else:
                opt_d1 = -self.defenders.speed*deriv3 / dstb_len
                opt_d2 = -self.defenders.speed*deriv4 / dstb_len
        return (opt_d1, opt_d2)


    def capture_set(self, grid, capture_radius, mode):
        # using meshgrid
        xa, ya, xd, yd = np.meshgrid(grid.grid_points[0], grid.grid_points[1],
                                     grid.grid_points[2], grid.grid_points[3], indexing='ij')
        data = np.power(xa - xd, 2) + np.power(ya - yd, 2)
        if mode == "capture":
            return np.sqrt(data) - capture_radius
        if mode == "escape":
            return capture_radius - np.sqrt(data)



class AttackerDefender2vs1(ReachAvoidGameEnv):
    """2 vs. 1 reach-avoid game environment."""

    def __init__(self, 
                 num_attackers: int=2,
                 num_defenders: int=1,
                 attackers_dynamics=Dynamics.SIG, 
                 defender_dynamics=Dynamics.FSIG, 
                 initial_attacker=None, 
                 initial_defender=None, 
                 uMax=1.0,
                 dMax=1.0,
                 uMode="min", 
                 dMode="max",
                 ctrl_freq=200): 
        
        if initial_attacker is None:
            initial_attacker = np.zeros((num_attackers, 2))
        if initial_defender is None:
            initial_defender = np.zeros((num_defenders, 2))

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
        xA11_dot = hcl.scalar(0, "xA11_dot")
        xA12_dot = hcl.scalar(0, "xA12_dot")
        xA21_dot = hcl.scalar(0, "xA21_dot")
        xA22_dot = hcl.scalar(0, "xA22_dot")
        xD1_dot = hcl.scalar(0, "xD1_dot")
        xD2_dot = hcl.scalar(0, "xD2_dot")

        xA11_dot[0] = self.attackers.speed * uOpt[0]
        xA12_dot[0] = self.attackers.speed * uOpt[1]
        xA21_dot[0] = self.attackers.speed * uOpt[2] 
        xA22_dot[0] = self.attackers.speed * uOpt[3] 
        xD1_dot[0] = self.defenders.speed * dOpt[0]
        xD2_dot[0] = self.defenders.speed * dOpt[1]


    def opt_ctrl(self, t, state, spat_deriv):
        """
        :param t: time t
        :param state: tuple of coordinates
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return:
        """
        # In 2vs1AttackerDefender, a(t) = [a1, a2, a3, a4]^T
        opt_a1 = hcl.scalar(0, "opt_a1")
        opt_a2 = hcl.scalar(0, "opt_a2")
        opt_a3 = hcl.scalar(0, "opt_a3")
        opt_a4 = hcl.scalar(0, "opt_a4")        

        deriv1 = hcl.scalar(0, "deriv1")
        deriv2 = hcl.scalar(0, "deriv2")
        deriv3 = hcl.scalar(0, "deriv3")
        deriv4= hcl.scalar(0, "deriv4")
        deriv1[0] = spat_deriv[0]
        deriv2[0] = spat_deriv[1]
        deriv3[0] = spat_deriv[2]
        deriv4[0] = spat_deriv[3]
        ctrl_len1 = hcl.sqrt(deriv1[0] * deriv1[0] + deriv2[0] * deriv2[0])     
        ctrl_len2 = hcl.sqrt(deriv3[0] * deriv3[0] + deriv4[0] * deriv4[0])
        if self.uMode == "min":
            with hcl.if_(ctrl_len1 == 0):
                opt_a1[0] = 0.0
                opt_a2[0] = 0.0
            with hcl.else_():
                opt_a1[0] = -deriv1[0] / ctrl_len1
                opt_a2[0] = -deriv2[0] / ctrl_len1
            with hcl.if_(ctrl_len2 == 0):
                opt_a3[0] = 0.0
                opt_a4[0] = 0.0
            with hcl.else_():
                opt_a3[0] = -deriv3[0] / ctrl_len2
                opt_a4[0] = -deriv4[0] / ctrl_len2
        else:
            with hcl.if_(ctrl_len1 == 0):
                opt_a1[0] = 0.0
                opt_a2[0] = 0.0
            with hcl.else_():
                opt_a1[0] = deriv1[0] / ctrl_len1
                opt_a2[0] = deriv2[0] / ctrl_len1
            with hcl.if_(ctrl_len2 == 0):
                opt_a3[0] = 0.0
                opt_a4[0] = 0.0
            with hcl.else_():
                opt_a3[0] = deriv3[0] / ctrl_len2
                opt_a4[0] = deriv4[0] / ctrl_len2

        return opt_a1[0], opt_a2[0], opt_a3[0], opt_a4[0]


    def opt_dstb(self, t, state, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal disturbances
        """
        # Graph takes in 4 possible inputs, by default, for now
        d1 = hcl.scalar(0, "d1")
        d2 = hcl.scalar(0, "d2")
        # Just create and pass back, even though they're not used
        d3 = hcl.scalar(0, "d3")
        d4 = hcl.scalar(0, "d4")
        # the same procedure in opt_ctrl
        deriv1 = hcl.scalar(0, "deriv1")
        deriv2 = hcl.scalar(0, "deriv2")
        deriv1[0] = spat_deriv[4]
        deriv2[0] = spat_deriv[5]
        dstb_len = hcl.sqrt(deriv1[0] * deriv1[0] + deriv2[0] * deriv2[0])
        # with hcl.if_(self.dMode == "max"):
        if self.dMode == 'max':
            with hcl.if_(dstb_len == 0):
                d1[0] = 0.0
                d2[0] = 0.0
            with hcl.else_():
                d1[0] = deriv1[0] / dstb_len
                d2[0] = deriv2[0] / dstb_len
        else:
            with hcl.if_(dstb_len == 0):
                d1[0] = 0.0
                d2[0] = 0.0
            with hcl.else_():
                d1[0] = -deriv1[0]/ dstb_len
                d2[0] = -deriv2[0] / dstb_len

        return d1[0], d2[0], d3[0], d4[0]


    def optCtrl_2vs1(self, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal control of two attackers
        """
        opt_a1 = self.uMax
        opt_a2 = self.uMax
        opt_a3 = self.uMax
        opt_a4 = self.uMax
        deriv1 = spat_deriv[0]
        deriv2 = spat_deriv[1]
        deriv3 = spat_deriv[2]
        deriv4 = spat_deriv[3]
        ctrl_len1 = np.sqrt(deriv1*deriv1 + deriv2*deriv2)
        ctrl_len2 = np.sqrt(deriv3*deriv3 + deriv4*deriv4)
        # The initialized control only change sign in the following cases
        if self.uMode == "min":
            if ctrl_len1 == 0:
                opt_a1 = 0.0
                opt_a2 = 0.0
            else:
                opt_a1 = -deriv1 / ctrl_len1
                opt_a2 = -deriv2 / ctrl_len1
            if ctrl_len2 == 0:
                opt_a3 = 0.0 
                opt_a4 = 0.0
            else:
                opt_a3 = -deriv3 / ctrl_len2
                opt_a4 = -deriv4 / ctrl_len2
        else:
            if ctrl_len1 == 0:
                opt_a1 = 0.0
                opt_a2 = 0.0
            else:
                opt_a1 = deriv1 / ctrl_len1
                opt_a2 = deriv2 / ctrl_len1
            if ctrl_len2 == 0:
                opt_a3 = 0.0 
                opt_a4 = 0.0
            else:
                opt_a3 = deriv3 / ctrl_len2
                opt_a4 = deriv4 / ctrl_len2
        return (opt_a1, opt_a2, opt_a3, opt_a4)
    

    def optDistb_2vs1(self, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal control of the defender (disturbances)
        """
        opt_d1 = self.dMax
        opt_d2 = self.dMax
        deriv5 = spat_deriv[4]
        deriv6 = spat_deriv[5]
        dstb_len = np.sqrt(deriv5*deriv5 + deriv6*deriv6)
        # The initialized control only change sign in the following cases
        if self.dMode == "max":
            if dstb_len == 0:
                opt_d1 = 0.0
                opt_d2 = 0.0
            else:
                opt_d1 = self.defenders.speed*deriv5 / dstb_len
                opt_d2 = self.defenders.speed*deriv6 / dstb_len
        else:
            if dstb_len == 0:
                opt_d1 = 0.0
                opt_d2 = 0.0
            else:
                opt_d1 = -self.defenders.speed*deriv5 / dstb_len
                opt_d2 = -self.defenders.speed*deriv6 / dstb_len
        return (opt_d1, opt_d2)


    def capture_set1(self, grid, capture_radius, mode):
        data = np.power(grid.vs[0] - grid.vs[4], 2) + np.power(grid.vs[1] -grid.vs[5], 2)
        if mode == "capture":
            return np.sqrt(data) - capture_radius
        if mode == "escape":
            return capture_radius - np.sqrt(data)


    def capture_set2(self, grid, capture_radius, mode):
        data = np.power(grid.vs[2] - grid.vs[4], 2) + np.power(grid.vs[3] -grid.vs[5], 2)
        if mode == "capture":
            return np.sqrt(data) - capture_radius
        if mode == "escape":
            return capture_radius - np.sqrt(data)



class AttackerDefender1vs2(ReachAvoidGameEnv):
    """1 vs. 2 reach-avoid game environment."""

    def __init__(self, 
                 num_attackers: int=1,
                 num_defenders: int=2,
                 attackers_dynamics=Dynamics.SIG, 
                 defender_dynamics=Dynamics.FSIG, 
                 initial_attacker=None, 
                 initial_defender=None, 
                 uMax=1.0,
                 dMax=1.0,
                 uMode="max", # "min" or "max"
                 dMode="min", # "max" or "min"
                 ctrl_freq=200): 
        
        if initial_attacker is None:
            initial_attacker = np.zeros((num_attackers, 2))
        if initial_defender is None:
            initial_defender = np.zeros((num_defenders, 2))

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

        xA1_dot = hcl.scalar(0, "xA1_dot")
        xA2_dot = hcl.scalar(0, "xA2_dot")
        xD11_dot = hcl.scalar(0, "xD11_dot")
        xD12_dot = hcl.scalar(0, "xD12_dot")
        xD21_dot = hcl.scalar(0, "xD21_dot")
        xD22_dot = hcl.scalar(0, "xD22_dot")

        xA1_dot[0] = self.attackers.speed * uOpt[0]
        xA2_dot[0] = self.attackers.speed * uOpt[1]
        xD11_dot[0] = self.defenders.speed * dOpt[0] 
        xD12_dot[0] = self.defenders.speed * dOpt[1] 
        xD21_dot[0] = self.defenders.speed * dOpt[2]
        xD22_dot[0] = self.defenders.speed * dOpt[3]

        return xA1_dot[0], xA2_dot[0], xD11_dot[0], xD12_dot[0], xD21_dot[0], xD22_dot[0]


    def opt_ctrl(self, t, state, spat_deriv):
        """
        :param t: time t
        :param state: tuple of coordinates
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return:
        """
        # In 1v2AttackerDefender, a(t) = [a1, a2]^T
        opt_a1 = hcl.scalar(0, "opt_a1")
        opt_a2 = hcl.scalar(0, "opt_a2")      
        # Just create and pass back, even though they're not used
        in3 = hcl.scalar(0, "in3")
        in4 = hcl.scalar(0, "in4")
        # declare the hcl scalars for relevant spat_derivs
        deriv1 = hcl.scalar(0, "deriv1")
        deriv2 = hcl.scalar(0, "deriv2")
        deriv1[0] = spat_deriv[0]
        deriv2[0] = spat_deriv[1]
        ctrl_len1 = hcl.sqrt(deriv1[0] * deriv1[0] + deriv2[0] * deriv2[0])     
        if self.uMode == "min":
            with hcl.if_(ctrl_len1 == 0):
                opt_a1[0] = 0.0
                opt_a2[0] = 0.0
            with hcl.else_():
                opt_a1[0] = -deriv1[0] / ctrl_len1
                opt_a2[0] = -deriv2[0] / ctrl_len1
        else:
            with hcl.if_(ctrl_len1 == 0):
                opt_a1[0] = 0.0
                opt_a2[0] = 0.0
            with hcl.else_():
                opt_a1[0] = deriv1[0] / ctrl_len1
                opt_a2[0] = deriv2[0] / ctrl_len1
        # return 3, 4 even if you don't use them
        return opt_a1[0], opt_a2[0], in3[0], in4[0]


    def opt_dstb(self, t, state, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal disturbances
        """
        # Graph takes in 4 possible inputs, by default, for now
        d1 = hcl.scalar(0, "d1")
        d2 = hcl.scalar(0, "d2")
        d3 = hcl.scalar(0, "d3")
        d4 = hcl.scalar(0, "d4")
        # the same procedure in opt_ctrl
        deriv1 = hcl.scalar(0, "deriv1")
        deriv2 = hcl.scalar(0, "deriv2")
        deriv3 = hcl.scalar(0, "deriv3")
        deriv4 = hcl.scalar(0, "deriv4")
        deriv1[0] = spat_deriv[2]
        deriv2[0] = spat_deriv[3]
        deriv3[0] = spat_deriv[4]
        deriv4[0] = spat_deriv[5]
        dstb_len1 = hcl.sqrt(deriv1[0] * deriv1[0] + deriv2[0] * deriv2[0])
        dstb_len2 = hcl.sqrt(deriv3[0] * deriv3[0] + deriv4[0] * deriv4[0])
        # with hcl.if_(self.dMode == "max"):
        if self.dMode == 'max':
            with hcl.if_(dstb_len1 == 0):
                d1[0] = 0.0
                d2[0] = 0.0
            with hcl.else_():
                d1[0] = deriv1[0] / dstb_len1
                d2[0] = deriv2[0] / dstb_len1
            with hcl.if_(dstb_len2 == 0):
                d3[0] = 0.0
                d4[0] = 0.0
            with hcl.else_():
                d3[0] = deriv3[0] / dstb_len2
                d4[0] = deriv4[0] / dstb_len2
        else:
            with hcl.if_(dstb_len1 == 0):
                d1[0] = 0.0
                d2[0] = 0.0
            with hcl.else_():
                d1[0] = -deriv1[0]/ dstb_len1
                d2[0] = -deriv2[0] / dstb_len1
            with hcl.if_(dstb_len2 == 0):
                d3[0] = 0.0
                d4[0] = 0.0
            with hcl.else_():
                d3[0] = -deriv3[0] / dstb_len2
                d4[0] = -deriv4[0] / dstb_len2

        return d1[0], d2[0], d3[0], d4[0]


    def optCtrl_1vs2(self, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal control of two attackers
        """
        opt_a1 = self.uMax
        opt_a2 = self.uMax
        deriv1 = spat_deriv[0]
        deriv2 = spat_deriv[1]
        ctrl_len = np.sqrt(deriv1*deriv1 + deriv2*deriv2)
        if self.uMode == "min":
            if ctrl_len == 0:
                opt_a1 = 0.0
                opt_a2 = 0.0
            else:
                opt_a1 = -deriv1 / ctrl_len
                opt_a2 = -deriv2 / ctrl_len
        else:
            if ctrl_len == 0:
                opt_a1 = 0.0
                opt_a2 = 0.0
            else:
                opt_a1 = deriv1 / ctrl_len
                opt_a2 = deriv2 / ctrl_len

        return (opt_a1, opt_a2)
    
    
    def optDistb_1vs2(self, spat_deriv):
        """
        :param spat_deriv: tuple of spatial derivative in all dimensions
        :return: a tuple of optimal control of the defender (disturbances)
        """
        opt_d1 = self.dMax
        opt_d2 = self.dMax
        opt_d3 = self.dMax
        opt_d4 = self.dMax
        deriv3 = spat_deriv[2]
        deriv4 = spat_deriv[3]
        deriv5 = spat_deriv[4]
        deriv6 = spat_deriv[5]
        dstb_len1 = np.sqrt(deriv3*deriv3 + deriv4*deriv4)
        dstb_len2 = np.sqrt(deriv5*deriv5 + deriv6*deriv6)
        # The initialized control only change sign in the following cases
        if self.dMode == "max":
            if dstb_len1 == 0:
                opt_d1 = 0.0
                opt_d2 = 0.0
            else:
                opt_d1 = self.defenders.speed*deriv3 / dstb_len1
                opt_d2 = self.defenders.speed*deriv4 / dstb_len1
            if dstb_len2 == 0:
                opt_d3 = 0.0
                opt_d4 = 0.0
            else:
                opt_d3 = self.defenders.speed*deriv5 / dstb_len2
                opt_d4 = self.defenders.speed*deriv6 / dstb_len2
        else:
            if dstb_len1 == 0:
                opt_d1 = 0.0
                opt_d2 = 0.0
            else:
                opt_d1 = -self.defenders.speed*deriv3 / dstb_len1
                opt_d2 = -self.defenders.speed*deriv4 / dstb_len1
            if dstb_len2 == 0:
                opt_d3 = 0.0
                opt_d4 = 0.0
            else:
                opt_d3 = -self.defenders.speed*deriv5 / dstb_len2
                opt_d4 = -self.defenders.speed*deriv6 / dstb_len2

        return (opt_d1, opt_d2, opt_d3, opt_d4)


    def capture_set1(self, grid, capture_radius, mode):
        data = np.power(grid.vs[0] - grid.vs[2], 2) + np.power(grid.vs[1] -grid.vs[3], 2)
        if mode == "capture":
            return np.sqrt(data) - capture_radius
        if mode == "escape":
            return capture_radius - np.sqrt(data)


    def capture_set2(self, grid, capture_radius, mode):
        data = np.power(grid.vs[0] - grid.vs[4], 2) + np.power(grid.vs[1] -grid.vs[5], 2)
        if mode == "capture":
            return np.sqrt(data) - capture_radius
        if mode == "escape":
            return capture_radius - np.sqrt(data)