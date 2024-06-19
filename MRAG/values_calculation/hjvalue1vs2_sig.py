import os
import gc
import time
import psutil
import numpy as np

from odp.Grid import Grid
from odp.Shapes import *
from MRAG.envs.AttackerDefender import AttackerDefender1vs2
from odp.Plots import PlotOptions
from odp.Plots.plotting_utilities import plot_isosurface, plot_valuefunction
from odp.solver import HJSolver

""" USER INTERFACES
- 0. This file needs to be run with the MRAG/values_calculation/MRAG_6D.py file, 
replace the original odp/computeGraphs/graph_6D.py with the MRAG_6D.py, also change some corresponding variables
- 1. Define grid
- 2. Instantiate the dynamics of the agent
- 3. Generate initial values for grid using shape functions
- 4. Time length for computations
- 5. Initialize plotting option
- 6. Call HJSolver function
"""
# Hanyang: this file is using my-designed value function for 1v2 game
##################################################### EXAMPLE 5 1 vs. 2 AttackerDefender ####################################
# Record the time of whole process
start_time = time.time()

# 1. Define grid
grid_size = 35
speed_d = 1.5

grids = Grid(np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]), 
             6, np.array([grid_size, grid_size, grid_size, grid_size, grid_size, grid_size])) 
process = psutil.Process(os.getpid())
print("1. Gigabytes consumed {}".format(process.memory_info().rss/1e9))  # in bytes

# 2. Instantiate the dynamics of the agent
agents_1v2 = AttackerDefender1vs2(uMode="max", dMode="min")  # Hanyang: from the defender view

# 3. Avoid set, no constraint means inf
avoid1 = ShapeRectangle(grids, [0.6, 0.1, -1000, -1000, -1000, -1000], [0.8, 0.3, 1000, 1000, 1000, 1000])  # avoid attacker arrives the target
avoid1 = np.array(avoid1, dtype='float32')

avoid2_escapeD1 = agents_1v2.capture_set1(grids, 0.1, "escape")  # avoid attacker escapes from defender 1
avoid2_escapeD2 = agents_1v2.capture_set2(grids, 0.1, "escape")  # avoid attacker escapes from defender 2
avoid2 = np.maximum(avoid2_escapeD1, avoid2_escapeD2)  # the intersection of escaping from defender 1 and 2
avoid2 = np.array(avoid2, dtype='float32')
del avoid2_escapeD1
del avoid2_escapeD2

avoid3_obs1D1 = ShapeRectangle(grids, [-1000, -1000, -0.1, -1.0, -1000, -1000], [1000, 1000, 0.1, -0.3, 1000, 1000])  # avoid attacker gets stuck in obs1
avoid3_obs2D1 = ShapeRectangle(grids, [-1000, -1000, -0.1, 0.30, -1000, -1000], [1000, 1000, 0.1, 0.60, 1000, 1000])  # avoid attacker gets stuck in obs2
avoid3_obsD1 = np.minimum(avoid3_obs1D1, avoid3_obs2D1)  # the union of getting stuck in obs1 or obs2
avoid3_obsD1 = np.array(avoid3_obsD1, dtype='float32')
del avoid3_obs1D1
del avoid3_obs2D1

avoid4_obs1D2 = ShapeRectangle(grids, [-1000, -1000, -1000, -1000, -0.1, -1.0], [1000, 1000, 1000, 1000, 0.1, -0.3])  # avoid defender 2 gets stuck in obs1
avoid4_obs2D2 = ShapeRectangle(grids, [-1000, -1000, -1000, -1000, -0.1, 0.30], [1000, 1000, 1000, 1000, 0.1, 0.60])  # avoid defender 2 gets stuck in obs2
avoid4_obsD2 = np.minimum(avoid4_obs1D2, avoid4_obs2D2)  # the union of getting stuck in obs1 or obs2
avoid4_obsD2 = np.array(avoid4_obsD2, dtype='float32')
del avoid4_obs1D2
del avoid4_obs2D2

avoid_set = np.minimum(np.maximum(avoid1, avoid2), np.minimum(avoid3_obsD1, avoid4_obsD2)) 
# avoid_set = np.maximum(avoid1, avoid2)
avoid_set = np.array(avoid_set, dtype='float32')
del avoid1
del avoid2
print("2. After generaing avoid set, the Gigabytes consumed {}".format(process.memory_info().rss/1e9))  # in bytes

# 4. Reach set, no constraint means inf
reach1 = - ShapeRectangle(grids, [0.6, 0.1, -1000, -1000, -1000, -1000], [0.8, 0.3, 1000, 1000, 1000, 1000])  # attacker has not arrived at the target
reach1 = np.array(reach1, dtype='float32')

