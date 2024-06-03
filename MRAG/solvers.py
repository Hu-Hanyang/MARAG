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
    # add constraint 1: upper bound for attackers to be captured based on the 2 vs. 1 game
    for j in range(num_defenders):
        model += xsum(e[i][j] for i in range(num_free_attackers)) <= 2
    # add constraint 2: upper bound for defenders to be assgined based on the 1 vs. 1 game
    for i in range(num_free_attackers):
        model += xsum(e[i][j] for j in range(num_defenders)) <= 1
    # add constraint 3: the attacker i could not be captured by the defender j in the 1 vs. 1 game
    for j in range(num_defenders):
        for indiv in (EscapedAttacker1vs1[j]):
            model += e[np.where(free_attackers_positions == indiv)[0][0]][j] == 0
    # add constraint 4: upper bound for attackers to be captured based on the 2 vs. 1 game result
    for j in range(num_defenders):
        for pairs in (EscapedPairs2vs1[j]):
            print(f"j is {j}, pairs is {pairs}")
            model += e[np.where(free_attackers_positions == pairs[0])[0][0]][j] + e[np.where(free_attackers_positions == pairs[1])[0][0]][j] <= 1
            
    # set up objective functions
    model.objective = maximize(xsum(e[i][j] for j in range(num_defenders) for i in range(num_free_attackers)))
    
    # problem solving
    model.max_gap = 0.05
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

    return assignments


def extend_mip_solver(num_defenders, current_attackers_status,  
                      EscapedAttacker1vs1, EscapedPairs2vs1,
                      EscapedAttackers1vs2, EscapedTri1vs2):
    #TODO: Not finished yet
    # initialize the solver
    num_free_attackers = np.count_nonzero(current_attackers_status == 0)
    free_attackers_positions = np.where(current_attackers_status == 0)[0]
    model = Model(solver_name=CBC) # use GRB for Gurobi, CBC default
    e = [[model.add_var(var_type=BINARY) for j in range(num_defenders)] for i in range(num_free_attackers)] # e[attacker index][defender index]
    # initialize the weakly defend edges set W and their weights for each defender
    Weakly = [[] for _ in range(num_defenders)]
    weights = np.ones((num_free_attackers, num_defenders))
    
    # add constraints
    # add constraint 1: upper bound for attackers to be captured based on the 2 vs. 1 game
    for j in range(num_defenders):
        model += xsum(e[i][j] for i in range(num_free_attackers)) <= 2

    # add constraint 2: upper bound for defenders to be assgined based on the 1 vs. 2 game
    for i in range(num_free_attackers):
        model += xsum(e[i][j] for j in range(num_defenders)) <= 2
    for add in EscapedTri1vs2:
        model += xsum(e[add[0]][j] for j in range(num_defenders)) <= 1
    #     model += e[add[0]][add[1]] + e[add[0]][add[2]] <= 1
    # for i in range(num_attacker):
    #     model += xsum(e[i][j] for j in range(num_defender)) <= 2

    # add constraint 3: the attacker i could not be captured by the defender j in both 1 vs. 1 and 1 vs. 2 games
    for j in range(num_defenders):
        for attacker in EscapedAttacker1vs1[j]:
            if attacker in EscapedAttackers1vs2[j]:  # the attacker could win the defender in both 1 vs. 1 and 1 vs. 2 games
                model += e[attacker][j] == 0
            else:  # the attacker could win the defender in 1 vs. 1 game but not in 1 vs. 2 game
                Weakly[j].append(attacker)
                weights[attacker][j] = 0.5

    # add constraint 4: upper bound for attackers to be captured based on the 2 vs. 1 game result
    for j in range(num_defenders):
        for pairs in (EscapedPairs2vs1[j]):
            # print(pairs)
            model += e[pairs[0]][j] + e[pairs[1]][j] <= 1

    # add constraint 5: upper bound for weakly defended attackers
    for j in range(num_defenders):
        for indiv in (Weakly[j]):
            # print(indiv)
            model += e[indiv][j] <= xsum(e[indiv][k] for k in range(num_defenders))
            
    # set up objective functions
    model.objective = maximize(xsum(weights[i][j] * e[i][j] for j in range(num_defenders) for i in range(num_free_attackers)))
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
        selected = []
        assigned = [[] for _ in range(num_free_attackers)]
        for j in range(num_defenders):
            selected.append([])
            for i in range(num_free_attackers):
                if e[i][j].x >= 0.9:
                    selected[j].append(i)
                    assigned[i].append(j)
        # print(f"The selected results in the extend_mip_solver is {selected}.")

    return selected, weights, assigned