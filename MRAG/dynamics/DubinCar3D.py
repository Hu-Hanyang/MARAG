import numpy as np
import heterocl as hcl

from MRAG.dynamics.BaseDynamics import BaseDynamics


class DubinsCar(BaseDynamics):
    '''3D * num DubinsCar agents dynamics.
    x_dot = v * cos(theta)
    y_dot = v * sin(theta)
    theta_dot = u
    '''
    def __init__(self, number, initials, frequency, uMin=-1.0, uMax=1.0, speed=0.22):  # Hanyang: for real world experiments, change uMax from 2.84 to 1.0
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

        Returns:
            next_state (np.ndarray, shape (3, )): the next state of one agent
        """
        x, y, theta = state
        u = action[0]
        dt = 1.0 / self.frequency
        # dx, dy, dtheta = self._dynamics(state, action)
        # Runge Kutta method
        # Compute the k1 terms
        k1_state = self._dynamics(state, action)
        k1_x, k1_y, k1_theta = k1_state
        k2 = self._dynamics((x+0.5*dt*k1_x, y+0.5*dt*k1_y, theta+0.5*dt*k1_theta), action)
        k2_x, k2_y, k2_theta = k2
        k3 = self._dynamics((x+0.5*dt*k2_x, y+0.5*dt*k2_y, theta+0.5*dt*k2_theta), action)
        k3_x, k3_y, k3_theta = k3
        k4 = self._dynamics((x+dt*k3_x, y+dt*k3_y, theta+dt*k3_theta), action)

        next_state = (x + dt/6*(k1_x + 2*k2_x + 2*k3_x + k4[0]), 
                      y + dt/6*(k1_y + 2*k2_y + 2*k3_y + k4[1]),
                      theta + dt/6*(k1_theta + 2*k2_theta + 2*k3_theta + k4[2]))
        

        # # Forward-Euler method
        # next_x = x + self.speed * np.cos(theta) * dt
        # next_y = y + self.speed * np.sin(theta) * dt
        # next_theta = theta + u * dt
        # next_state = (next_x, next_y, next_theta)

        def check_theta(angle):
            # Make sure the angle is in the range of [-pi, pi)
            while angle >=np.pi:
                angle -= 2 * np.pi
            while angle < -np.pi:
                angle += 2 * np.pi

            return angle

        # Check the boundary
        x_min, x_max, y_min, y_max = -1.0, 1.0, -1.0, 1.0
        x_new = max(min(next_state[0], x_max), x_min)
        y_new = max(min(next_state[1], y_max), y_min)
        theta_new = check_theta(next_state[2])
        # print(f"theta_new is {theta_new}. \n")
        next_state = (x_new, y_new, theta_new)
        
        return next_state


    def step(self, action):
        """Update and return the next state of all agents after executing the action.
        
        Args:
            action (np.ndarray, shape (num, 1)): the actions of all agents

        """
        for i in range(self.numbers):
            self.state[i] = self.forward(self.state[i], action[i])