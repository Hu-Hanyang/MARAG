import matplotlib.pyplot as plt
import numpy as np
from odp.Plots.plotting_utilities import *
from odp.Grid import Grid
from utilities import lo2slice1v1, lo2slice2v1, lo2slice1v0
from utilities import check1v2, check1v1, check2v1

# load reach-avoid value functions
grid_size1v1 = 45
grid_size1v2 = 35
grid_size2v1 = 30

value1v1 = np.load('MRAG/1v1AttackDefend_g45_dspeed1.5.npy')
# value1v1 = np.load('MRAG/1v1AttackDefend_g35_dspeed1.0.npy')
value1v2 = np.load('MRAG/1v2AttackDefend_g35_dspeed1.5.npy')
# value1v2 = np.load('MRAG/1v2AttackDefend_g35_dspeed1.0.npy')
# value1v2 = np.load('MRAG/1v2AttackDefend_g30_dspeed1.5.npy')
value2v1 = np.load('MRAG/2v1AttackDefend_speed15.npy')

# print(f"The shape of the 1v1 value function is {value1v1.shape} \n")
# print(f'The shape of the 1v2 value function is {value1v2.shape} \n')

grid1v1 = Grid(np.array([-1.0, -1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0, 1.0]), 4, 
               np.array([grid_size1v1, grid_size1v1, grid_size1v1, grid_size1v1]))  # original 45
grid1v2 = Grid(np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]), 6, 
               np.array([grid_size1v2, grid_size1v2, grid_size1v2, grid_size1v2, grid_size1v2, grid_size1v2]))  # [30, 30, 30, 30, 30, 30][36, 36, 36, 36, 36, 36]
grid2v1 = Grid(np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]), 6, 
               np.array([grid_size2v1, grid_size2v1, grid_size2v1, grid_size2v1, grid_size2v1, grid_size2v1])) # [36, 36, 36, 36, 36, 36] [30, 30, 30, 30, 30, 30]


# Debugging
# attackers_initials = [(-0.5, 0.5), (0.8, -0.5)]  # [(-0.5, 0.5), (0.8, -0.5)]
# defenders_initials = [(-0.3, 0.0), (0.3, 0.0)]  # , (0.3, -0.5)

attackers_initials = [(-0.5, 0.5), (0.8, -0.5)]  # [(-0.5, 0.5), (0.8, -0.5)]
defenders_initials = [(0.3, 0.5), (0.3, -0.5)]  # , (0.3, -0.5)

a1x = attackers_initials[0][0]
a1y = attackers_initials[0][1]
a2x = attackers_initials[1][0]
a2y = attackers_initials[1][1]
d1x = defenders_initials[0][0]
d1y = defenders_initials[0][1]
d2x = defenders_initials[1][0]
d2y = defenders_initials[1][1]

# A1 in 1vs.1 and 1vs.2 game
A1D1 = (a1x, a1y, d1x, d1y)
A1D2 = (a1x, a1y, d2x, d2y)
A1D1D2 = (a1x, a1y, d1x, d1y, d2x, d2y)

# A2 in 1vs.1 and 1vs.2 game
A2D1 = (a2x, a2y, d1x, d1y)
A2D2 = (a2x, a2y, d2x, d2y)
A2D1D2 = (a2x, a2y, d1x, d1y, d2x, d2y)

# D1 in 2vs.1 game
A1A2D1 = (a1x, a1y, a2x, a2y, d1x, d1y)

# D2 in 2vs.1 game
A1A2D2 = (a1x, a1y, a2x, a2y, d2x, d2y)

# Display the results
# print(f"************ The initial value of 1 vs. 2 value function is {value}. ************ \n")
print(f"************ The initial capture result of (A1, D1) in the 1 vs. 1 game is {check1v1(value1v1, A1D1, grid_size=grid_size1v1)}. ************ \n")
print(f"************ The initial capture result of (A1, D2) in the 1 vs. 1 game is {check1v1(value1v1, A1D2, grid_size=grid_size1v1)}. ************ \n")
print(f"************ The initial capture result of (A2, D1) in the 1 vs. 1 game is {check1v1(value1v1, A2D1, grid_size=grid_size1v1)}. ************ \n")
print(f"************ The initial capture result of (A2, D2) in the 1 vs. 1 game is {check1v1(value1v1, A2D2, grid_size=grid_size1v1)}. ************ \n")
print(f"************ The initial capture result of (A1, D1, D2) in the 1 vs. 2 game is {check1v2(value1v2, A1D1D2, grid_size=grid_size1v2)}. ************ \n")
print(f"************ The initial capture result of (A2, D1, D2) in the 1 vs. 2 game is {check1v2(value1v2, A2D1D2, grid_size=grid_size1v2)}. ************ \n")
print(f"************ The initial capture result of (A1, A2, D1) in the 2 vs. 1 game is {check2v1(value2v1, A1A2D1, grid_size=grid_size2v1)}. ************ \n")
print(f"************ The initial capture result of (A1, A2, D2) in the 2 vs. 1 game is {check2v1(value2v1, A1A2D2, grid_size=grid_size2v1)}. ************ \n")