'''Base agent classes module for the reach-avoid game.

Hanyang Hu, 20240517
'''

import numpy as np


class BaseDynamics:
    """Base class for "drone aviary" Gym environments."""
    
    def __init__(self, number, initials, frequency):
        ''' Initialize the dynamics of the agents.
        Now assume all agents have the same dynamics. 
        If heterogeneous dynamics are needed, please change the states type from ndarray to list.
        Args:
            number (int): the number of agents
            initials (np.ndarray): the initial states of all agents
        '''
        self.numbers = number
        self.initials = initials
        self.state = self.initials
        self.frequency = frequency
        if initials is not None:
            self.dim = self.initials.shape[0] * self.initials.shape[1]
        else:
            self.dim = 0
    
    
    def forward(self, state, action):
        """Update and return the next state of one agent after executing the action.

        Must be implemented in a subclass.

        """
        raise NotImplementedError


    def step(self, action):
        """Update and return the next state of all agents after executing the action.

        Must be implemented in a subclass.

        """
        raise NotImplementedError
    

    def _get_state(self):
        """Return the current states of all agents in the form of xxx.
        
        Returns:
            np.ndarray (shape (num_agents, state_dim)): the current states of all agents

        """
        return self.state
    

    def _dynamics(self):
        """Return the dynamics of the agents.

        Must be implemented in a subclass.

        """
        raise NotImplementedError