reach2_captureD1 = agents_1v2.capture_set1(grids, 0.1, "capture")  # attacker is captured by defender 1
reach_captureD1 = np.maximum(reach1, reach2_captureD1)  # the intersection of being captured by defender 1
reach_captureD1 = np.array(reach_captureD1, dtype='float32')
del reach2_captureD1

reach2_captureD2 = agents_1v2.capture_set2(grids, 0.1, "capture")  # attacker is captured by defender 2
reach_captureD2 = np.maximum(reach1, reach2_captureD2)  # the intersection of being captured by defender 2
reach_captureD2 = np.array(reach_captureD2, dtype='float32')
del reach2_captureD2

reach2 = np.minimum(reach_captureD1, reach_captureD2)  # the union of being captured by defender 1 or 2, and the attacker has not arrived at the target
reach2 = np.array(reach2, dtype='float32')
del reach_captureD1
del reach_captureD2
del reach1

reach3_obs1D1 = -ShapeRectangle(grids, [-1000, -1000, -0.1, -1.0, -1000, -1000], [1000, 1000, 0.1, -0.3, 1000, 1000])  # defender 1 does not get stuck in obs1
reach3_obs2D1 = -ShapeRectangle(grids, [-1000, -1000, -0.1, 0.30, -1000, -1000], [1000, 1000, 0.1, 0.60, 1000, 1000])  # defender 1 does not get stuck in obs2
reach3_obsD1 = np.maximum(reach3_obs1D1, reach3_obs2D1)  # the intersection of defender 1 not getting stuck in obs1 or obs2
reach3_obsD1 = np.array(reach3_obsD1, dtype='float32')
del reach3_obs1D1
del reach3_obs2D1

reach4_obs1D2 = ShapeRectangle(grids, [-1000, -1000, -1000, -1000, -0.1, -1.0], [1000, 1000, 1000, 1000, 0.1, -0.3])  # defender 2 does not get stuck in obs1
reach4_obs2D2 = ShapeRectangle(grids, [-1000, -1000, -1000, -1000, -0.1, 0.30], [1000, 1000, 1000, 1000, 0.1, 0.60])  # defender 2 does not get stuck in obs2
reach4_obsD2 = np.maximum(reach4_obs1D2, reach4_obs2D2)  # the intersection of defender 2 not getting stuck in obs1 or obs2
reach4_obsD2 = np.array(reach4_obsD2, dtype='float32')
del reach4_obs1D2
del reach4_obs2D2

reach_set = np.maximum(reach2, np.maximum(reach3_obsD1, reach4_obsD2))
reach_set = np.array(reach_set, dtype='float32')
del reach2
del reach3_obsD1
del reach4_obsD2
gc.collect()
process = psutil.Process(os.getpid())
print("3. After generating reach set, the Gigabytes consumed {}".format(process.memory_info().rss/1e9))  # in bytes

# 4. Look-back length and time step
lookback_length = 4.5  # the same as 2014Mo
t_step = 0.025

# Actual calculation process, needs to add new plot function to draw a 2D figure
small_number = 1e-5
tau = np.arange(start=0, stop=lookback_length + small_number, step=t_step)

# while plotting make sure the len(slicesCut) + len(plotDims) = grid.dims
po = PlotOptions(do_plot=True, plot_type="set", plotDims=[0, 1], slicesCut=[2, 2, 2, 2])

# In this example, we compute a Reach-Avoid Tube
compMethods = {"TargetSetMode": "minVWithVTarget", "ObstacleSetMode": "maxVWithObstacle"} # original one
# compMethods = {"TargetSetMode": "minVWithVTarget"}
solve_start_time = time.time()

result = HJSolver(agents_1v2, grids, [reach_set, avoid_set], tau, compMethods, po, saveAllTimeSteps=None, accuracy="medium") # original one
# result = HJSolver(my_2agents, g, avoid_set, tau, compMethods, po, saveAllTimeSteps=True)
process = psutil.Process(os.getpid())
print(f"The CPU memory used during the calculation of the value function is {process.memory_info().rss/(1024 ** 3): .2f} GB.")  # in bytes

solve_end_time = time.time()
print(f'The shape of the value function is {result.shape} \n')
print(f"The size of the value function is {result.nbytes / (1024 ** 3): .2f} GB or {result.nbytes/(1024 ** 2)} MB.")
print(f"The time of solving HJ is {solve_end_time - solve_start_time} seconds.")
print(f'The shape of the value function is {result.shape} \n')
# save the value function
np.save(f'MRAG/values/1vs2AttackDefend_g{grid_size}_dspeed{speed_d}.npy', result)
print("The value function has been saved successfully.")

# Record the time of whole process
end_time = time.time()
print(f"The time of whole process is {end_time - start_time} seconds.")