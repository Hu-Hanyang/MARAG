import os
import gc
import time
import psutil
import numpy as np

from odp.Grid import Grid
from odp.Shapes import *
from MRAG.envs.AttackerDefender import AttackerDefender2vs1
from odp.Plots import PlotOptions
from odp.Plots.plotting_utilities import plot_isosurface, plot_valuefunction
from odp.solver import HJSolver


""" USER INTERFACES
- 0. This file needs to be run with the MRAG/values_calculation/MRAG_6D.py file, replace the original odp/computeGraphs/graph_6D.py with the MRAG_6D.py
- 1. Initialize the grids
- 2. Initialize the dynamics
- 3. Instruct the avoid set and reach set
- 4. Set the look-back length and time step
- 5. Call HJSolver function
- 6. Save the value function
"""

##################################################### EXAMPLE 6 2v1AttackerDefender ####################################
# Record the time of whole process
start_time = time.time()
print("The start time is {}".format(start_time))

# 1. Initialize the grids
grid_size = 3
grids = Grid(np.array([-1.0, -1.0, -1.0, -1.0, -1.0, -1.0]), np.array([1.0, 1.0, 1.0, 1.0, 1.0, 1.0]), 
             6, np.array([grid_size, grid_size, grid_size, grid_size, grid_size, grid_size]))  # grid = 35

process = psutil.Process(os.getpid())
print("1. Gigabytes consumed by the grids is {}".format(process.memory_info().rss/(1e9)))  # in bytes


# 2. Initialize the dynamics
agents_2v1 = AttackerDefender2vs1(uMode="min", dMode="max")  # 2v1 (6 dim dynamics)

# 3. Instruct the avoid set and reach set
# 3.0 First load the 6D reach-avoid set
# RA_1V1 = np.load("1v1AttackDefend_g25_speed15.npy")  # grid = 25
# RA_1V1 = np.load("1v1AttackDefend_g27_speed15.npy")  # grid = 27
# RA_1V1 = np.load("1v1AttackDefend_g29_speed15.npy")  # grid = 29
# RA_1V1 = np.load("1v1AttackDefend_g31_speed15.npy")  # grid = 31
# RA_1V1 = np.load("1v1AttackDefend_g33_speed15.npy")  # grid = 33
# RA_1V1 = np.load("1v1AttackDefend_g35_speed15.npy")  # grid = 35
RA_1V1 = np.load(f'MRAG/values/1v1AttackDefend_g{grid_size}_dspeed1.5.npy')  # grid = grid_size

# 3.1 Avoid set, no constraint means inf
obs1_a1 = ShapeRectangle(grids, [-0.1, -1.0, -1000, -1000, -1000, -1000], [0.1, -0.3, 1000, 1000, 1000, 1000])  # a1 get stuck in the obs1
obs1_a1 = np.array(obs1_a1, dtype='float32')
process = psutil.Process(os.getpid())
print("2. Gigabytes consumed of the obstalce1 {}".format(process.memory_info().rss/(1e9)))  # in bytes

obs2_a1 = ShapeRectangle(grids, [-0.1, 0.30, -1000, -1000, -1000, -1000], [0.1, 0.60, 1000, 1000, 1000, 1000])  # a1 get stuck in the obs2
obs2_a1 = np.array(obs2_a1, dtype='float32')
process = psutil.Process(os.getpid())
print("3. Gigabytes consumed of the obstalce2 {}".format(process.memory_info().rss/(1e9)))  # in bytes

obs_a1 = np.minimum(obs1_a1, obs2_a1)
obs_a1 = np.array(obs_a1, dtype='float32')
del obs1_a1
del obs2_a1
gc.collect()  #TODO: what does this do?

capture_a1 = agents_2v1.capture_set1(grids, 0.1, "capture")  # a1 is captured
capture_a1 = np.array(capture_a1, dtype='float32')

a1_captured = np.minimum(capture_a1, obs_a1)
a1_captured = np.array(a1_captured, dtype='float32')

# Backproject 4D reach-avoid array to 6D
# The losing conditions is complement of winning conditions of attacker 2

a2_lose_after_a1 = -(np.zeros((grid_size, grid_size, grid_size, grid_size, grid_size, grid_size)) + np.expand_dims(RA_1V1, axis = (0, 1)))  # grid = grid_size
a2_lose_after_a1 = np.array(a2_lose_after_a1, dtype='float32')

process = psutil.Process(os.getpid())
print("4. Gigabytes consumed of the losing conditions {}".format(process.memory_info().rss/(1e9)))  # in bytes

a1_captured_then_a2_lose = np.maximum(a1_captured, a2_lose_after_a1)
a1_captured_then_a2_lose = np.array(a1_captured_then_a2_lose, dtype='float32')
del a1_captured
del a2_lose_after_a1

# Attacker 2 avoid set
obs1_a2 = ShapeRectangle(grids, [-1000, -1000, -0.1, -1.0, -1000, -1000], [1000, 1000, 0.1, -0.3, 1000, 1000])  # a2 get stuck in the obs1
process = psutil.Process(os.getpid())
print("5. Gigabytes consumed of the avoid set1 to attacker2 {}".format(process.memory_info().rss/(1e9)))  # in bytes

obs2_a2 = ShapeRectangle(grids, [-1000, -1000, -0.1, 0.30, -1000, -1000], [1000, 1000, 0.1, 0.60, 1000, 1000])  # a2 get stuck in the obs2
process = psutil.Process(os.getpid())
print("6. Gigabytes consumed of the avoid set2 to attacker2 {}".format(process.memory_info().rss/(1e9)))  # in bytes

