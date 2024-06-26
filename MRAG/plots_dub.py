import math
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.graph_objects import Layout


def po2slice1vs0_dub(attacker, grid_size):
    """ Convert the position of the attacker and defender to the slice of the value function for 1 vs 1 game.

    Args:
        attacker (np.ndarray): the attacker's state
        defender (np.ndarray): the defender's state
        grid_size (int): the size of the grid
    
    Returns:
        joint_slice (tuple): the joint slice of the joint state using the grid size

    """
    joint_state = (attacker[0], attacker[1], attacker[2])  # (xA1, yA1, xD1, yD1)#TODO: The third joint slice is not correct
    joint_slice = []
    grid_points = np.linspace(-0.5, +0.5, num=grid_size)
    grid_points_theta = np.linspace(-math.pi, math.pi, num=200)
    for i, s in enumerate(joint_state):
        if i == 2:  # theta
            idx = np.searchsorted(grid_points_theta, s)
            if idx > 0 and (
                idx == len(grid_points_theta)
                or math.fabs(s - grid_points_theta[idx - 1])
                < math.fabs(s - grid_points_theta[idx])
            ):
                joint_slice.append(idx - 1)
            else:
                joint_slice.append(idx)
        else:  # x, y
            idx = np.searchsorted(grid_points, s)
            if idx > 0 and (
                idx == len(grid_points)
                or math.fabs(s - grid_points[idx - 1])
                < math.fabs(s - grid_points[idx])
            ):
                joint_slice.append(idx - 1)
            else:
                joint_slice.append(idx)

    return tuple(joint_slice)


def po2slice1vs1_dub(attacker, defender, grid_size):
    """ Convert the position of the attacker and defender to the slice of the value function for 1 vs 1 game.

    Args:
        attacker (np.ndarray): the attacker's state
        defender (np.ndarray): the defender's state
        grid_size (int): the size of the grid
    
    Returns:
        joint_slice (tuple): the joint slice of the joint state using the grid size

    """
    joint_state = (attacker[0], attacker[1], attacker[2], defender[0], defender[1], defender[2]) 
    joint_slice = []
    grid_points = np.linspace(-0.5, +0.5, num=grid_size)
    grid_points_theta = np.linspace(-math.pi, math.pi, num=200)
    for i, s in enumerate(joint_state):
        if i == 2 or i == 5:  # theta
            idx = np.searchsorted(grid_points_theta, s)
            if idx > 0 and (
                idx == len(grid_points_theta)
                or math.fabs(s - grid_points_theta[idx - 1])
                < math.fabs(s - grid_points_theta[idx])
            ):
                joint_slice.append(idx - 1)
            else:
                joint_slice.append(idx)
        else:  # x, y
            idx = np.searchsorted(grid_points, s)
            if idx > 0 and (
                idx == len(grid_points)
                or math.fabs(s - grid_points[idx - 1])
                < math.fabs(s - grid_points[idx])
            ):
                joint_slice.append(idx - 1)
            else:
                joint_slice.append(idx)

    return tuple(joint_slice)


def check_current_value_dub(attackers, defenders, value_function, grids):
    """ Check the value of the current state of the attackers and defenders.

    Args:
        attackers (np.ndarray): the attackers' states
        defenders (np.ndarray): the defenders' states
        value (np.ndarray): the value function for the game
        grids: the instance of the grid
    
    Returns:
        value (float): the value of the current state of the attackers and defenders
    """
    if len(value_function.shape) == 3:  # 1vs0 game
        joint_slice = grids.get_index(attackers[0])
        # joint_slice = po2slice1vs0_dub(attackers[0], value_function.shape[0])
    elif len(value_function.shape) == 6:  # 1vs1 game
        joint_slice = grids.get_index(np.concatenate((attackers[0], defenders[0])))
        # joint_slice = po2slice1vs1_dub(attackers[0], defenders[0], value_function.shape[0])
        
    value = value_function[joint_slice]

    return value


