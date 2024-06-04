'''Controllers for the reach-avoid game.

'''
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


def defender_control_2vs1(game, grid2vs1, value2vs1, jointstate_2vs1):
    """Return a list of 2-dimensional control inputs of one defender based on the value function
    
    Args:
    game (class): the corresponding ReachAvoidGameEnv instance
    grid2vs1 (class): the corresponding Grid instance
    value2vs1 (ndarray, (grid_size*dim, 1)): 1v1 HJ reachability value function with only final slice
    game (class instance): the corresponding ReachAvoidGameEnv instance
    jointstate_2vs1 (tuple): the corresponding positions of (A1, A2, D)
    """
    value2vs1s = value2vs1[..., np.newaxis] 
    spat_deriv_vector = spa_deriv(grid2vs1.get_index(jointstate_2vs1), value2vs1s, grid2vs1)
    opt_d1, opt_d2 = game.optDistb_2vs1(spat_deriv_vector)

    return (opt_d1, opt_d2)


def defender_control_1vs1(game, grid1vs1, value1vs1, jointstate_1vs1):
    """Return a list of 2-dimensional control inputs of one defender based on the value function
    
    Args:
    game (class): the corresponding ReachAvoidGameEnv instance
    grid1v1 (class): the corresponding Grid instance
    value1v1 (ndarray): 1v1 HJ reachability value function with only final slice
    agents_1v1 (class): the corresponding AttackerDefender instance
    joint_states1v1 (tuple): the corresponding positions of (A1, D1)
    """
    value1vs1s = value1vs1[..., np.newaxis] 
    spat_deriv_vector = spa_deriv(grid1vs1.get_index(jointstate_1vs1), value1vs1s, grid1vs1)
    opt_d1, opt_d2 = game.optDistb_1vs1(spat_deriv_vector)

    return (opt_d1, opt_d2)


def attacker_control_1vs0(game, grid1vs0, value1vs0, attacker, neg2pos):
    """Return a list of 2-dimensional control inputs of one defender based on the value function
    
    Args:
    game (class): the corresponding ReachAvoidGameEnv instance
    grid1vs0 (class): the corresponding Grid instance
    value1vs0 (ndarray): 1v1 HJ reachability value function with only final slice
    attacker (ndarray, (dim,)): the current state of one attacker
    neg2pos (list): the positions of the value function that change from negative to positive
    """
    current_value = grid1vs0.get_value(value1vs0[..., 0], list(attacker))
    if current_value > 0:
        value1vs0 = value1vs0 - current_value
    v = value1vs0[..., neg2pos] # Minh: v = value1v0[..., neg2pos[0]]
    spat_deriv_vector = spa_deriv(grid1vs0.get_index(attacker), v, grid1vs0)
    opt_a1, opt_a2 = game.optCtrl_1vs0(spat_deriv_vector)

    return (opt_a1, opt_a2)


def find_sign_change1v0(grid1vs0, value1vs0, attacker):
    """Return two positions (neg2pos, pos2neg) of the value function

    Args:
    grid1vs0 (class): the instance of grid
    value1vs0 (ndarray): including all the time slices, shape = [100, 100, len(tau)]
    attacker (ndarray, (dim,)): the current state of one attacker
    """
    current_slices = grid1vs0.get_index(attacker)
    current_value = value1vs0[current_slices[0], current_slices[1], :]  # current value in all time slices
    neg_values = (current_value<=0).astype(int)  # turn all negative values to 1, and all positive values to 0
    checklist = neg_values - np.append(neg_values[1:], neg_values[-1])
    # neg(True) - pos(False) = 1 --> neg to pos
    # pos(False) - neg(True) = -1 --> pos to neg
    return np.where(checklist==1)[0], np.where(checklist==-1)[0]


def hj_controller_defenders(game, assigments, 
                            value1vs1, value2vs1, 
                            grid1vs1, grid2vs1):
    #TODO: Hanyang: big exits 
    """This fuction computes the control for the defenders based on the assignments. 
       Assume dynamics are single integrator.

    Args:
        game (class): the corresponding ReachAvoidGameEnv instance
        assignments (a list of lists): the list of attackers that the defender assigned to capture
        value1vs1 (np.ndarray): the value function for 1 vs 1 game
        value2vs1 (np.ndarray): the value function for 2 vs 1 game
        value1vs2 (np.ndarray): the value function for 1 vs 2 game
        grid1vs1 (Grid): the grid for 1 vs 1 game
        grid2vs1 (Grid): the grid for 2 vs 1 game
        grid1vs2 (Grid): the grid for 1 vs 2 game
    
    Returns:
        control_defenders ((ndarray): the control of defenders
    """
    attackers = game.attackers.state
    defenders = game.defenders.state
    num_defenders = game.NUM_DEFENDERS 
    control_defenders = np.zeros((num_defenders, 2))
    for j in range(num_defenders):
        d1x, d1y = defenders[j]
        if len(assigments[j]) == 2: # defender j capture the attacker selected[j][0] and selected[j][1]
            a1x, a1y = attackers[assigments[j][0]]
            a2x, a2y = attackers[assigments[j][1]]
            jointstate_2vs1 = (a1x, a1y, a2x, a2y, d1x, d1y)
            control_defenders[j] = defender_control_2vs1(game, grid2vs1, value2vs1, jointstate_2vs1)
        elif len(assigments[j]) == 1:
            a1x, a1y = attackers[assigments[j][0]]
            jointstate_1vs1 = (a1x, a1y, d1x, d1y)
            control_defenders[j] = defender_control_1vs1(game, grid1vs1, value1vs1, jointstate_1vs1)
        elif len(assigments[j]) == 0: # defender j could not capture any of attackers
            control_defenders[j] = (0.0, 0.0)
        else:
            raise ValueError("The number of attackers assigned to one defender should be less than 3.")
        
    return control_defenders


def hj_contoller_attackers(game, value1vs0, grid1vs0):
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
    control_attackers = np.zeros((num_attackers, 2))
    for i in range(num_attackers):
        if not current_attackers_status[i]:  # the attacker is free
            neg2pos, pos2neg = find_sign_change1v0(grid1vs0, value1vs0, attackers[i])
            if len(neg2pos):
                control_attackers[i] = attacker_control_1vs0(game, grid1vs0, value1vs0, attackers[i], neg2pos)
            else:
                control_attackers[i] = (0.0, 0.0)
        else:  # the attacker is captured or arrived
            control_attackers[i] = (0.0, 0.0)
            
    return control_attackers