obs_a2 = np.minimum(obs1_a2, obs2_a2)
obs_a2 = np.array(obs_a2, dtype='float32')
del obs1_a2
del obs2_a2
gc.collect()
process = psutil.Process(os.getpid())
print("7. Gigabytes consumed {}".format(process.memory_info().rss/(1e9)))  # in bytes

capture_a2 = agents_2v1.capture_set2(grids, 0.1, "capture")  # a2 is captured
capture_a2 = np.array(capture_a2, dtype='float32')
process = psutil.Process(os.getpid())

a2_captured = np.minimum(obs_a2, capture_a2)
a2_captured = np.array(a2_captured, dtype='float32')
del obs_a2
del capture_a2

# The losing conditions is complement of winning conditions of attacker 1
a1_lose_after_a2 = -(np.zeros((grid_size, grid_size, grid_size, grid_size, grid_size, grid_size)) + np.expand_dims(RA_1V1, axis = (2, 3)))  # grid = grid_size

a1_lose_after_a2 = np.array(a1_lose_after_a2, dtype='float32')
process = psutil.Process(os.getpid())
print("8. Gigabytes consumed of the losing conditions a1 lose after a2 {}".format(process.memory_info().rss/(1e9)))  # in bytes

a2_captured_then_a1_lose = np.maximum(a1_lose_after_a2, a2_captured)
a2_captured_then_a1_lose = np.array(a2_captured_then_a1_lose, dtype='float32')
del a1_lose_after_a2
del a2_captured

avoid_set = np.minimum(a2_captured_then_a1_lose, a1_captured_then_a2_lose)
np.array(avoid_set, dtype='float32')
del a2_captured_then_a1_lose
del a1_captured_then_a2_lose

print("9. Gigabytes consumed {}".format(process.memory_info().rss/(1e9)))  # in bytes

# 3.2 Reach set, at least one of them manage to reach the target

a1_goal = ShapeRectangle(grids, [0.6, 0.1, -1000, -1000, -1000, -1000],
                                [0.8, 0.3,  1000,  1000,  1000,  1000])  # a1 is at goal
a1_is_safe = agents_2v1.capture_set1(grids, 0.1, "escape")  # a1 is 0.1 away from defender
a1_wins = np.maximum(a1_goal, a1_is_safe)
a1_wins = np.array(a1_wins, dtype='float32')

a2_goal = ShapeRectangle(grids, [-1000, -1000, 0.6, 0.1, -1000, -1000],
                                [1000,   1000, 0.8, 0.3 , 1000,  1000])  # a2 is at goal
a2_is_safe = agents_2v1.capture_set2(grids, 0.1, "escape")  # a2 escape
a2_wins = np.maximum(a2_goal, a2_is_safe)
a2_wins = np.array(a2_wins, dtype='float32')

a1_or_a2_wins = np.minimum(a1_wins, a2_wins)
del a2_wins
del a1_wins
a1_or_a2_wins = np.array(a1_or_a2_wins, dtype='float32')
gc.collect()

obs1_defend = ShapeRectangle(grids, [-1000, -1000, -1000, -1000, -0.1, -1.0],
                                    [1000, 1000, 1000, 1000, 0.1, -0.3])  # defender stuck in obs1
obs2_defend = ShapeRectangle(grids, [-1000, -1000, -1000, -1000, -0.1, 0.30],
                                    [1000, 1000, 1000, 1000, 0.1, 0.60])  # defender stuck in obs2

d_lose = np.minimum(obs1_defend, obs2_defend)
d_lose = np.array(d_lose, dtype='float32')
del obs2_defend
del obs1_defend
gc.collect()
process = psutil.Process(os.getpid())
print("10. Gigabytes consumed {}".format(process.memory_info().rss/(1e9)))  # in bytes

reach_set = np.minimum(d_lose, a1_or_a2_wins)
reach_set = np.array(reach_set, dtype='float32')
del d_lose
del a1_or_a2_wins
gc.collect()
process = psutil.Process(os.getpid())
print("11. Gigabytes consumed {}".format(process.memory_info().rss/(1e9)))  # in bytes


# 4. Set the look-back length and time step
lookback_length = 1.5  # try 1.5, 2.0, 2.5, 3.0, 5.0, 6.0, 8.0
t_step = 0.025

# Actual calculation process, needs to add new plot function to draw a 2D figure
small_number = 1e-5
tau = np.arange(start=0, stop=lookback_length + small_number, step=t_step)

# while plotting make sure the len(slicesCut) + len(plotDims) = grid.dims
po = PlotOptions(do_plot=True, plot_type="set", plotDims=[0, 1], slicesCut=[2, 2])
# 5. Call HJSolver function
compMethods = {"TargetSetMode": "minVWithVTarget", "ObstacleSetMode": "maxVWithObstacle"} # original one
solve_start_time = time.time()
result = HJSolver(agents_2v1, grids, [reach_set, avoid_set], tau, compMethods, po, saveAllTimeSteps=False) # original one

process = psutil.Process(os.getpid())
print(f"The CPU memory used during the calculation of the value function is {process.memory_info().rss/(1e9): .2f} GB.")  # in bytes

solve_end_time = time.time()
print(f'The shape of the value function is {result.shape} \n')
print(f"The size of the value function is {result.nbytes / (1e9): .2f} GB or {result.nbytes/(1e6)} MB.")
print(f"The time of solving HJ is {solve_end_time - solve_start_time} seconds.")
print(f'The shape of the value function is {result.shape} \n')

print("The calculation is done! \n")

# 6. Save the value function
# np.save(f'MRAG/2v1AttackDefend_g{grid_size}_speed1.5.npy', result)
# print(f"The value function has been saved successfully.")

# Record the time of whole process
end_time = time.time()
print(f"The end time is {end_time}")
print(f"The time of whole process is {end_time - start_time} seconds.")