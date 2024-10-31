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

def compute_4d_ttr(ttr_whole_map=False):
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
    if ttr_whole_map: 
        # in theory the speed ranges from [-0.1, 0.8], we extend this range to make sure the extremes are covered
        min_bounds = np.array([-6.5, -13.0, -0.3, 0.0])  
        costmapinfo = [561.0, 231.0, 0.05, -6.5, -13.0]
        num_y = 561
    else:
        min_bounds = np.array([-6.5, 4.0, -0.3, 0.0])
        costmapinfo = [220.0, 231.0, 0.05, -6.5, 4.0]  
        num_y = 220 
        
    max_bounds = np.array([5.0, 15.0, 1.0, 2*np.pi]) 
    num_x = 231  
    num_speed = 100
    num_theta = 100
    pts_each_dim = np.array([num_x, num_y, num_speed, num_theta]) 
    
    grid = Grid(min_bounds.copy(), max_bounds.copy(), 4, pts_each_dim.copy(), [3])
    process = psutil.Process(os.getpid())
    print(f"The grid takes {process.memory_info().rss/1e9: .2f} GB CPU memory.")  # in bytes

    # 3. Set the goals and obstacles
    goals = np.array([[-2.5, 5.2],
                    [1.0, 5.2],
                    [-2.6, 5.2],
                    [-2.6, 10.5]])
    speed_obs1 = ShapeRectangle(grid, 
                                [min_bounds.copy()[0], min_bounds.copy()[1], -0.3, min_bounds.copy()[3]],
                                [max_bounds.copy()[0], max_bounds.copy()[1], -0.15, max_bounds.copy()[3]])
    speed_obs2 = ShapeRectangle(grid,
                                [min_bounds.copy()[0], min_bounds.copy()[1], 0.85, min_bounds.copy()[3]],
                                [max_bounds.copy()[0], max_bounds.copy()[1], 1.0, max_bounds.copy()[3]])  
    speed_obs = np.minimum(speed_obs1, speed_obs2)
    del speed_obs1
    del speed_obs2
    # %%
    # 4. Compute the TTR value functions
    ttr_obs = False
    TTR_values = []
    start_time = time.time()
    for goal in goals:
        xy_goal = CylinderShape(grid, [2,3], goal, 0.5)
        speed_lower = Lower_Half_Space(grid, 2, 0.4)
        speed_upper = Upper_Half_Space(grid, 2, 0.0)
        speed_goal = Intersection(speed_lower, speed_upper)
        goal_region = Intersection(xy_goal, speed_goal)
        del xy_goal
        del speed_lower
        del speed_upper
        del speed_goal
        ttr_value = TTRSolver(dyn,
                            grid,
                            [goal_region, speed_obs],
                            0.001,
                            PlotOptions(do_plot=False, plot_type="value", plotDims=[0,1], slicesCut=[9]),
                            )
        print(f"The TTRSolver takes {process.memory_info().rss/1e9: .2f} GB CPU memory.")  # in bytes
        TTR_values.append(ttr_value)
        
    end_time = time.time()
    print(f"The TTR computation takes {end_time-start_time} seconds to finish. The memory usage is {psutil.virtual_memory().percent}%")

    ttr_values = np.stack(TTR_values, axis=0)
    grid_info = [min_bounds, max_bounds, pts_each_dim]
    ttr_info = {"dyn.z_dim": 4,
                "dyn.u_dim": 2,
                "dyn.u_min": dyn.uMin,
                "dyn.u_max": dyn.uMax,
                "dyn.u_mode": dyn.uMode,
                "dyn.d_mode": dyn.dMode,
                "grid.min": min_bounds,
                "grid.max": max_bounds,
                "ttr_obs": ttr_obs,
                "goals": goals,
                "recover_ttr_from_brt": False,}

    ttr_info_hash = get_hash(ttr_info)
    np.savez(
        f"ttr_{ttr_info_hash}",
        ttr_values=ttr_values,
        dyn_z_dim=4,
        dyn_u_dim=2,
        costmapinfo=costmapinfo,
        goals=goals,
        grid_info=grid_info,
        ttr_obs=ttr_obs,
        recover_ttr_from_brt=False,
    )
    print(f"The npz file ttr_{ttr_info_hash}.npz is saved.")


if __name__ == "__main__":
    compute_4d_ttr(ttr_whole_map=False)