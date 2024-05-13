import numpy as np
import heterocl as hcl

class CartPole4D:
    def __init__(self, x=[0, 0, 0, 0], uMax=10, dMax=5, uMode="min", dMode="max") -> None:
        self.x = x
        self.uMax = uMax
        self.dMax = dMax
        self.uMode = uMode
        self.dMode = dMode
        # Physical parameters
        self.l = 0.5
        self.mc = 1.0
        self.mp = 0.1
        self.g = 9.8
    
    
    def dynamics(self, state, uOpt, dOpt):
        # Reference: https://coneural.org/florian/papers/05_cart_pole.pdf
        # Set of differential equations describing the system
        # x1_dot = x2
        # x2_dot = (uOpt + mp*l*(x4^2*sin(x3) - x4_dot*cost(x2))/(mc + mp) 
        # x3_dot = x4
        # x4_dot = (g*sin(x3) + cos(x3)*(-uOpt - mp*l*x4^2*sin(x3))/(mc + mp))/(l*(4/3 - mp*cos(x3)^2/(mc + mp)))
        x1_dot = hcl.scalar(0, "x1_dot")
        x2_dot = hcl.scalar(0, "x2_dot")
        x3_dot = hcl.scalar(0, "x3_dot")
        x4_dot = hcl.scalar(0, "x4_dot")

        x1_dot[0] = state[1]
        x4_dot[0] = (self.g*hcl.sin(state[2]) + hcl.cos(state[2])*(-uOpt[0] - dOpt[0] - self.mp*self.l*state[3]**2*hcl.sin(state[2])) / (self.mc+ self.mp))/(self.l*(4/3 - self.mp*hcl.cos(state[2])**2/(self.mc + self.mp)))
        x2_dot[0] = (uOpt[0] + dOpt[0] + self.mp*self.l*(state[3]**2*hcl.sin(state[2]) - x4_dot[0]*hcl.cos(state[2])))/(self.mc + self.mp)
        x3_dot[0] = state[3]
        
        return (x1_dot[0], x2_dot[0], x3_dot[0], x4_dot[0])


    def opt_ctrl(self, state, spat_deriv):
        opt_u = hcl.scalar(self.uMax, "opt_u")
        # Just create and pass back, even though they're not used
        in2 = hcl.scalar(0, "in2")
        in3 = hcl.scalar(0, "in3")
        in4 = hcl.scalar(0, "in4")
        u_coefficient = hcl.scalar(0, "u_coefficient")

        u_coefficient = spat_deriv[1]/(self.mc + self.mp) - (spat_deriv[3]*hcl.cos(state[2]))/(self.l*(4/3*(self.mp+self.mc) - self.mp*hcl.cos(state[2])**2))
        with hcl.if_(u_coefficient >= 0):
            with hcl.if_(self.uMode == "min"):
                opt_u[0] = -opt_u[0]
        with hcl.elif_(u_coefficient < 0):
            with hcl.if_(self.uMode == "max"):
                opt_u[0] = -opt_u[0]
        return (opt_u[0], in2[0], in3[0], in4[0])
    

    def opt_dstb(self, state, spat_deriv):
        opt_d = hcl.scalar(self.dMax, "opt_d")
        # Just create and pass back, even though they're not used
        d2 = hcl.scalar(0, "d2")
        d3 = hcl.scalar(0, "d3")
        d4 = hcl.scalar(0, "d4")
        d_coefficient = hcl.scalar(0, "d_coefficient")

        d_coefficient = spat_deriv[1]/(self.mc + self.mp) - (spat_deriv[3]*hcl.cos(state[2]))/(self.l*(4/3*(self.mp+self.mc) - self.mp*hcl.cos(state[2])**2))
        with hcl.if_(d_coefficient >= 0):
            with hcl.if_(self.dMode == "min"):
                opt_d[0] = -opt_d[0]
        with hcl.elif_(d_coefficient < 0):
            with hcl.if_(self.dMode == "max"):
                opt_d[0] = -opt_d[0]
        return (opt_d[0], d2[0], d3[0], d4[0])
    

    def optCtrl_inPython(self, state, spat_deriv):
        opt_a = self.uMax
        u_coefficient = spat_deriv[1]/(self.mc + self.mp) - (spat_deriv[3]*np.cos(state[2]))/(self.l*(4/3*(self.mp+self.mc) - self.mp*np.cos(state[2])**2))

        if u_coefficient >= 0:
            if self.uMode == "min":
                opt_a = -opt_a
        else:
            if self.uMode == "max":
                opt_a = -opt_a

        return opt_a
    

    def optDstb_inPython(self, state, spat_deriv):
        opt_d = self.dMax
        d_coefficient = spat_deriv[1]/(self.mc + self.mp) - (spat_deriv[3]*np.cos(state[2]))/(self.l*(4/3*(self.mp+self.mc) - self.mp*np.cos(state[2])**2))

        if d_coefficient >= 0:
            if self.dMode == "min":
                opt_d = -opt_d
        else:
            if self.dMode == "max":
                opt_d = -opt_d

        return opt_d



