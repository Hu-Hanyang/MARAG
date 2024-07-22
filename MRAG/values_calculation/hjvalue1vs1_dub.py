import os
import gc
import time
import math
import psutil
import numpy as np
# Utility functions to initialize the problem
from odp.Grid import Grid
from odp.Shapes import *
# Specify the  file that includes dynamic systems, AttackerDefender4D
from MRAG.envs.DubinCars import DubinCar1vs1
from MRAG.plots_dub import plot_value_1vs1_dub
# Plot options
from odp.Plots import PlotOptions
from odp.Plots.plotting_utilities import plot_isosurface, plot_valuefunction
from odp.solver import HJSolver

""" USER INTERFACES
- 1. Initialize the grids
- 2. Initialize the dynamics
- 3. Instruct the avoid set and reach set
- 4. Set the look-back length and time step
- 5. Call HJSolver function
- 6. Save the value function
"""
##################################################### Remember to check the compGraph 6D ####################################
# Record the time of whole process
start_time = time.time()

# 1. Initialize the grids
grid_size = 28
grids = Grid(np.array([-1.0, -1.0, -math.pi, -1.0, -1.0, -math.pi]), np.array([1.0, 1.0, math.pi, 1.0, 1.0, math.pi]),
             6, np.array([grid_size, grid_size, grid_size, grid_size, grid_size, grid_size]), [2, 5])
process = psutil.Process(os.getpid())
print("1. Gigabytes consumed of the grids initialization {}".format(process.memory_info().rss/1e9))  # in bytes

# 2. Initialize the dynamics
angularv = 1.0
agents_1vs1 = DubinCar1vs1(uMode="min", dMode="max", uMax=angularv, dMax=angularv)  # 1v1 (6 dims dynamics)

# 3. Instruct the avoid set and reach set
## 3.1 Avoid set, no constraint means inf
obs1_a = ShapeRectangle(grids, [-0.1, -1.0, -1000, -1000, -1000, -1000], [0.1, -0.3, 1000, 1000, 1000, 1000])  # a1 get stuck in the obs1
obs1_a = np.array(obs1_a, dtype='float32')

obs2_a = ShapeRectangle(grids, [-0.1, 0.3, -1000, -1000, -1000, -1000], [0.1, 0.6, 1000, 1000, 1000, 1000])  # a1 get stuck in the obs2
obs2_a = np.array(obs2_a, dtype='float32')

obs_a = np.minimum(obs1_a, obs2_a)  # the union of the two obstacles
obs_a = np.array(obs_a, dtype='float32')
del obs1_a
del obs2_a

capture_a = agents_1vs1.capture_set(grids, 0.30, "capture")  # a1 is captured
capture_a = np.array(capture_a, dtype='float32')

avoid_set = np.minimum(capture_a, obs_a)  # the attacker either gets captured or stuck in the obstacles
avoid_set = np.array(avoid_set, dtype='float32')
# del capture_a
# del obs_a
gc.collect()
process = psutil.Process(os.getpid())
print("2. Gigabytes consumed of the avoid_set {}".format(process.memory_info().rss/1e9))  # in bytes

### 3.2 Reach set
goal1_destination = ShapeRectangle(grids, [0.6, 0.1, -1000, -1000, -1000, -1000], [0.8, 0.3, 1000, 1000, 1000, 1000])  # a1 is at goal
goal2_escape = agents_1vs1.capture_set(grids, 0.30, "escape")  # a1 is 0.05 away from defender
a_win = np.maximum(goal1_destination, goal2_escape)
a_win = np.array(a_win, dtype='float32')
del goal1_destination
del goal2_escape

obs1_d = ShapeRectangle(grids, [-1000, -1000, -1000, -0.1, -1.0, -1000], [1000, 1000, 1000, 0.1, -0.3, 1000])  # defender stuck in obs1
obs2_d = ShapeRectangle(grids, [-1000, -1000, -1000, -0.1, 0.3, -1000], [1000, 1000, 1000, 0.1, 0.6, 1000])  # defender stuck in obs2
d_lose = np.minimum(obs1_d, obs2_d)
d_lose = np.array(d_lose, dtype='float32')
del obs2_d
del obs1_d

reach_set = np.minimum(a_win, d_lose) # original
reach_set = np.array(reach_set, dtype='float32')
del a_win
# del d_lose
process = psutil.Process(os.getpid())
print("3. Gigabytes consumed of the reach_set {}".format(process.memory_info().rss/1e9))  # in bytes

# 4. Set the look-back length and time step
lookback_length = 10.0  
t_step = 0.025

# Actual calculation process, needs to add new plot function to draw a 2D figure
small_number = 1e-5
tau = np.arange(start=0, stop=lookback_length + small_number, step=t_step)

# while plotting make sure the len(slicesCut) + len(plotDims) = grid.dims
po = PlotOptions(do_plot=False, plot_type="set", plotDims=[0, 1], slicesCut=[2, 2, 2, 2])

# 5. Call HJSolver function
compMethods = {"TargetSetMode": "minVWithVTarget", "ObstacleSetMode": "maxVWithObstacle"} # original one
# compMethods = {"TargetSetMode": "minVWithVTarget"}
solve_start_time = time.time()


# Before computation test
initial_attacker = np.array([[0.0, 0.0, math.pi/2]])
initial_defender = np.array([[-0.4, 0.4, 0.0]])
target = np.maximum(reach_set, -avoid_set)
plot_value_1vs1_dub(initial_attacker, initial_defender, 0, 0, 1, target, grids)

# accuracy = "medium"
accuracy = "low"
result = HJSolver(agents_1vs1, grids, [reach_set, avoid_set], tau, compMethods, po, saveAllTimeSteps=None, accuracy=accuracy) # original one
process = psutil.Process(os.getpid())
print(f"The CPU memory used during the calculation of the value function is {process.memory_info().rss/1e9: .2f} GB.")  # in bytes

solve_end_time = time.time()
print(f'The shape of the value function is {result.shape} \n')
print(f"The size of the value function is {result.nbytes / 1e9: .2f} GB or {result.nbytes/(1e6)} MB.")
print(f"The time of solving HJ is {solve_end_time - solve_start_time} seconds.")
print(f'The shape of the value function is {result.shape} \n')

# 6. Save the value function
np.save(f'MRAG/values/DubinCar1vs1_grid{grid_size}_{accuracy}_{angularv}angularv.npy', result)


# print(f"The value function has been saved successfully.")

# # Record the time of whole process
# end_time = time.time()
# print(f"The time of whole process is {end_time - start_time} seconds.")
