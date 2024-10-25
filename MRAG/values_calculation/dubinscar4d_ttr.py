# %%
import os
import gc
import time
import psutil
import math
import hashlib
import json
import numpy as np

from odp.Grid import Grid
from odp.Shapes import *
from odp.dynamics import DubinsCar4D
from odp.Plots import PlotOptions
from odp.Plots.plotting_utilities import plot_isosurface, plot_valuefunction
from odp.solver import TTRSolver

# 0. Functions
def get_hash(numpy_dict):
    def ndarray_to_list(arr):
        if isinstance(arr, np.ndarray):
            return arr.tolist()
        return arr
    
    converted_dict = {key: ndarray_to_list(val) for key, val in numpy_dict.items()}
    json_string = json.dumps(converted_dict, sort_keys=True)
    hash_object = hashlib.sha256(json_string.encode("utf-8"))
    hash_string = hash_object.hexdigest()
    
    return hash_string

# 1. Initialize the dynamics
dyn = DubinsCar4D(
    x=[0.0, 0.0, 0.0, 0.0],
    uMin=[-0.5, -1.0],
    uMax=[0.5, 1.0],
    dMin=[0.0, 0.0],
    dMax=[0.0, 0.0],
    uMode="min",
    dMode="max",)
print(f"The dynamics is done.")

# 2. Initialize the grid
min_bounds = np.array([-6.5, 4.0, -0.1, 0.0]) 
max_bounds = np.array([5.0, 15.0, 0.8, 2*np.pi]) 
num_x = 231
num_y = 220
num_speed = 100
num_theta = 100
pts_each_dim = np.array([num_x, num_y, num_speed, num_theta]) 
grid = Grid(min_bounds, max_bounds, 4, pts_each_dim, [3])

process = psutil.Process(os.getpid())
print(f"The grid takes {process.memory_info().rss/1e9: .2f} GB CPU memory.")  # in bytes

# 3. Set the goals
goals = np.array([[-2.5, 5.2],
                   [1.0, 5.2],
                   [-2.6, 5.2],
                   [-2.6, 10.5]])
# %%
# 4. Compute the TTR value functions
ttr_obs = False
TTR_values = []
start_time = time.time()
for goal in goals:
    goal_region = CylinderShape(grid, [2,3], goal, 0.5)
    ttr_value = TTRSolver(dyn,
                          grid,
                          goal_region,
                          0.001,
                          PlotOptions(do_plot=False, plot_type="value", plotDims=[0,1], slicesCut=[9]),
                          )
    print(f"The TTRSolver takes {process.memory_info().rss/1e9: .2f} GB CPU memory.")  # in bytes
    TTR_values.append(ttr_value)
    
end_time = time.time()
print(f"The TTR computation takes {end_time-start_time} seconds to finish. The memory usage is {psutil.virtual_memory().percent}%")

ttr_values = np.stack(TTR_values, axis=0)

ttr_info = {"dyn.z_dim": 4,
            "dyn.u_dim": 2,
            "dyn.u_min": dyn.uMin,
            "dyn.u_max": dyn.uMax,
            "dyn.u_mode": dyn.uMode,
            "dyn.d_mode": dyn.dMode,
            "grid.min": grid.min,
            "grid.max": grid.max,
            "ttr_obs": ttr_obs,
            "goals": goals,
            "recover_ttr_from_brt": False,}

ttr_info_hash = get_hash(ttr_info)
costmapinfo = [561.0, 231.0, 0.05, -6.5, -13.0]
np.savez(
    f"ttr_{ttr_info_hash}",
    ttr_values=ttr_values,
    dyn_z_dim=4,
    dyn_u_dim=2,
    costmapinfo=costmapinfo,
    goals=goals,
    ttr_obs=ttr_obs,
    recover_ttr_from_brt=False,
)
print(f"The npz file ttr_{ttr_info_hash}.npz is saved.")