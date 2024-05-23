import numpy as np
import heterocl as hcl

from MRAG.dynamics.BaseDynamics import BaseDynamics

#TODO: Not finished yet, Hanyang, 20240520
""" DubinCar(3D) Dynamics Implementation 
 x_dot = v * cos(theta)
 y_dot = v * sin(theta)
 theta_dot = u
 """

class DubinsCar(BaseDynamics):
    '''3D * num DubinsCar agents dynamics.
    x_dot = v * cos(theta)
    y_dot = v * sin(theta)
    theta_dot = u
    '''
    def __init__(self, physics, number, initials, x=[0, 0, 0, 0, 0, 0], uMin=-1, uMax=1, dMin=-1, 
                 dMax=1, uMode="min", dMode="max", speed_a=1.0, speed_d=1.5):
        self.x = x
        self.uMax = uMax
        self.uMin = uMin
        self.dMax = dMax
        self.dMin = dMin
        assert (uMode in ["min", "max"])
        self.uMode = uMode
        self.dMode = dMode
        self.speed_a = speed_a
        self.speed_d = speed_d     


    def forward(self, state, action, ):
        x_dot = hcl.scalar(0, "x_dot")
        y_dot = hcl.scalar(0, "y_dot")
        theta_dot = hcl.scalar(0, "theta_dot")
        xD_dot = hcl.scalar(0, "xD_dot")
        yD_dot = hcl.scalar(0, "yD_dot")
        thetaD_dot = hcl.scalar(0, "thetaD_dot")

        x_dot[0] = self.speed_a*hcl.cos(state[2])
        y_dot[0] = self.speed_a*hcl.sin(state[2])
        theta_dot[0] = uOpt[0]
        xD_dot[0] = self.speed_d*hcl.cos(state[5])
        yD_dot[0] = self.speed_d*hcl.sin(state[5])
        thetaD_dot[0] = dOpt[0]

        return (x_dot[0], y_dot[0], theta_dot[0], xD_dot[0], yD_dot[0], thetaD_dot[0])  

