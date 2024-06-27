'''Controllers for the reach-avoid game with dub dynamics.

'''
import numpy as np

from MRAG.plots_dub import po2slice1vs0_dub


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


def find_sign_change1vs0_dub(grid1vs0, value1vs0, attacker):
    """Return two positions (neg2pos, pos2neg) of the value function

    Args:
    grid1vs0 (class): the instance of grid
    value1vs0 (ndarray): including all the time slices, shape = [100, 100, 200, len(tau)]
    attacker (ndarray, (dim,)): the current state of one attacker
    """
    current_slices = grid1vs0.get_index(attacker)
    # current_slices = po2slice1vs0_dub(attacker, value1vs0.shape[0])
    current_value = value1vs0[current_slices[0], current_slices[1], current_slices[2], :]  # current value in all time slices
    neg_values = (current_value<=0).astype(int)  # turn all negative values to 1, and all positive values to 0
    checklist = neg_values - np.append(neg_values[1:], neg_values[-1])
    # neg(True) - pos(False) = 1 --> neg to pos
    # pos(False) - neg(True) = -1 --> pos to neg
    return np.where(checklist==1)[0], np.where(checklist==-1)[0]


def attacker_control_1vs0_dub(game, grid1vs0, value1vs0, attacker, neg2pos):
    """Return a list of 1-dimensional control inputs of one defender based on the value function
    
    Args:
    game (class): the corresponding ReachAvoidGameEnv instance
    grid1vs0 (class): the corresponding Grid instance
    value1vs0 (ndarray): 1vs1 HJ reachability value function with only final slice
    attacker (ndarray, (dim,)): the current state of one attacker
    neg2pos (list): the positions of the value function that change from negative to positive
    """
    current_value = grid1vs0.get_value(value1vs0[..., 0], list(attacker))
    if current_value > 0:
        value1vs0 = value1vs0 - current_value
    v = value1vs0[..., neg2pos] # Minh: v = value1v0[..., neg2pos[0]]
    # current_slices = po2slice1vs0_dub(attacker, value1vs0.shape[0])
    spat_deriv_vector = spa_deriv(grid1vs0.get_index(attacker), v, grid1vs0)
    # spat_deriv_vector = spa_deriv(current_slices, v, grid1vs0)
    opt_u = game.optCtrl_1vs0(spat_deriv_vector)

    return (opt_u)


def hj_contoller_attackers_dub(game, value1vs0_dub, grid1vs0_dub):
    """This function computes the control for the attackers based on the control_attackers. 
       Assume dynamics are single integrator.

    Args:
        game (class): the corresponding ReachAvoidGameEnv instance
        value1vs0 (np.ndarray): the value function for 1 vs 0 game with all time slices
        grid1vs0 (Grid): the grid for 1 vs 0 game
    
    Returns:
        control_attackers (ndarray): the control of attackers
    """
    attackers = game.attackers.state
    num_attackers = game.NUM_ATTACKERS
    current_attackers_status = game.attackers_status[-1]
    control_attackers = np.zeros((num_attackers, 1))
    for i in range(num_attackers):
        if not current_attackers_status[i]:  # the attacker is free
            neg2pos, pos2neg = find_sign_change1vs0_dub(grid1vs0_dub, value1vs0_dub, attackers[i])
            if len(neg2pos):
                control_attackers[i] = attacker_control_1vs0_dub(game, grid1vs0_dub, value1vs0_dub, attackers[i], neg2pos)
            else:
                control_attackers[i] = (0.0)
        else:  # the attacker is captured or arrived
            control_attackers[i] = (0.0)
            
    return control_attackers


def hj_contoller_defenders_dub_1vs1(game, value1vs1_dub, grid1vs1_dub):
    """Return a tuple of 1-dimensional control inputs of one defender based on the value function
    
    Args:
        game (class): the corresponding ReachAvoidGameEnv instance
        grid1v1 (class): the corresponding Grid instance
        value1v1 (ndarray): 1vs1 HJ reachability value function with only final slice
        agents_1v1 (class): the corresponding AttackerDefender instance
    
    Returns:
        opt_d (tuple): the optimal control of the defender
    """
    attackers = game.attackers.state.copy()
    defenders = game.defenders.state.copy()
    assert game.NUM_ATTACKERS == 1, "The number of attacker should be 1."
    assert game.NUM_DEFENDERS == 1, "The number of defender should be 1."
    num_defenders = game.NUM_DEFENDERS 
    control_defenders = np.zeros((num_defenders, 1))
    a1x, a1y, a1o = attackers[0]
    d1x, d1y, d1o = defenders[0]
    jointstate_1vs1 = (a1x, a1y, a1o, d1x, d1y, d1o)

    opt_d = defender_control_1vs1_dub(game, grid1vs1_dub, value1vs1_dub, jointstate_1vs1)
    control_defenders[0] = (opt_d)

    return control_defenders


def defender_control_1vs1_dub(game, grid1vs1_dub, value1vs1_dub, jointstate_1vs1):
    """Return a tuple of 2-dimensional control inputs of one defender based on the value function
    
    Args:
        game (class): the corresponding ReachAvoidGameEnv instance
        grid1v1 (class): the corresponding Grid instance
        value1v1 (ndarray): 1vs1 HJ reachability value function with only final slice
        agents_1v1 (class): the corresponding AttackerDefender instance
        joint_states1v1 (tuple): the corresponding positions of (A1, D1)
    
    Returns:
        opt_d (tuple): the optimal control of the defender
    """
    value1vs1s = value1vs1_dub[..., np.newaxis] 
    spat_deriv_vector = spa_deriv(grid1vs1_dub.get_index(jointstate_1vs1), value1vs1s, grid1vs1_dub)
    opt_d = game.optDistb_1vs1(spat_deriv_vector) 

    return (opt_d)


def optDistb_1vs1(spat_deriv, dMode, dMax=1.0):
    opt_d = dMax
    if spat_deriv[5] > 0:
        if dMode == "min":
            opt_d = - dMax
    else:
        if dMode == "max":
            opt_d = - dMax

    return opt_d


def hj_controller_dub_1vs1(uMode, dMode, uMax, dMax, speed, attacker_state, defender_state, value1vs1_dub, grid1vs1_dub,  current_status):
    """Return a tuple of 1-dimensional control inputs of one defender based on the value function
    
    Args:
        attacker_state (ndarray, (1, 3)): the current state of the attacker
        defender_state (ndarray, (1, 3)): the current state of the defender
        grid1vs1 (class): the corresponding Grid instance
        value1vs1 (ndarray): 1vs1 HJ reachability value function with only final slice

    Returns:
        opt_d (tuple): the optimal control of the defender
    """
    control_defenders = np.zeros((1, 1))
    a1x, a1y, a1o = attacker_state[0]
    d1x, d1y, d1o = defender_state[0]
    jointstate_1vs1 = (a1x, a1y, a1o, d1x, d1y, d1o)
    value1vs1s = value1vs1_dub[..., np.newaxis] 
    spat_deriv_vector = spa_deriv(grid1vs1_dub.get_index(jointstate_1vs1), value1vs1s, grid1vs1_dub)
    opt_d = dMax
    if spat_deriv_vector[5] > 0:
        if dMode == "min":
            opt_d = - dMax
    else:
        if dMode == "max":
            opt_d = - dMax

    return opt_d
    
