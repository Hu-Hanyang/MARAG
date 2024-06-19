import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.graph_objects import Layout

from MRAG.utilities import po2slice1vs1,  po2slice2vs1



def plot_value_1vs1(attackers, defenders, plot_attacker, plot_defender, fix_agent, value1vs1, grid1vs1):
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
    a1x_slice, a1y_slice, d1x_slice, d1y_slice = po2slice1vs1(attackers[plot_attacker], defenders[plot_defender], value1vs1.shape[0])
    if fix_agent == 1:  # fix the defender
        value_function1vs1 = value1vs1[:, :, d1x_slice, d1y_slice]
        dims_plot = [0, 1]
        dim1, dim2 = dims_plot[0], dims_plot[1]
    else:
        value_function1vs1 = value1vs1[a1x_slice, a1y_slice, :, :]
        dims_plot = [2, 3]
        dim1, dim2 = dims_plot[0], dims_plot[1]

    complex_x = complex(0, grid1vs1.pts_each_dim[dim1])
    complex_y = complex(0, grid1vs1.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid1vs1.min[dim1]:grid1vs1.max[dim1]: complex_x, grid1vs1.min[dim2]:grid1vs1.max[dim2]: complex_y]
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
    fig.update_layout(autosize=False, width=580, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # $\mathcal{R} \mathcal{A}_{\infty}^{21}$
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")
    

def plot_value_3agents(attackers, defenders, plot_agents, free_dim, value_function, grids):
    """Plot the value function of the game.

    Args:
        attackers (np.ndarray): The attackers' states.
        defenders (np.ndarray): The defenders' states.
        plot_agents (list): The agents to plot the value function, in the sequence of [all attackers, all defenders]
        fix_agent (int): The agent to fix (1 and 2 for defender, 0 for attacker).
        value1vs2 (np.ndarray): The value function of the 1 vs. 2 game.
        grid1vs2 (Grid): The grid of the 1 vs. 2 game.

    Returns:
        None
    """
    assert len(plot_agents) == 3, "The number of agents to plot should be 3."
    assert free_dim in plot_agents, "The fixed agent should be two of plot agents"
    num_attackers = attackers.shape[0]
    info = {}
    attacker_counter, defender_counter = 0, 0
    for player in plot_agents:
        if player < num_attackers:
            info[player] = "Attacker"
            attacker_counter += 1
        else:
            info[player] = "Defender"
            defender_counter += 1
    
    players = np.vstack((attackers, defenders))
    # p1x_slice, p1y_slice, p2x_slice, p2y_slice, p3x_silce, p3y_slice = po2slice2vs1(players[plot_agents[0]], players[plot_agents[1]], players[plot_agents[2]], value_function.shape[0])
    p1x_slice, p1y_slice, p2x_slice, p2y_slice, p3x_silce, p3y_slice = grids.get_index(np.concatenate((players[plot_agents[0]], players[plot_agents[1]], players[plot_agents[2]]), axis=0))
    # po2slice2vs1(players[plot_agents[0]], players[plot_agents[1]], players[plot_agents[2]], value_function.shape[0])

    if plot_agents.index(free_dim) == 0:
        value_function3agents = value_function[:, :, p2x_slice, p2y_slice, p3x_silce, p3y_slice]
        # value_function3agents = value_function[:, :, p2x_slice, p2y_slice, 0, 0]
    elif plot_agents.index(free_dim) == 1:
        value_function3agents = value_function[p1x_slice, p1y_slice, :, :, p3x_silce, p3y_slice]
    else:
        value_function3agents = value_function[p1x_slice, p1y_slice, p2x_slice, p2y_slice, :, :]

    dims_plot = [free_dim*2, free_dim*2+1]
    dim1, dim2 = dims_plot[0], dims_plot[1]

    complex_x = complex(0, grids.pts_each_dim[dim1])
    complex_y = complex(0, grids.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grids.min[dim1]:grids.max[dim1]: complex_x, grids.min[dim2]:grids.max[dim2]: complex_y]
    x_players = players[:, 0]
    y_players = players[:, 1]

    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=value_function3agents.flatten(),
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

    # # plot fixed agents
    for player in plot_agents:
        if info[player] == "Attacker":
            if player == free_dim:
                fig.add_trace(go.Scatter(x=[x_players[player]], y=[y_players[player]], mode="markers", name='Free Attacker', marker=dict(symbol="triangle-up", size=10, color='red')))
            else:
                fig.add_trace(go.Scatter(x=[x_players[player]], y=[y_players[player]], mode="markers", name='Fixed Attacker', marker=dict(symbol="triangle-up", size=10, color='green')))
        else:
            if player == free_dim:
                fig.add_trace(go.Scatter(x=[x_players[player]], y=[y_players[player]], mode="markers", name='Free Defender', marker=dict(symbol="square", size=10, color='red')))   
            else:
                fig.add_trace(go.Scatter(x=[x_players[player]], y=[y_players[player]], mode="markers", name='Fixed Defender', marker=dict(symbol="square", size=10, color='green')))
    # figure settings
    fig.update_layout(title={'text': f"<b>{int(attacker_counter)} vs. {int(defender_counter)} game value function <b>", 'y':0.85, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 20})
    fig.update_layout(autosize=False, width=580, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # $\mathcal{R} \mathcal{A}_{\infty}^{21}$
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")
    

def animation(attackers_traj, defenders_traj, attackers_status):
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
                      title={'text': "<b>Our method, t={}s<b>".format(num_steps/200), 'y':0.85, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    

def record_video(attackers_traj, defenders_traj, attackers_status, filename='animation.mp4', fps=10):
    # Ensure the save directory exists
    save_dir = os.path.join('MRAG', 'game_recordings')
    if not os.path.exists(save_dir):
        os.makedirs(save_dir+'/')
    # Full path for the video file
    video_path = os.path.join(save_dir, filename)

    # VideoWriter setup
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_size = (800, 800)
    out = cv2.VideoWriter(video_path, fourcc, fps, frame_size)

    # Set up the plot
    fig, ax = plt.subplots()
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    
    # Plot the obstacles
    obstacles = [
        [(-0.1, -1.0), (0.1, -1.0), (0.1, -0.3), (-0.1, -0.3), (-0.1, -1.0)], 
        [(-0.1, 0.3), (0.1, 0.3), (0.1, 0.6), (-0.1, 0.6), (-0.1, 0.3)]
    ]
    for obstacle in obstacles:
        x, y = zip(*obstacle)
        ax.plot(x, y, "k-")

    # Plot the target
    target = [(0.6, 0.1), (0.8, 0.1), (0.8, 0.3), (0.6, 0.3), (0.6, 0.1)]
    x, y = zip(*target)
    ax.plot(x, y, "g-")

    for i, (attackers, defenders, status) in enumerate(zip(attackers_traj, defenders_traj, attackers_status)):
        ax.clear()
        ax.set_xlim([-1, 1])
        ax.set_ylim([-1, 1])

        # Re-plot the obstacles and target on each frame
        for obstacle in obstacles:
            x, y = zip(*obstacle)
            ax.plot(x, y, color="black", linestyle="-")
        x, y = zip(*target)
        ax.plot(x, y, color="purple", linestyle="-")

        # Plot attackers
        free_attackers = attackers[status == 0]
        captured_attackers = attackers[status == -1]
        arrived_attackers = attackers[status == 1]

        if free_attackers.size > 0:
            ax.scatter(free_attackers[:, 0], free_attackers[:, 1], c='red', marker='^', label='Free Attackers')
        if captured_attackers.size > 0:
            ax.scatter(captured_attackers[:, 0], captured_attackers[:, 1], c='red', marker='p', label='Captured Attackers')
        if arrived_attackers.size > 0:
            ax.scatter(arrived_attackers[:, 0], arrived_attackers[:, 1], c='green', marker='^', label='Arrived Attackers')

        # Plot defenders
        if defenders.size > 0:
            ax.scatter(defenders[:, 0], defenders[:, 1], c='blue', marker='s', label='Defenders')

        # Convert Matplotlib plot to a frame for OpenCV
        fig.canvas.draw()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

        # Resize and convert to BGR for OpenCV
        img = cv2.resize(img, frame_size)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Write frame to video
        out.write(img)
    print(f"========== Animation saved at {video_path}. ==========")
    # Release the video writer
    out.release()
  

def plot_scene(attackers_traj, defenders_traj, attackers_status, step, save=False, save_path='MRAG'):
    """Plot the scene of the game at a specific step.

    Args:
        attackers_traj (list): List of attackers' trajectories.
        defenders_traj (list): List of defenders' trajectories.
        attackers_status (list): List of attackers' status.
        step (int): The step to plot.
        save (bool): Whether to save the plot.
        save_path (str): The path to save the plot.
    
    Returns:
        None
    """
    assert step <= len(attackers_traj), "The step should be less than the length of the attackers' trajectories."
    attackers = attackers_traj[step]
    defenders = defenders_traj[step]
    status = attackers_status[step]
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Set map boundaries
    ax.set_xlim([-1, 1])
    ax.set_ylim([-1, 1])
    ax.set_aspect('equal', adjustable='box')

    # Add caption
    # plt.text(0, 1.05, "Our Method", ha='center', va='center', fontsize=16)

    # Draw outer map boundary
    outer_map = plt.Rectangle((-1, -1), 2, 2, edgecolor='black', facecolor='none', linewidth=2.0)
    ax.add_patch(outer_map)

    # Draw obstacles
    obstacle1 = plt.Rectangle((-0.1, -1.0), 0.2, 0.7, edgecolor='black', facecolor='none', label='Obstacle', linewidth=2.0)
    obstacle2 = plt.Rectangle((-0.1, 0.3), 0.2, 0.3, edgecolor='black', facecolor='none', linewidth=2.0)
    ax.add_patch(obstacle1)
    ax.add_patch(obstacle2)

    # Draw target
    target = plt.Rectangle((0.6, 0.1), 0.2, 0.2, edgecolor='purple', facecolor='none', label='Target', linewidth=2.0)
    ax.add_patch(target)
    
    # Plot attackers
    for i in range(len(attackers)):
        if status[i] == 0:
            ax.plot(attackers[i, 0], attackers[i, 1], 'r^', label='Free Attacker' if i == 0 else "")
        elif status[i] == -1:
            ax.plot(attackers[i, 0], attackers[i, 1], marker=(4, 2, 0), color='red', markersize=10, label='Captured Attacker' if i == 0 else "")
        elif status[i] == 1:
            ax.plot(attackers[i, 0], attackers[i, 1], 'ro', label='Arrived Attacker' if i == 0 else "")
    
    # Plot defenders
    for i in range(len(defenders)):
        ax.plot(defenders[i, 0], defenders[i, 1], 'bs', label='Defender' if i == 0 else "")
    
    # Add legend
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left', bbox_to_anchor=(1.05, 1))

    # Adjust the plot to ensure the legend is fully visible
    plt.tight_layout()

    if not save:
        plt.show()
    else:
        plt.savefig(f"{save_path}/scene_{step}.png", bbox_inches='tight')
        print(f"Plot saved at {save_path}.")