def plot_value_1vs1_dub(attackers, defenders, plot_attacker, plot_defender, fix_agent, value1vs1_dub, grid1vs1_dub):
    """Plot the value function of the game.

    Args:
        attackers (np.ndarray): The attackers' states.
        defenders (np.ndarray): The defenders' states.
        plot_attacker (int): The attacker to plot the value function, other attackers are ignored.
        plot_defender (int): The defender to plot the value function, other defenders are ignored.
        fix_agent (int): The agent to fix (1 for defender, 0 for attacker).
        value1vs1 (np.ndarray): The value function of the 1 vs. 1 game.
        grid1vs1 (Grid): The grid of the 1 vs. 1 game.

    Returns:
        None
    """
    # a1x_slice, a1y_slice, a1o_slice, d1x_slice, d1y_slice, d1o_slice = po2slice1vs1_dub(attackers[plot_attacker], defenders[plot_defender], value1vs1_dub.shape[0])
    a1x_slice, a1y_slice, a1o_slice, d1x_slice, d1y_slice, d1o_slice = grid1vs1_dub.get_index(np.concatenate((attackers[plot_attacker], defenders[plot_defender])))

    if fix_agent == 1:  # fix the defender
        value_function1vs1 = value1vs1_dub[:, :, a1o_slice, d1x_slice, d1y_slice, d1o_slice]
        dims_plot = [0, 1]
        dim1, dim2 = dims_plot[0], dims_plot[1]
    else:
        value_function1vs1 = value1vs1_dub[a1x_slice, a1y_slice, a1o_slice, :, :, d1o_slice]
        dims_plot = [3, 4]
        dim1, dim2 = dims_plot[0], dims_plot[1]

    complex_x = complex(0, grid1vs1_dub.pts_each_dim[dim1])
    complex_y = complex(0, grid1vs1_dub.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid1vs1_dub.min[dim1]:grid1vs1_dub.max[dim1]: complex_x, grid1vs1_dub.min[dim2]:grid1vs1_dub.max[dim2]: complex_y]
    x_attackers = attackers[:, 0]
    y_attackers = attackers[:, 1]
    x_defenders = defenders[:, 0]
    y_defenders = defenders[:, 1]
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=value_function1vs1.flatten(),
        zmin=0.0,
        ncontours=1,
        contours_coloring = 'none', # former: lines 
        name= "Zero-Level", # zero level
        line_width = 1.5,
        line_color = 'magenta',
        zmax=0.0,
    ), layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) #,paper_bgcolor='rgba(0,0,0,0)'
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")
    fig.add_trace(go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')))
    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0))
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    # plot attackers
    fig.add_trace(go.Scatter(x=x_attackers, y=y_attackers, mode="markers", name='Attacker', marker=dict(symbol="triangle-up", size=10, color='red')))
    # plot defenders
    fig.add_trace(go.Scatter(x=x_defenders, y=y_defenders, mode="markers", name='Fixed Defender', marker=dict(symbol="square", size=10, color='green')))
   
    # figure settings
    fig.update_layout(title={'text': f"<b>1 vs. 1 value function<b>", 'y':0.85, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 20})
    fig.update_layout(autosize=False, width=580, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1.0, 1.0], yaxis_range=[-1.0, 1.0], font=dict(size=20)) # $\mathcal{R} \mathcal{A}_{\infty}^{21}$
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")



