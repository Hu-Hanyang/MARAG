import os
import gc
import time
import psutil
import math
import numpy as np

from odp.Grid import Grid
from odp.Shapes import *
from MRAG.envs.DubinCars import DubinCar1vs0
from odp.Plots import PlotOptions
from odp.Plots.plotting_utilities import plot_isosurface, plot_valuefunction
from odp.solver import HJSolver
from MRAG.plots_dub import plot_value_1vs0_dub_debug


""" USER INTERFACES
- 1. Initialize the grids
- 2. Initialize the dynamics
- 3. Instruct the avoid set and reach set
- 4. Set the look-back length and time step
- 5. Call HJSolver function
- 6. Save the value function
"""
##################################################### EXAMPLE 2 1v0AttackerDefender ####################################
# Record the time of whole process
start_time = time.time()

# 1. Initialize the grids
grid_size = 100
grid_size_theta = 200
grids = Grid(np.array([-1.0, -1.0, -math.pi]), np.array([1.0, 1.0, math.pi]), 3, np.array([grid_size, grid_size, grid_size_theta]), [2])

# 2. Initialize the dynamics
angularv = 1.0
agents_1vs0 = DubinCar1vs0(uMode="min", dMode="max", uMax=angularv, dMax=angularv)  

# 3. Instruct the avoid set and reach set
## 3.1 Avoid set, no constraint means inf
obs1_a = ShapeRectangle(grids, [-0.1, -1.0, -1000], [0.1, -0.3, 1000])  # not sure about the third dimension
obs1_a = np.array(obs1_a, dtype='float32')

obs2_a = ShapeRectangle(grids, [-0.1, 0.3, -1000], [0.1, 0.6, 1000]) 
obs2_a = np.array(obs2_a, dtype='float32')

avoid_set = np.minimum(obs1_a, obs2_a)
avoid_set = np.array(avoid_set, dtype='float32')
del obs1_a
del obs2_a

### 3.2 Reach set
reach_set = ShapeRectangle(grids, [0.6, 0.1, -1000], [0.8, 0.3, 1000]) 

# 4. Set the look-back length and time step
lookback_length = 15.0 
t_step = 0.025

# Actual calculation process, needs to add new plot function to draw a 2D figure
small_number = 1e-5
tau = np.arange(start=0, stop=lookback_length + small_number, step=t_step)

# while plotting make sure the len(slicesCut) + len(plotDims) = grid.dims
po = PlotOptions(do_plot=True, plot_type="set", plotDims=[0, 1], slicesCut=[50])

# 5. Call HJSolver function
compMethods = {"TargetSetMode": "minVWithVTarget", "ObstacleSetMode": "maxVWithObstacle"}
# compMethods = {"TargetSetMode": "minVWithVTarget"}
solve_start_time = time.time()

# # Before computation test
# initial_attacker = np.array([[0.0, 0.0, math.pi/2]])
# target = np.maximum(reach_set, -avoid_set)
# plot_value_1vs0_dub_debug(initial_attacker, target, grids)

accuracy = "medium"
result = HJSolver(agents_1vs0, grids, [reach_set, avoid_set], tau, compMethods, po, saveAllTimeSteps=True, accuracy=accuracy)
process = psutil.Process(os.getpid())
print(f"The CPU memory used during the calculation of the value function is {process.memory_info().rss/1e9: .2f} GB.")  # in bytes

solve_end_time = time.time()
print(f'The shape of the value function is {result.shape} \n')
print(f"The size of the value function is {result.nbytes / 1e9: .2f} GB or {result.nbytes/(1e6)} MB.")
print(f"The time of solving HJ is {solve_end_time - solve_start_time} seconds.")
print(f'The shape of the value function is {result.shape} \n')

# 6. Save the value function
np.save(f'MRAG/values/DubinCar1vs0_grid{grid_size}_{accuracy}_{angularv}angularv.npy', result)

print(f"The value function has been saved successfully.")

# Record the time of whole process
end_time = time.time()
print(f"The time of whole process is {end_time - start_time} seconds.")
