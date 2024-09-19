import os
import time
import psutil
import numpy as np

from odp.Grid import Grid
from odp.Shapes import *
from MRAG.envs.AttackerDefender import AttackerDefender1vs0
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
#Easier means no obstacles

# Record the time of whole process
start_time = time.time()

# 1. Initialize the grids
grid_size = 100
grids = Grid(np.array([-1.0, -1.0]), np.array([1.0, 1.0]), 2, np.array([grid_size, grid_size]))

# 2. Initialize the dynamics
agents_1v0 = AttackerDefender1vs0(uMode="min", dMode="max") 

# 3. Instruct the avoid set and reach set
# 3.1 Avoid set, no avoid set in the easier setting
# obs1_attack = ShapeRectangle(grids, [-0.1, -1.0], [0.1, -0.3])  # attacker stuck in obs1
# obs2_attack = ShapeRectangle(grids, [-0.1, 0.30], [0.1, 0.60])  # attacker stuck in obs2
# # obs3_capture = agents_1v0.capture_set(grids, 0.1, "capture")  # attacker being captured by defender, try different radius
# avoid_set = np.minimum(obs1_attack, obs2_attack)

# 3.2 Reach set, run and see what it is!
goal1_destination = ShapeRectangle(grids, [0.6, 0.1], [0.8, 0.3])  # attacker arrives target
# goal2_escape = agents_1v0.capture_set(grids, 0.1, "escape")  # attacker escape from defender
# obs1_defend = ShapeRectangle(grids, [-1000, -1000, -0.1, -1000], [1000, 1000, 0.1, -0.3])  # defender stuck in obs1
# obs2_defend = ShapeRectangle(grids, [-1000, -1000, -0.1, 0.30], [1000, 1000, 0.1, 0.60])  # defender stuck in obs2
reach_set = goal1_destination
# plot_original(grids, reach_set)

# 4. Set the look-back length and time step
lookback_length = 2.0  # the same as 2014Mo 
t_step = 0.025
small_number = 1e-5
tau = np.arange(start=0, stop=lookback_length + small_number, step=t_step)

# while plotting make sure the len(slicesCut) + len(plotDims) = grid.dims
po = PlotOptions(do_plot=True, plot_type="set", plotDims=[0, 1], slicesCut=[22, 22])

# 5. Call HJSolver function
# compMethods = {"TargetSetMode": "minVWithVTarget", "ObstacleSetMode": "maxVWithObstacle"} # default for reach-avoid game
compMethods = {"TargetSetMode": "minVWithV0"}

solve_start_time = time.time()
# initial_memory_usage = psutil.virtual_memory().used / (1024 ** 3)
result = HJSolver(agents_1v0, grids, reach_set, tau, compMethods, po, saveAllTimeSteps=True, accuracy="medium") # original one
process = psutil.Process(os.getpid())
print(f"The CPU memory used during the calculation of the value function is {process.memory_info().rss/(1024 ** 3): .2f} GB.")  # in bytes
# result = HJSolver(agents_1v0, grids, reach_set, tau, compMethods, po, saveAllTimeSteps=True)
# final_memory_usage = psutil.virtual_memory().used / (1024 ** 3)
solve_end_time = time.time()
print(f'The shape of the value function is {result.shape} \n')
print(f"The size of the value function is {result.nbytes / (1024 ** 3): .2f} GB or {result.nbytes/(1024 ** 2)} MB.")
print(f"The time of solving HJ is {solve_end_time - solve_start_time} seconds.")

# 6. Save the value function
np.save(f'MRAG/values/1vs0_easier_SIG_g{grid_size}_speed1.0.npy', result)

# Record the time of whole process
end_time = time.time()
print(f"The time of whole process is {end_time - start_time} seconds.")