def plot_value_1vs0_dub(attackers, defenders, value1vs0_dub, grid1vs0_dub):
    """Plot the value function of the game.

    Args:
        attackers (np.ndarray): The attackers' states.
        defenders (np.ndarray): The defenders' states.
        plot_attacker (int): The attacker to plot the value function, other attackers are ignored.
        plot_defender (int): The defender to plot the value function, other defenders are ignored.
        fix_agent (int): The agent to fix (1 for defender, 0 for attacker).
        value1vs1 (np.ndarray): The value function of the 1 vs. 1 game.
        grid1vs1 (Grid): The grid of the 1 vs. 1 game.

    Returns:
        None
    """
    a1x_slice, a1y_slice, a1o_slice = grid1vs0_dub.get_index(attackers[0])

    value_function1vs1 = value1vs0_dub[:, :, a1o_slice, 0]
    dims_plot = [0, 1]
    dim1, dim2 = dims_plot[0], dims_plot[1]
    
    complex_x = complex(0, grid1vs0_dub.pts_each_dim[dim1])
    complex_y = complex(0, grid1vs0_dub.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid1vs0_dub.min[dim1]:grid1vs0_dub.max[dim1]: complex_x, grid1vs0_dub.min[dim2]:grid1vs0_dub.max[dim2]: complex_y]
    x_attackers = attackers[:, 0]
    y_attackers = attackers[:, 1]
    x_defenders = defenders[:, 0]
    y_defenders = defenders[:, 1]
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=value_function1vs1.flatten(),
        zmin=0.0,
        ncontours=1,
        contours_coloring = 'none', # former: lines 
        name= "Zero-Level", # zero level
        line_width = 1.5,
        line_color = 'magenta',
        zmax=0.0,
    ), layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) #,paper_bgcolor='rgba(0,0,0,0)'
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.30, line=dict(color='purple', width=3.0), name="Target")
    fig.add_trace(go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')))
    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0))
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.30, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    # plot attackers
    fig.add_trace(go.Scatter(x=x_attackers, y=y_attackers, mode="markers", name='Attacker', marker=dict(symbol="triangle-up", size=10, color='red')))
    # plot defenders
    fig.add_trace(go.Scatter(x=x_defenders, y=y_defenders, mode="markers", name='Current Defender', marker=dict(symbol="square", size=10, color='blue')))
   
    # figure settings
    fig.update_layout(title={'text': f"<b>1 vs. 0 value function<b>", 'y':0.85, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 20})
    fig.update_layout(autosize=False, width=580, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1.0, 1.0], yaxis_range=[-1.0, 1.0], font=dict(size=20)) # $\mathcal{R} \mathcal{A}_{\infty}^{21}$
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")



def animation_dub(attackers_traj, defenders_traj, attackers_status):
    """Animate the game.

    Args:
        attackers_traj (list): List of attackers' trajectories.
        defenders_traj (list): List of defenders' trajectories.
        attackers_status (list): List of attackers' status.

    Returns:
        None
    """
    # Determine the number of steps
    num_steps = len(attackers_traj)
    num_attackers = attackers_traj[0].shape[0]
    num_defenders = defenders_traj[0].shape[0]

    # Create frames for animation
    frames = []
    for step in range(num_steps):
        attackers = attackers_traj[step]
        defenders = defenders_traj[step]
        status = attackers_status[step]

        x_list = []
        y_list = []
        symbol_list = []
        color_list = []

        # Go through list defenders
        for j in range(num_defenders):
            x_list.append(defenders[j][0])
            y_list.append(defenders[j][1])
            symbol_list += ["square"]
            color_list += ["blue"]
        
        # Go through list of attackers
        for i in range(num_attackers):
            x_list.append(attackers[i][0])
            y_list.append(attackers[i][1])
            if status[i] == -1:  # attacker is captured
                symbol_list += ["cross-open"]
            elif status[i] == 1:  # attacker has arrived
                symbol_list += ["circle"]
            else:  # attacker is free
                symbol_list += ["triangle-up"]
            color_list += ["red"]

        # Generate a frame based on the characteristic of each agent
        frames.append(go.Frame(data=go.Scatter(x=x_list, y=y_list, mode="markers", name="Agents trajectory",
                                               marker=dict(symbol=symbol_list, size=5, color=color_list), showlegend=False)))

    
    # Static object - obstacles, goal region, grid
    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')),
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)', updatemenus=[dict(type="buttons",
                                                                            buttons=[dict(label="Play", method="animate",
                                                                            args=[None, {"frame": {"duration": 30, "redraw": True},
                                                                            "fromcurrent": True, "transition": {"duration": 0}}])])]), frames=frames) # for the legend

    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")
    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))

    # figure settings
    # fig.update_layout(showlegend=False)  # to display the legends or not
    fig.update_layout(autosize=False, width=560, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0),
                      title={'text': "<b>Our method, t={}s<b>".format(num_steps/200), 'y':0.85, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1.0, 1.0], yaxis_range=[-1.0, 1.0], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()