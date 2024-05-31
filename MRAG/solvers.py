'''Solvers for the reach-avoid game.

'''
import numpy as np

from mip import Model, xsum, maximize, BINARY, CBC, OptimizationStatus


def mip_solver(num_defenders, current_attackers_status,  EscapedAttacker1vs1, EscapedPairs2vs1):
    """ Returns a list selected that contains all allocated attackers that the defender could capture, [[a1, a3], ...]

    Args:
        num_defenders (int): the number of defenders
        current_attackers_status (np.ndarray, (num_attackers, )): the current moment attackers' status, 0 stands for free, -1 stands for captured, 1 stands for arrived
        EscapedAttacker1vs1 (list): the attacker that could escape from the defender in a 1 vs 1 game
        EscapedPairs2vs1 (list): the pair of attackers that could escape from the defender in a 2 vs 1 game
    
    Returns:
        assignments (a list of lists): the list of attackers that the defender assigned to capture
    """
    # initialize the solver
    num_free_attackers = np.count_nonzero(current_attackers_status == 0)
    free_attackers_positions = np.where(current_attackers_status == 0)[0]
    
    model = Model(solver_name=CBC) # use GRB for Gurobi, CBC default
    e = [[model.add_var(var_type=BINARY) for j in range(num_defenders)] for i in range(num_free_attackers)] # e[attacker index][defender index]
    # add constraints
    # add constraints 12c
    for j in range(num_defenders):
        model += xsum(e[i][j] for i in range(num_free_attackers)) <= 2
    # add constraints 12d
    for i in range(num_free_attackers):
        model += xsum(e[i][j] for j in range(num_defenders)) <= 1
    # add constraints 12c EscapedPairs2vs1
    for j in range(num_defenders):
        for pairs in (EscapedPairs2vs1[j]):
            # print(pairs)
            model += e[pairs[0]][j] + e[pairs[1]][j] <= 1
    # add constraints 12f EscapedAttacker1vs1
    for j in range(num_defenders):
        for indiv in (EscapedAttacker1vs1[j]):
            # print(indiv)
            model += e[indiv][j] == 0
    # set up objective functions
    model.objective = maximize(xsum(e[i][j] for j in range(num_defenders) for i in range(num_free_attackers)))
    # problem solving
    model.max_gap = 0.05
    # log_status = []
    status = model.optimize(max_seconds=300)
    if status == OptimizationStatus.OPTIMAL:
        print('optimal solution cost {} found'.format(model.objective_value))
    elif status == OptimizationStatus.FEASIBLE:
        print('sol.cost {} found, best possible: {} '.format(model.objective_value, model.objective_bound))
    elif status == OptimizationStatus.NO_SOLUTION_FOUND:
        print('no feasible solution found, lower bound is: {} '.format(model.objective_bound))
    if status == OptimizationStatus.OPTIMAL or status == OptimizationStatus.FEASIBLE:
        print('Solution:')
        assignments = []
        for j in range(num_defenders):
            assignments.append([])
            for i in range(num_free_attackers):
                if e[i][j].x >= 0.9:
                    assignments[j].append(free_attackers_positions[i])
        # print(assignments)
    return assignments

def extend_mip_solver(num_attacker, num_defender, attacker_status, Escape1v1, Escape1v2, Escape_Triad, Escape_Pair):
    pass