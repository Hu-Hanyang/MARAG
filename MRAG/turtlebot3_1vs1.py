import numpy as np


def spa_deriv(slice_index, value_function, grid, periodic_dims=[]):
    """
    Calculates the spatial derivatives of V at an index for each dimension

    Args:
        slice_index: (a1x, a1y)
        value_function (ndarray): [..., neg2pos] where neg2pos is a list [scalar] or []
        grid (class): the instance of the corresponding Grid
        periodic_dims (list): the corrsponding periodical dimensions []

    Returns:
        List of left and right spatial derivatives for each dimension
    """
    spa_derivatives = []
    for dim, idx in enumerate(slice_index):
        if dim == 0:
            left_index = []
        else:
            left_index = list(slice_index[:dim])

        if dim == len(slice_index) - 1:
            right_index = []
        else:
            right_index = list(slice_index[dim + 1:])

        next_index = tuple(
            left_index + [slice_index[dim] + 1] + right_index
        )
        prev_index = tuple(
            left_index + [slice_index[dim] - 1] + right_index
        )

        if idx == 0:
            if dim in periodic_dims:
                left_periodic_boundary_index = tuple(
                    left_index + [value_function.shape[dim] - 1] + right_index
                )
                left_boundary = value_function[left_periodic_boundary_index]
            else:
                left_boundary = value_function[slice_index] + np.abs(value_function[next_index] - value_function[slice_index]) * np.sign(value_function[slice_index])
            left_deriv = (value_function[slice_index] - left_boundary) / grid.dx[dim]
            right_deriv = (value_function[next_index] - value_function[slice_index]) / grid.dx[dim]
        elif idx == value_function.shape[dim] - 1:
            if dim in periodic_dims:
                right_periodic_boundary_index = tuple(
                    left_index + [0] + right_index
                )
                right_boundary = value_function[right_periodic_boundary_index]
            else:
                right_boundary = value_function[slice_index] + np.abs(value_function[slice_index] - value_function[prev_index]) * np.sign([value_function[slice_index]])
            left_deriv = (value_function[slice_index] - value_function[prev_index]) / grid.dx[dim]
            right_deriv = (right_boundary - value_function[slice_index]) / grid.dx[dim]
        else:
            left_deriv = (value_function[slice_index] - value_function[prev_index]) / grid.dx[dim]
            right_deriv = (value_function[next_index] - value_function[slice_index]) / grid.dx[dim]

        spa_derivatives.append(((left_deriv + right_deriv) / 2)[0])
        
    return spa_derivatives


def optDistb_1vs1(spat_deriv, dMode="max", dMax=1.0):
    opt_d = dMax
    if spat_deriv[5] > 0:
        if dMode == "min":
            opt_d = - dMax
    else:
        if dMode == "max":
            opt_d = - dMax

    return opt_d

def hj_contoller_defenders_dub_1vs1(attacker_state, defender_state, value1vs1_dub, grid1vs1_dub):
    """Return a tuple of 1-dimensional control inputs of one defender based on the value function
    
    Args:
        grid1v1 (class): the corresponding Grid instance
        value1v1 (ndarray): 1vs1 HJ reachability value function with only final slice
        agents_1v1 (class): the corresponding AttackerDefender instance
    
    Returns:
        opt_d (tuple): the optimal control of the defender
    """
    control_defenders = np.zeros((1, 1))  # (num_defenders, control_dim)
    
    a1x, a1y, a1o = attacker_state
    d1x, d1y, d1o = defender_state
    jointstate_1vs1 = (a1x, a1y, a1o, d1x, d1y, d1o)

    opt_d = defender_control_1vs1_dub(grid1vs1_dub, value1vs1_dub, jointstate_1vs1)
    control_defenders[0] = (opt_d)

    return control_defenders


def defender_control_1vs1_dub(grid1vs1_dub, value1vs1_dub, jointstate_1vs1):
    """Return a tuple of 2-dimensional control inputs of one defender based on the value function
    
    Args:
        grid1v1 (class): the corresponding Grid instance
        value1v1 (ndarray): 1vs1 HJ reachability value function with only final slice
        agents_1v1 (class): the corresponding AttackerDefender instance
        joint_states1v1 (tuple): the corresponding positions of (A1, D1)
    
    Returns:
        opt_d (tuple): the optimal control of the defender
    """
    value1vs1s = value1vs1_dub[..., np.newaxis] 
    spat_deriv_vector = spa_deriv(grid1vs1_dub.get_index(jointstate_1vs1), value1vs1s, grid1vs1_dub)
    opt_d = optDistb_1vs1(spat_deriv_vector, dMode="max", dMax=1.0) 

    return (opt_d)