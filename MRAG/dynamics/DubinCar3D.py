import numpy as np
import heterocl as hcl

from MRAG.dynamics.BaseDynamics import BaseDynamics


class DubinsCar(BaseDynamics):
    #TODO: need to change the parameters based on the hardware, 2024.6.12
    '''3D * num DubinsCar agents dynamics.
    x_dot = v * cos(theta)
    y_dot = v * sin(theta)
    theta_dot = u
    '''
    def __init__(self, number, initials, frequency, uMin=-1, uMax=1, speed=1.0):
        ''' Initialize the dynamics of the agents.
        
        Args:
            number (int): the number of agents
            initials (np.ndarray): the initial states of all agents
        '''
        super().__init__(number=number, initials=initials, frequency=frequency)
        self.uMax = uMax
        self.uMin = uMin
        self.speed = speed
        assert self.dim == number*3, "The dimension of the initial states are not correct for the DubinsCar."
    
    
    def _dynamics(self, state, action):
        """Return the partial derivative equations of one agent.

        Args:
            state (np.ndarray, shape(3, )): the state of one agent
            action (np.ndarray, shape (1, )): the action of one agent
        """
        dx = self.speed * np.cos(state[2])
        dy = self.speed * np.sin(state[2])
        dtheta = action[0]
        return (dx, dy, dtheta)


    def forward(self, state, action):
        """Update and return the next state of one agent with the action based on the Runge Kutta method.
                
        Args:
            state (np.ndarray,  shape(3, )): the state of one agent
            action (np.ndarray, shape (1, )): the action of one agent

        """
        x, y, theta = state
        u = action[0]
        dx, dy, dtheta = self._dynamics(state, action)
        # Compute the k1 terms
        k1 = self._dynamics(state, action)

        # Calculate the k values
        k2 = self._dynamics(state + 0.5 * self.frequency * k1, action)
        k3 = self._dynamics(state + 0.5 * self.frequency * k2, action)
        k4 = self._dynamics(state + self.frequency * k3, action)

        next_state = state + (self.frequency / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        
        return next_state


    def step(self, action):
        """Update and return the next state of all agents after executing the action.
        
        Args:
            action (np.ndarray, shape (num, 1)): the actions of all agents

        """
        for i in range(self.numbers):
            self.state[i] = self.forward(self.state[i], action[i])