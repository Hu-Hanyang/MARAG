import plotly.graph_objects as go
<<<<<<< HEAD
from plotly.graph_objects import Layout
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np



def plot_isosurface(grid, V, plot_option):
=======
from plotly.subplots import make_subplots
import plotly.express as px
from odp.Grid import Grid
import numpy as np

def plot_isosurface(grid, V_ori, plot_option):
    
>>>>>>> dev_hhy
    dims_plot = plot_option.dims_plot

    grid, my_V = pre_plot(plot_option, grid, V_ori)

<<<<<<< HEAD
    if len(dims_plot) == 2:
        dim1, dim2 = dims_plot[0], dims_plot[1]
        complex_x = complex(0, grid.pts_each_dim[dim1])
        complex_y = complex(0, grid.pts_each_dim[dim2])
        mg_X, mg_Y= np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
        print("Plotting beautiful 2D plots. Please wait\n")
        fig = go.Figure(data=go.Contour(
            x=mg_X.flatten(),
            y=mg_Y.flatten(),
            z=V.flatten(),
            colorscale='jet'
        ))
        fig.show()
        print("Please check the plot on your browser.")

    elif len(dims_plot) == 3:
        dim1, dim2, dim3 = dims_plot[0], dims_plot[1], dims_plot[2]
        complex_x = complex(0, grid.pts_each_dim[dim1])
        complex_y = complex(0, grid.pts_each_dim[dim2])
        complex_z = complex(0, grid.pts_each_dim[dim3])
        mg_X, mg_Y, mg_Z = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y,
                           grid.min[dim3]:grid.max[dim3]: complex_z]
=======
    if len(dims_plot) != 3 and len(dims_plot) != 2 and len(dims_plot) != 1:
        raise Exception('dims_plot length should be equal to 3, 2 or 1\n')

    if len(dims_plot) == 3 and len(my_V.shape) == 3:
        # Plot 3D isosurface for only one time step
        
        complex_x = complex(0, grid.pts_each_dim[0])
        complex_y = complex(0, grid.pts_each_dim[1])
        complex_z = complex(0, grid.pts_each_dim[2])
        mg_X, mg_Y, mg_Z = np.mgrid[grid.min[0]:grid.max[0]: complex_x, grid.min[1]:grid.max[1]: complex_y,
                           grid.min[2]:grid.max[2]: complex_z]
        

>>>>>>> dev_hhy

        if (my_V > 0.0).all():
            print("Implicit surface will not be shown since all values are positive ")
        if (my_V < 0.0).all():
            print("Implicit surface will not be shown since all values are negative ")

<<<<<<< HEAD
        if (V > 0.0).all() or (V < 0.0).all():
            print("Implicit surface will not be shown since all values have the same sign ")
        print("Plotting beautiful 3D plots. Please wait\n")
=======
        print("Plotting beautiful plots. Please wait\n")
>>>>>>> dev_hhy
        fig = go.Figure(data=go.Isosurface(
            x=mg_X.flatten(),
            y=mg_Y.flatten(),
            z=mg_Z.flatten(),
            value=my_V.flatten(),
            caps=dict(x_show=True, y_show=True),
            isomin=plot_option.min_isosurface,
            surface_count=plot_option.surface_count,
            isomax=plot_option.max_isosurface,
            colorscale=plot_option.colorscale,
            opacity=plot_option.opacity,
            contour=plot_option.contour,
            flatshading=plot_option.flatshading,
            lighting=plot_option.lighting,
            lightposition=plot_option.lightposition,
            reversescale=plot_option.reversescale,
            showlegend=plot_option.showlegend,
            showscale=plot_option.showscale,
        ))

    if len(dims_plot) == 3 and len(my_V.shape) == 4:
        # Plot 3D isosurface with animation
        # dim1, dim2, dim3 = dims_plot[0], dims_plot[1], dims_plot[2]
        
        complex_x = complex(0, grid.pts_each_dim[0])
        complex_y = complex(0, grid.pts_each_dim[1])
        complex_z = complex(0, grid.pts_each_dim[2])
        mg_X, mg_Y, mg_Z = np.mgrid[grid.min[0]:grid.max[0]: complex_x, grid.min[1]:grid.max[1]: complex_y,
                           grid.min[2]:grid.max[2]: complex_z]

        N = my_V.shape[3]
        print("Plotting beautiful plots. Please wait\n")

        # Define frames
        fig = go.Figure(frames=[go.Frame(data = go.Isosurface(
            x=mg_X.flatten(),
            y=mg_Y.flatten(),
            z=mg_Z.flatten(),
            value=my_V[:, :, :, N-k-1].flatten(),
            caps=dict(x_show=True, y_show=True),
            isomin=plot_option.min_isosurface,
            surface_count=plot_option.surface_count,
            isomax=plot_option.max_isosurface,
            colorscale=plot_option.colorscale,
            opacity=plot_option.opacity,
            contour=plot_option.contour,
            flatshading=plot_option.flatshading,
            lighting=plot_option.lighting,
            lightposition=plot_option.lightposition,
            reversescale=plot_option.reversescale,
            showlegend=plot_option.showlegend,
            showscale=plot_option.showscale,
            ),
            name=str(k) # you need to name the frame for the animation to behave properly
            )
            for k in range(N)])

        # Add data to be displayed before animation starts
        fig.add_trace(go.Isosurface(
            x=mg_X.flatten(),
            y=mg_Y.flatten(),
            z=mg_Z.flatten(),
            value=my_V[:, :, :, N-1].flatten(),
            caps=dict(x_show=True, y_show=True),
            isomin=plot_option.min_isosurface,
            surface_count=plot_option.surface_count,
            isomax=plot_option.max_isosurface,
            colorscale=plot_option.colorscale,
            opacity=plot_option.opacity,
            contour=plot_option.contour,
            flatshading=plot_option.flatshading,
            lighting=plot_option.lighting,
            lightposition=plot_option.lightposition,
            reversescale=plot_option.reversescale,
            showlegend=plot_option.showlegend,
            showscale=plot_option.showscale,
            ))
        
        fig.update_layout(
            title='3D Set',
            scene=dict( xaxis={"nticks": 20},
                        zaxis={"nticks": 20},
                        camera_eye={"x": 0, "y": -1, "z": 0.5},
                        aspectratio={"x": 1, "y": 1, "z": 0.6}
                        ))
        
        fig = slider_define(fig)


    if len(dims_plot) == 2 and len(my_V.shape) == 2:
        # Plot 2D isosurface for only one time step
        # dim1, dim2 = dims_plot[0], dims_plot[1]
        complex_x = complex(0, grid.pts_each_dim[0])
        complex_y = complex(0, grid.pts_each_dim[1])
        mg_X, mg_Y = np.mgrid[grid.min[0]:grid.max[0]: complex_x, grid.min[1]:grid.max[1]: complex_y]


        if (my_V > 0.0).all():
            print("Implicit surface will not be shown since all values are positive ")
        if (my_V < 0.0).all():
            print("Implicit surface will not be shown since all values are negative ")

        print("Plotting beautiful 2D plots. Please wait\n")
        # TODO Chong
        fig = go.Figure(data=go.Contour(
            x=mg_X.flatten(),
            y=mg_Y.flatten(),
            z=my_V.flatten(),
            zmin=0.0,
            ncontours=1,
            contours_coloring='none',  # former: lines
            name="Reachable Set",  # zero level
            line_width=1.5,
            line_color='magenta',
            zmax=0.0,
        ), layout=go.Layout(plot_bgcolor='rgba(0,0,0,0)'))  # ,paper_bgcolor='rgba(0,0,0,0)'

    if len(dims_plot) == 2 and len(my_V.shape) == 3:
        # Plot 2D isosurface with animation
        # dim1, dim2 = dims_plot[0], dims_plot[1]
        complex_x = complex(0, grid.pts_each_dim[0])
        complex_y = complex(0, grid.pts_each_dim[1])
        mg_X, mg_Y = np.mgrid[grid.min[0]:grid.max[0]: complex_x, grid.min[1]:grid.max[1]: complex_y]

        N = my_V.shape[2]

        print("Plotting beautiful plots. Please wait\n")
        # Define frames
        fig = go.Figure(frames=[go.Frame(data = go.Contour(
            x=mg_X.flatten(),
            y=mg_Y.flatten(),
            z=my_V[:,:,N-k-1].flatten(),
            zmin=0.0,
            ncontours=1,
            contours_coloring='none',  # former: lines
            name="Reachable Set",  # zero level
            line_width=1.5,
            line_color='magenta',
            zmax=0.0,
            ), layout=go.Layout(plot_bgcolor='rgba(0,0,0,0)'),
            name=str(k) # you need to name the frame for the animation to behave properly
            )
            for k in range(N)])

        # Add data to be displayed before animation starts
        fig.add_trace(go.Contour(
            x=mg_X.flatten(),
            y=mg_Y.flatten(),
            z=my_V[:,:,N-1].flatten(),
            zmin=0.0,
            ncontours=1,
            contours_coloring='none',  # former: lines
            name="Reachable Set",  # zero level
            line_width=1.5,
            line_color='magenta',
            zmax=0.0,
            ))
        
        fig.update_layout(title='2D Set',)
        
        fig = slider_define(fig)


    if len(dims_plot) == 1 and len(my_V.shape) == 1:
        # Plot 1D isosurface for only one time step
        # dim1 = dims_plot[0]
        complex_x = complex(0, grid.pts_each_dim[0])
        mg_X = np.mgrid[grid.min[0]:grid.max[0]: complex_x]

        if (my_V > 0.0).all():
            print("Implicit surface will not be shown since all values are positive ")
        if (my_V < 0.0).all():
            print("Implicit surface will not be shown since all values are negative ")

        print("Plotting beautiful 1D plots. Please wait\n")
        fig = go.Figure(data=px.line(
            x=mg_X.flatten(),
            y=my_V.flatten(),
            name="Reachable Set",
            labels={'x','Vaue'}
        ), layout=go.Layout(plot_bgcolor='rgba(0,0,0,0)'))



    if len(dims_plot) == 1 and len(my_V.shape) == 2:
        # Plot 1D isosurface with animation
        # dim1 = dims_plot[0]
        complex_x = complex(0, grid.pts_each_dim[0])
        mg_X = np.mgrid[grid.min[0]:grid.max[0]: complex_x]
        
        N = my_V.shape[1]

        # Define frames
        fig = go.Figure(frames=[go.Frame(data=px.line(
            x=mg_X.flatten(),
            y=my_V[:,N-k-1].flatten(),
            labels={'x','Vaue'}
            ), layout=go.Layout(plot_bgcolor='rgba(0,0,0,0)'),
            name=str(k) # you need to name the frame for the animation to behave properly
            )
            for k in range(N)])

        # Add data to be displayed before animation starts
        fig.add_trace(go.Contour(
            x=mg_X.flatten(),
            y=mg_Y.flatten(),
            z=my_V[:,:,N-1].flatten(),
            zmin=0.0,
            ncontours=1,
            contours_coloring='none',  # former: lines
            line_width=1.5,
            line_color='magenta',
            zmax=0.0,
            ))
        
        fig.update_layout(title='1D Value Function',)
        
        fig = slider_define(fig)


    if plot_option.do_plot:
        fig.show()
        print("Please check the plot on your browser.")

<<<<<<< HEAD
    else:
        raise Exception('dims_plot length should be equal to 2 or 3\n')

def plot_2d(grid, V_2D):
    dims_plot = [0, 1]
    dim1, dim2 = dims_plot[0], dims_plot[1]
    complex_x = complex(0, grid.pts_each_dim[dim1])
    complex_y = complex(0, grid.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=V_2D.flatten(),
        zmin=0.0,
        ncontours=1,
        contours_coloring = 'lines',
        line_width = 1.5,
        line_color = 'Red',
        zmax=0.0,
    ), layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) #,paper_bgcolor='rgba(0,0,0,0)'
    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=2.0))
    fig.add_shape(type='line', x0=-0.1, y0=-1.0, x1=-0.1, y1=-0.3, line=dict(color='black', width=2.0))
    fig.add_shape(type='line', x0=0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    fig.add_shape(type='line', x0=-0.1, y0=-0.3, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=2.0))
    # figure settings
    fig.update_layout(autosize=False, width=500, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White") # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 1.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 1.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_2d_with_avoid(grid, V_2D):
    dims_plot = [0, 1]
    dim1, dim2 = dims_plot[0], dims_plot[1]
    complex_x = complex(0, grid.pts_each_dim[dim1])
    complex_y = complex(0, grid.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
    x_obstacle = np.linspace(-0.5, 0.5, num=mg_X.flatten().shape[0])
    y_obstacle = np.linspace(-0.5, 0.5, num=mg_X.flatten().shape[0])
    V_obstacle = np.ones(V_2D.shape)
    # print(f'The shape of mg_X before flatten is {mg_X.shape}')
    # print(f'The shape of mg_Y before flatten is {mg_Y.shape}')
    # print(f'The shape of V_2D before flatten is {V_2D.shape}')
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=V_2D.flatten(),
        zmin=0.0,
        ncontours=1,
        zmax=0.0,
    ))
    fig.add_trace(go.Contour(
        x=x_obstacle.flatten(),
        y=y_obstacle.flatten(),
        z=V_obstacle.flatten(),
        zmin=0.0,
        ncontours=1,
        zmax=0.0,
    ))
    fig.show()
    # print(f'The shape of x after flatten is {mg_X.flatten().shape}')
    # print(f'The shape of y after flatten is {mg_Y.flatten().shape}')
    # print(f'The shape of z after flatten is {V_2D.flatten().shape}')
    print("Please check the plot on your browser.")

def plot_game(grid, V_2D, attackers, defenders, name):
    # based on the plot_2d, add the attacker and the defender 
    dims_plot = [0, 1]
    dim1, dim2 = dims_plot[0], dims_plot[1]
    complex_x = complex(0, grid.pts_each_dim[dim1])
    complex_y = complex(0, grid.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
    x_attackers = [a[0] for a in attackers]
    y_attackers = [a[1] for a in attackers]
    x_defenders = [d[0] for d in defenders]
    y_defenders = [d[1] for d in defenders]
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=V_2D.flatten(),
        zmin=0.0,
        ncontours=1,
        contours_coloring = 'none', # former: lines 
        name= "Reachable Set", # zero level
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
    # fig.add_shape(type='line', x0=-0.1, y0=-1.0, x1=-0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=-0.1, y0=-0.3, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # plot attackers
    fig.add_trace(go.Scatter(x=x_attackers, y=y_attackers, mode="markers", name='Attacker', marker=dict(symbol="triangle-up", size=10, color='red')))
    # for i in range(len(x_attackers)):
    #     fig.add_trace(go.Scatter(x=[x_attackers[i]], y=[y_attackers[i]], mode="markers", name=f'Attacker{i+1}', marker=dict(symbol="triangle-up", size=10, color='red')))
    # plot defenders
    fig.add_trace(go.Scatter(x=x_defenders, y=y_defenders, mode="markers", name='Defender', marker=dict(symbol="square", size=10, color='blue')))
   
    # figure settings
    # fig.update_layout(title={'text': f"<b>{name}<b>", 'y':0.82, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 30})
    fig.update_layout(autosize=False, width=580, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # $\mathcal{R} \mathcal{A}_{\infty}^{21}$
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_game1v1(grid, V_2D, attackers, defenders, name):
    # fixed 1 defender 
    dims_plot = [0, 1]
    dim1, dim2 = dims_plot[0], dims_plot[1]
    complex_x = complex(0, grid.pts_each_dim[dim1])
    complex_y = complex(0, grid.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
    x_attackers = [a[0] for a in attackers]
    y_attackers = [a[1] for a in attackers]
    x_defenders = [d[0] for d in defenders]
    y_defenders = [d[1] for d in defenders]
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=V_2D.flatten(),
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
    # fig.add_shape(type='line', x0=-0.1, y0=-1.0, x1=-0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=-0.1, y0=-0.3, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # plot attackers
    fig.add_trace(go.Scatter(x=x_attackers, y=y_attackers, mode="markers", name='Attacker', marker=dict(symbol="triangle-up", size=10, color='red')))
    # for i in range(len(x_attackers)):
    #     fig.add_trace(go.Scatter(x=[x_attackers[i]], y=[y_attackers[i]], mode="markers", name=f'Attacker{i+1}', marker=dict(symbol="triangle-up", size=10, color='red')))
    # plot defenders
    fig.add_trace(go.Scatter(x=x_defenders, y=y_defenders, mode="markers", name='Fixed Defender', marker=dict(symbol="square", size=10, color='green')))
   
    # figure settings
    # fig.update_layout(title={'text': f"<b>{name}<b>", 'y':0.82, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 30})
    fig.update_layout(autosize=False, width=580, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # $\mathcal{R} \mathcal{A}_{\infty}^{21}$
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")


def plot_game0(grid, V_2D, attackers, defenders, name):
    # based on the plot_game but not showing legends 
    dims_plot = [0, 1]
    dim1, dim2 = dims_plot[0], dims_plot[1]
    complex_x = complex(0, grid.pts_each_dim[dim1])
    complex_y = complex(0, grid.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
    x_attackers = [a[0] for a in attackers]
    y_attackers = [a[1] for a in attackers]
    x_defenders = [d[0] for d in defenders]
    y_defenders = [d[1] for d in defenders]
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=V_2D.flatten(),
        zmin=0.0,
        ncontours=1,
        contours_coloring = 'none', # former: lines 
        line_width = 1.5,
        line_color = 'magenta',
        zmax=0.0,
    ), layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) #,paper_bgcolor='rgba(0,0,0,0)'
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0))
    fig.add_trace(go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', line=dict(color='purple')))
    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0))
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', line=dict(color='black')))
    # fig.add_shape(type='line', x0=-0.1, y0=-1.0, x1=-0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=-0.1, y0=-0.3, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # plot attackers
    fig.add_trace(go.Scatter(x=x_attackers, y=y_attackers, mode="markers", marker=dict(symbol="triangle-up", size=10, color='red')))
    # for i in range(len(x_attackers)):
    #     fig.add_trace(go.Scatter(x=[x_attackers[i]], y=[y_attackers[i]], mode="markers", name=f'Attacker{i+1}', marker=dict(symbol="triangle-up", size=10, color='red')))
    # plot defenders
    fig.add_trace(go.Scatter(x=x_defenders, y=y_defenders, mode="markers", marker=dict(symbol="square", size=10, color='blue')))
   
    # figure settings
    fig.update_layout(showlegend=False)
    # fig.update_layout(title={'text': f"<b>{name}<b>", 'y':0.82, 'x':0.5, 'xanchor': 'center','yanchor': 'top', 'font_size': 50})
    fig.update_layout(autosize=False, width=425, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0),  paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # $\mathcal{R} \mathcal{A}_{\infty}^{21}$
    # fig.update_layout(autosize=False, width=457.5, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_game2v1_2(grid, V_2D, attackers, defenders, name):
    # fixed the positions of 1 defender + attacker
    dims_plot = [0, 1]
    dim1, dim2 = dims_plot[0], dims_plot[1]
    complex_x = complex(0, grid.pts_each_dim[dim1])
    complex_y = complex(0, grid.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
    x_attackers = [a[0] for a in attackers]
    y_attackers = [a[1] for a in attackers]
    x_defenders = [d[0] for d in defenders]
    y_defenders = [d[1] for d in defenders]
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=V_2D.flatten(),
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
    # fig.add_shape(type='line', x0=-0.1, y0=-1.0, x1=-0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=-0.1, y0=-0.3, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # plot attackers
    fig.add_trace(go.Scatter(x=x_attackers, y=y_attackers, mode="markers", name='Fixed Attacker', marker=dict(symbol="triangle-up", size=10, color='green')))

    # for i in range(len(x_attackers)):
    #     fig.add_trace(go.Scatter(x=[x_attackers[i]], y=[y_attackers[i]], mode="markers", name=f'Attacker{i+1}', marker=dict(symbol="triangle-up", size=10, color='red')))
    # plot defenders
    fig.add_trace(go.Scatter(x=x_defenders, y=y_defenders, mode="markers", name='Defender', marker=dict(symbol="square", size=10, color='blue')))
   
    # figure settings
    # fig.update_layout(title={'text': f"<b>{name}<b>", 'y':0.82, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 30})
    fig.update_layout(autosize=False, width=580, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # $\mathcal{R} \mathcal{A}_{\infty}^{21}$
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")


def plot_game2v1_1(grid, V_2D, attackers, defenders, name):
    # fixed the positions of 1 defender + attacker
    dims_plot = [0, 1]
    dim1, dim2 = dims_plot[0], dims_plot[1]
    complex_x = complex(0, grid.pts_each_dim[dim1])
    complex_y = complex(0, grid.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
    x_attackers = [a[0] for a in attackers]
    y_attackers = [a[1] for a in attackers]
    x_defenders = [d[0] for d in defenders]
    y_defenders = [d[1] for d in defenders]
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=V_2D.flatten(),
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
    # fig.add_shape(type='line', x0=-0.1, y0=-1.0, x1=-0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=-0.1, y0=-0.3, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # plot attackers
    fig.add_trace(go.Scatter(x=[x_attackers[0]], y=[y_attackers[0]], mode="markers", name='Fixed Attacker', marker=dict(symbol="triangle-up", size=10, color='green')))
    fig.add_trace(go.Scatter(x=[x_attackers[1]], y=[y_attackers[1]], mode="markers", name='Attacker', marker=dict(symbol="triangle-up", size=10, color='red')))
    # for i in range(len(x_attackers)):
    #     fig.add_trace(go.Scatter(x=[x_attackers[i]], y=[y_attackers[i]], mode="markers", name=f'Attacker{i+1}', marker=dict(symbol="triangle-up", size=10, color='red')))
    # plot defenders
    fig.add_trace(go.Scatter(x=x_defenders, y=y_defenders, mode="markers", name='Fixed Defender', marker=dict(symbol="square", size=10, color='green')))
   
    # figure settings
    # fig.update_layout(title={'text': f"<b>{name}<b>", 'y':0.82, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 30})
    fig.update_layout(autosize=False, width=580, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # $\mathcal{R} \mathcal{A}_{\infty}^{21}$
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")


def plot_game1v2(grid, V_2D, attackers, defenders, name):
    # fixed the positions of 1 defender + attacker
    dims_plot = [0, 1]
    dim1, dim2 = dims_plot[0], dims_plot[1]
    complex_x = complex(0, grid.pts_each_dim[dim1])
    complex_y = complex(0, grid.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
    x_attackers = [a[0] for a in attackers]
    y_attackers = [a[1] for a in attackers]
    x_defenders = [d[0] for d in defenders]
    y_defenders = [d[1] for d in defenders]
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=V_2D.flatten(),
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
    # fig.add_shape(type='line', x0=-0.1, y0=-1.0, x1=-0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # fig.add_shape(type='line', x0=-0.1, y0=-0.3, x1=0.1, y1=-0.3, line=dict(color='black', width=2.0))
    # plot attackers
    fig.add_trace(go.Scatter(x=[x_attackers[0]], y=[y_attackers[0]], mode="markers", name='Free Attacker', marker=dict(symbol="triangle-up", size=10, color='green')))
    # fig.add_trace(go.Scatter(x=[x_attackers[1]], y=[y_attackers[1]], mode="markers", name='Attacker', marker=dict(symbol="triangle-up", size=10, color='red')))
    # for i in range(len(x_attackers)):
    #     fig.add_trace(go.Scatter(x=[x_attackers[i]], y=[y_attackers[i]], mode="markers", name=f'Attacker{i+1}', marker=dict(symbol="triangle-up", size=10, color='red')))
    # plot defenders
    # for j in range(len(x_defenders)):
    #     fig.add_trace(go.Scatter(x=[x_defenders[j]], y=[y_defenders[j]], mode="markers", name=f'Defender{j}', marker=dict(symbol="square", size=10, color='blue')))
    fig.add_trace(go.Scatter(x=[x_defenders[0]], y=[y_defenders[0]], mode="markers", name='Fixed Defender1', marker=dict(symbol="square", size=10, color='blue')))
    fig.add_trace(go.Scatter(x=[x_defenders[1]], y=[y_defenders[1]], mode="markers", name='Fixed Defender2', marker=dict(symbol="square", size=10, color='blue')))
    # figure settings
    # fig.update_layout(title={'text': f"<b>{name}<b>", 'y':0.82, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 30})
    fig.update_layout(autosize=False, width=580, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # $\mathcal{R} \mathcal{A}_{\infty}^{21}$
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_original(grid, V_2D):
    dims_plot = [0, 1]
    dim1, dim2 = dims_plot[0], dims_plot[1]
    complex_x = complex(0, grid.pts_each_dim[dim1])
    complex_y = complex(0, grid.pts_each_dim[dim2])
    mg_X, mg_Y = np.mgrid[grid.min[dim1]:grid.max[dim1]: complex_x, grid.min[dim2]:grid.max[dim2]: complex_y]
    print("Plotting beautiful 2D plots. Please wait\n")
    fig = go.Figure(data=go.Contour(
        x=mg_X.flatten(),
        y=mg_Y.flatten(),
        z=V_2D.flatten(),
        zmin=0.0,
        ncontours=1,
        zmax=0.0,
    ))
    fig.show()
    print("Please check the plot on your browser.")


def plot_simulation(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=2.5), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=2.5), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.5))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot attackers
    # fig.add_trace(go.Scatter(x=attackers_x[0], y=attackers_y[0], mode="lines+markers", name="Attacker", marker=dict(symbol="triangle-up", size=10, color='red')))

    for i in range(len(attackers_x)):
        fig.add_trace(go.Scatter(x=attackers_x[i], y=attackers_y[i], mode="markers", name=f"Attacker{i}", marker=dict(symbol="triangle-up", size=3, color='red'))) # symbol="cross"
    # plot defenders
    for j in range(len(defenders_x)):
        fig.add_trace(go.Scatter(x=defenders_x[j], y=defenders_y[j], mode="markers", name=f'Defender{j}', marker=dict(symbol="square", size=3, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=602.5, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=25)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

# plotting for simulations

def plot_simulation2v1_1(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[defenders_x[0][-1], attackers_x[1][-1]], y=[defenders_y[0][-1], attackers_y[1][-1]], mode="lines+markers", name="D1-A2", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[0][-1], y0=attackers_y[0][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))

    # figure settings
    # fig.update_layout(showlegend=False)  # to display the legends or not
    fig.update_layout(autosize=False, width=560, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Our method, t=0.475s<b>", 'y':0.85, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    # plot attackers
    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory


    # plot defenders
    for j in range(len(defenders_x)):
        dsparsex = defenders_x[j][0:-1:8]
        dsparsey = defenders_y[j][0:-1:8]
        dsparsex.append(defenders_x[j][-1])
        dsparsey.append(defenders_y[j][-1])
        fig.add_trace(go.Scatter(x=dsparsex, y=dsparsey, mode="markers", name=f'$D_{j+1}$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation2v1_2(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot attackers
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1], attackers_x[0][-1]], y=[defenders_y[0][-1], attackers_y[0][-1]], mode="lines+markers", name="D1-A1", marker=dict(symbol="cross", size=5, color='green')))

    # for i in range(len(attackers_x)):
    #     sparsex1 = attackers_x[i][0:-1:5]
    #     sparsey1 = attackers_y[i][0:-1:5]
    #     sparsex1.append(attackers_x[i][-1])
    #     sparsey1.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # plot attacker 0
    sparsex1 = attackers_x[0][0:-1:5]
    sparsey1 = attackers_y[0][0:-1:5]
    sparsex1.append(attackers_x[0][-1])
    sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    # plot attacker 1
    sparsex2 = [attackers_x[1][-1]]
    sparsey2 = [attackers_y[1][-1]]
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory

    # plot defenders
    for j in range(len(defenders_x)):
        dsparsex = defenders_x[j][95:-1:8]
        dsparsey = defenders_y[j][95:-1:8]
        dsparsex.append(defenders_x[j][-1])
        dsparsey.append(defenders_y[j][-1])
        fig.add_trace(go.Scatter(x=dsparsex, y=dsparsey, mode="markers", name=f'$D_{j+1}$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    # fig.update_layout(showlegend=False)  # to display the legends or not
    fig.update_layout(autosize=False, width=560, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.690s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation2v1_2s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # fig.add_trace(go.Scatter(x=[defenders_x[0][-1]], y=[defenders_y[0][-1]], mode="markers", name='Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"

    # plot captured + stop in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1]], y=[attackers_y[0][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1]], y=[defenders_y[0][-1]], mode="markers", name=f'Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # , symbol="square", size=4, color='blue'


    # plot attackers
    # fig.add_trace(go.Scatter(x=[defenders_x[0][-1], attackers_x[0][-1]], y=[defenders_y[0][-1], attackers_y[0][-1]], mode="lines+markers", name="D1-A1", marker=dict(symbol="cross", size=5, color='green')))

    # for i in range(len(attackers_x)):
    #     sparsex1 = attackers_x[i][0:-1:5]
    #     sparsey1 = attackers_y[i][0:-1:5]
    #     sparsex1.append(attackers_x[i][-1])
    #     sparsey1.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # figure settings
    # fig.update_layout(showlegend=False)  # to display the legends or not
    fig.update_layout(autosize=False, width=530, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Our method, t=0.785s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    
    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    # plot attacker 1
    sparsex2 = [attackers_x[1][-1]]
    sparsey2 = [attackers_y[1][-1]]
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory

    # plot defenders
    for j in range(len(defenders_x)):
        dsparsex = [defenders_x[j][-1]]
        dsparsey = [defenders_y[j][-1]]
        # dsparsex.append(defenders_x[j][-1])
        # dsparsey.append(defenders_y[j][-1])
        fig.add_trace(go.Scatter(x=dsparsex, y=dsparsey, mode="markers", name=f'$D_{j+1}$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # , symbol="square", size=4, color='blue'

    fig.show()
    print("Please check the plot on your browser.")


def animation_2v1(attackers_traj, defenders_traj, capture_status, T):
    # Just a movie with the agent's positions for now
    N = len(attackers_traj[0])
    num_attackers = len(attackers_traj)
    num_defenders = len(defenders_traj)

    attackers_traj = np.array(attackers_traj)
    defenders_traj = np.array(defenders_traj)

    attacker_x_list = [attackers_traj[i, :, 0] for i in range(num_attackers)]
    attacker_y_list = [attackers_traj[i, :, 1] for i in range(num_attackers)]
    defender_x_list = [defenders_traj[i, :, 0] for i in range(num_defenders)]
    defender_y_list = [defenders_traj[i, :, 1] for i in range(num_defenders)]

    # Make sure the length of all trajectories are the same
    # assert attacker_x_list[0].shape[0] == N
    # assert attacker_x_list[0].shape[0] == attacker_x_list[1].shape[0]
    # assert attacker_x_list[1].shape[0] == defender_x_list[0].shape[0]

    # First generate the frames
    frames= [] # All the frames
    for t in range(0, N):
        # Data for each frame
        # frame_data = []
        x_list = []
        y_list = []
        symbol_list = []
        color_list = []
        # Go through list defenders
        for i_d in range(num_defenders):
            # Display the trajectory for up to time t
            x_list.append(defender_x_list[i_d][t])
            y_list.append(defender_y_list[i_d][t])
            symbol_list += ["square"]
            color_list += ["blue"]

        # Go through list of attackers
        for i_a in range(num_attackers):
            x_list.append(attacker_x_list[i_a][t]) # Each agent trajectory is seperated by a NONE
            y_list.append(attacker_y_list[i_a][t])
            if capture_status[t][i_a]:
                symbol_list += ["cross-open"]
            else:
                symbol_list += ["triangle-up"]
            color_list += ["red"]
        # Generate a frame based on the characteristic of each agent
        frames.append(go.Frame(data=go.Scatter(x=x_list, y=y_list, mode="markers", name="Agents trajectory",
                                               marker=dict(symbol=symbol_list, size=4, color=color_list), showlegend=False)))

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
    # TODO: add the legends for agents and defenders

    # figure settings
    # fig.update_layout(showlegend=False)  # to display the legends or not
    fig.update_layout(autosize=False, width=560, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0),
                      title={'text': "<b>Our method, t={}s<b>".format(T), 'y':0.85, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()


def animation_MvsN(attacker_trajs, defender_trajs, capture_status, T):
    N = len(attackers_traj[0])
    num_attackers = len(attackers_traj)
    num_defenders = len(defenders_traj)

    attackers_traj = np.array(attackers_traj)
    defenders_traj = np.array(defenders_traj)

    attacker_x_list = [attackers_traj[i, :, 0] for i in range(num_attackers)]
    attacker_y_list = [attackers_traj[i, :, 1] for i in range(num_attackers)]
    defender_x_list = [defenders_traj[i, :, 0] for i in range(num_defenders)]
    defender_y_list = [defenders_traj[i, :, 1] for i in range(num_defenders)]

    # Make sure the length of all trajectories are the same
    # assert attacker_x_list[0].shape[0] == N
    # assert attacker_x_list[0].shape[0] == attacker_x_list[1].shape[0]
    # assert attacker_x_list[1].shape[0] == defender_x_list[0].shape[0]

    # First generate the frames
    frames= [] # All the frames
    for t in range(0, N):
        # Data for each frame
        # frame_data = []
        x_list = []
        y_list = []
        symbol_list = []
        color_list = []
        # Go through list defenders
        for i_d in range(num_defenders):
            # Display the trajectory for up to time t
            x_list.append(defender_x_list[i_d][t])
            y_list.append(defender_y_list[i_d][t])
            symbol_list += ["square"]
            color_list += ["blue"]

        # Go through list of attackers
        for i_a in range(num_attackers):
            x_list.append(attacker_x_list[i_a][t]) # Each agent trajectory is seperated by a NONE
            y_list.append(attacker_y_list[i_a][t])
            if capture_status[t][i_a]:
                symbol_list += ["cross-open"]
            else:
                symbol_list += ["triangle-up"]
            color_list += ["red"]
        # Generate a frame based on the characteristic of each agent
        frames.append(go.Frame(data=go.Scatter(x=x_list, y=y_list, mode="markers", name="Agents trajectory",
                                               marker=dict(symbol=symbol_list, size=4, color=color_list), showlegend=False)))

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
    # TODO: add the legends for agents and defenders

    # figure settings
    # fig.update_layout(showlegend=False)  # to display the legends or not
    fig.update_layout(autosize=False, width=560, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0),
                      title={'text': "<b>Our method, t={}s<b>".format(T), 'y':0.85, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()

def plot_simulation2v1_b1(attackers_x, attackers_y, defenders_x, defenders_y):  
    # for 2v1 baseline
    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP or Maximum Matching 
    # fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="Assigned D1", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1], attackers_x[0][-1]], y=[defenders_y[0][-1], attackers_y[0][-1]], mode="lines+markers", name="D1-A1", marker=dict(symbol="cross", size=5, color='green')))

    # plot attackers
    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # plot defenders
    for j in range(len(defenders_x)):
        dsparsex = defenders_x[j][0:-1:8]
        dsparsey = defenders_y[j][0:-1:8]
        dsparsex.append(defenders_x[j][-1])
        dsparsey.append(defenders_y[j][-1])
        fig.add_trace(go.Scatter(x=dsparsex, y=dsparsey, mode="markers", name=f'$D_{j+1}$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=525, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.530s<b>", 'y':0.85, 'x':0.4, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation2v1_b1s(attackers_x, attackers_y, defenders_x, defenders_y):  
    # for 2v1 baseline with the time 0.475
    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP or Maximum Matching 
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1], attackers_x[0][-1]], y=[defenders_y[0][-1], attackers_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[0][-1], y0=attackers_y[0][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))

    # figure settings
    fig.update_layout(autosize=False, width=560, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Baseline, t=0.475s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attackers
    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot defenders
    for j in range(len(defenders_x)):
        dsparsex = defenders_x[j][0:-1:8]
        dsparsey = defenders_y[j][0:-1:8]
        dsparsex.append(defenders_x[j][-1])
        dsparsey.append(defenders_y[j][-1])
        fig.add_trace(go.Scatter(x=dsparsex, y=dsparsey, mode="markers", name=f'$D_{j+1}$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")


def plot_simulation2v1_b2(attackers_x, attackers_y, defenders_x, defenders_y):  
    # for 2v1 baseline
    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP or Maximum Matching 
    # fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="Assigned D1", marker=dict(symbol="cross", size=5, color='green')))

    # # plot attackers
    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     # sparsex = [attackers_x[i][0], attackers_x[i][-1]]
    #     # sparsey = [attackers_y[i][0], attackers_y[i][-1]]
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1]], y=[attackers_y[0][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1]], y=[defenders_y[0][-1]], mode="markers", name='Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=530, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Baseline, t=0.785s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attacker 0
    sparsex1 =  [attackers_x[0][-1]]
    sparsey1 =  [attackers_y[0][-1]]
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory

    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5] 
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ arrived", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot defenders
    for j in range(len(defenders_x)):
        dsparsex = [defenders_x[j][-1]]
        dsparsey = [defenders_y[j][-1]]
        # dsparsex.append(defenders_x[j][-1])
        # dsparsey.append(defenders_y[j][-1])
        fig.add_trace(go.Scatter(x=dsparsex, y=dsparsey, mode="markers", name=f'$D_{j+1}$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")


# def plot_simulation_plot(attackers_x, attackers_y, defenders_x, defenders_y, t_slice, selected):

#     print("Plotting beautiful 2D plots. Please wait\n")

#     fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
#                     layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
#     # plot target
#     fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=2.5), name="Target")

#     # plot obstacles
#     fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=2.5), name="Obstacle")
#     fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.5))
#     fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
#     # plot selected
#     for j in range(len(defenders_x)):
#         if len(selected[j]): # not empty
#             xs = [attackers_x[n][-1] for n in range(len(selected[j]))].append(attackers_x[j][-1])
#             ys = [attackers_y[n][-1] for n in range(len(selected[j]))].append(defenders_y[j][-1])
#             fig.add_trace(go.Scatter(x = xs, y=ys, mode="lines+markers", name="Assigned", marker=dict(symbol="cross", size=2, color='magenta'))) 
#     # fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1], attackers_x[1][-1]], y=[attackers_y[0][-1], defenders_y[0][-1], attackers_y[1][-1]], mode="lines+markers", name="MIP", marker=dict(symbol="cross", size=2, color='magenta')))

#     for i in range(len(attackers_x)):
#         sparsex = attackers_x[i][t_slice:-1:5]
#         sparsey = attackers_y[i][t_slice:-1:5]
#         sparsex.append(attackers_x[i][-1])
#         sparsey.append(attackers_y[i][-1])
#         # sparsex = [attackers_x[i][0], attackers_x[i][-1]]
#         # sparsey = [attackers_y[i][0], attackers_y[i][-1]]
#         fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"A{i} traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
#         # fig.add_trace(go.Scatter(x=[attackers_x[i][-1]], y=[attackers_y[i][-1]], mode="markers+text", text=[f"A{i}"], textposition="top center", marker=dict(symbol="triangle-up", size=3, color='red')))
#     # plot defenders
#     for j in range(len(defenders_x)):
#         dsparsex = defenders_x[j][t_slice:-1:8]
#         dsparsey = defenders_y[j][t_slice:-1:8]
#         dsparsex.append(defenders_x[j][-1])
#         dsparsey.append(defenders_y[j][-1])
#         fig.add_trace(go.Scatter(x=dsparsex, y=dsparsey, mode="markers", name=f'D{j} traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

#     # figure settings
#     fig.update_layout(autosize=False, width=525, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
#     fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
#     fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
#     fig.show()
#     print("Please check the plot on your browser.")

def plot_simulation4v2_1(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=2.5), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=2.5), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.5))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot attackers
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1], attackers_x[1][-1]], y=[attackers_y[0][-1], defenders_y[0][-1], attackers_y[1][-1]], mode="lines+markers", name="Assigned D1", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[1][-1]], y=[attackers_y[2][-1], defenders_y[1][-1]], mode="lines+markers", name="Assigned D2", marker=dict(symbol="cross", size=5, color='green')))

    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        # sparsex = [attackers_x[i][0], attackers_x[i][-1]]
        # sparsey = [attackers_y[i][0], attackers_y[i][-1]]
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
        # fig.add_trace(go.Scatter(x=[attackers_x[i][-1]], y=[attackers_y[i][-1]], mode="markers+text", text=[f"A{i}"], textposition="top center", marker=dict(symbol="triangle-up", size=3, color='red')))
    # plot defenders
    for j in range(len(defenders_x)):
        dsparsex = defenders_x[j][0:-1:8]
        dsparsey = defenders_y[j][0:-1:8]
        dsparsex.append(defenders_x[j][-1])
        dsparsey.append(defenders_y[j][-1])
        fig.add_trace(go.Scatter(x=dsparsex, y=dsparsey, mode="markers", name=f'$D_{j+1}$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=525, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation4v2_2(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=2.5), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=2.5), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.5))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot attackers
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[0][-1], attackers_x[3][-1]], y=[attackers_y[1][-1], defenders_y[0][-1], attackers_y[3][-1]], mode="lines+markers", name="Assigned D1", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[defenders_x[1][-1], attackers_x[2][-1]], y=[defenders_y[1][-1], attackers_y[2][-1]], mode="lines+markers", name="Assigned D2", marker=dict(symbol="cross", size=5, color='green')))

    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        # sparsex = [attackers_x[i][0], attackers_x[i][-1]]
        # sparsey = [attackers_y[i][0], attackers_y[i][-1]]
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
        # fig.add_trace(go.Scatter(x=[attackers_x[i][-1]], y=[attackers_y[i][-1]], mode="markers+text", text=[f"A{i}"], textposition="top center", marker=dict(symbol="triangle-up", size=3, color='red')))
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][68:-1:8]
    d1sparsey = defenders_y[0][68:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"
    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=525, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation4v2_3(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=2.5), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=2.5), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.5))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot attackers
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[0][-1], attackers_x[2][-1]], y=[attackers_y[1][-1], defenders_y[0][-1], attackers_y[2][-1]], mode="lines+markers", name="Assigned D1", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[defenders_x[1][-1], attackers_x[2][-1]], y=[defenders_y[1][-1], attackers_y[2][-1]], mode="lines+markers", name="MIP1", marker=dict(symbol="cross", size=5, color='magenta')))

    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        # sparsex = [attackers_x[i][0], attackers_x[i][-1]]
        # sparsey = [attackers_y[i][0], attackers_y[i][-1]]
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
        # fig.add_trace(go.Scatter(x=[attackers_x[i][-1]], y=[attackers_y[i][-1]], mode="markers+text", text=[f"A{i}"], textposition="top center", marker=dict(symbol="triangle-up", size=3, color='red')))
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][111:-1:8]
    d1sparsey = defenders_y[0][111:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"
    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=525, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation4v2_4(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=2.5), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=2.5), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.5))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot attackers
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[0][-1]], y=[attackers_y[2][-1], defenders_y[0][-1]], mode="lines+markers", name="Assigned D1", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[defenders_x[1][-1], attackers_x[2][-1]], y=[defenders_y[1][-1], attackers_y[2][-1]], mode="lines+markers", name="MIP1", marker=dict(symbol="cross", size=5, color='magenta')))

    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        # sparsex = [attackers_x[i][0], attackers_x[i][-1]]
        # sparsey = [attackers_y[i][0], attackers_y[i][-1]]
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
        # fig.add_trace(go.Scatter(x=[attackers_x[i][-1]], y=[attackers_y[i][-1]], mode="markers+text", text=[f"A{i}"], textposition="top center", marker=dict(symbol="triangle-up", size=3, color='red')))
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][145:-1:8]
    d1sparsey = defenders_y[0][145:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"
    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=525, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation4v2_1b(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=2.5), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=2.5), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.5))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot Maximum Matched
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="Assigned D1", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[defenders_x[1][-1], attackers_x[2][-1]], y=[defenders_y[1][-1], attackers_y[2][-1]], mode="lines+markers", name="Assigned D2", marker=dict(symbol="cross", size=5, color='green')))

    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        # sparsex = [attackers_x[i][0], attackers_x[i][-1]]
        # sparsey = [attackers_y[i][0], attackers_y[i][-1]]
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
        # fig.add_trace(go.Scatter(x=[attackers_x[i][-1]], y=[attackers_y[i][-1]], mode="markers+text", text=[f"A{i}"], textposition="top center", marker=dict(symbol="triangle-up", size=3, color='red')))
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][0:-1:8]
    d1sparsey = defenders_y[0][0:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"
    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=525, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation4v2_2b(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=2.5), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=2.5), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=2.5))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot Maximum Matched
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[0][-1]], y=[attackers_y[2][-1], defenders_y[0][-1]], mode="lines+markers", name="Assigned D1", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[defenders_x[1][-1], attackers_x[2][-1]], y=[defenders_y[1][-1], attackers_y[2][-1]], mode="lines+markers", name="Assigned D2", marker=dict(symbol="cross", size=5, color='magenta')))

    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        # sparsex = [attackers_x[i][0], attackers_x[i][-1]]
        # sparsey = [attackers_y[i][0], attackers_y[i][-1]]
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
        # fig.add_trace(go.Scatter(x=[attackers_x[i][-1]], y=[attackers_y[i][-1]], mode="markers+text", text=[f"A{i}"], textposition="top center", marker=dict(symbol="triangle-up", size=3, color='red')))
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][40:-1:8]
    d1sparsey = defenders_y[0][40:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"
    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=525, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=20)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_1(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    # fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1], attackers_x[1][-1]], y=[attackers_y[0][-1], defenders_y[0][-1], attackers_y[1][-1]], mode="lines+markers", name="Assigned D1", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[1][-1], attackers_x[4][-1]], y=[attackers_y[2][-1], defenders_y[1][-1], attackers_y[4][-1]], mode="lines+markers", name="Assigned D2", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A1", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[0][-1]], y=[attackers_y[1][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A2", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[1][-1]], y=[attackers_y[2][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A3", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[4][-1], defenders_x[1][-1]], y=[attackers_y[4][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A5", marker=dict(symbol="cross", size=5, color='green')))

    # plot attackers
    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][0:-1:8]
    d1sparsey = defenders_y[0][0:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=475, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.120s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_1s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[0][-1], y0=attackers_y[0][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[4][-1], y0=attackers_y[4][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Our method, t=0.1s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    
    # plot attackers
    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][0:-1:8]
    d1sparsey = defenders_y[0][0:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_2s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[0][-1]], y=[attackers_y[1][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[3][-1], y0=attackers_y[3][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))

    # plot obstacle mark in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[4][-1]], y=[attackers_y[4][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory


    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Our method, t=0.3s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    
    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1]]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 5
    sparsex6 = attackers_x[5][0:-1:5]
    sparsey6 = attackers_y[5][0:-1:5]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][20:-1:8]
    d1sparsey = defenders_y[0][20:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = defenders_x[1][20:-1:8]
    d2sparsey = defenders_y[1][20:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_2(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A1", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1], attackers_x[3][-1]], y=[defenders_y[0][-1], attackers_y[3][-1]], mode="lines+markers", name="D1-A4", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[1][-1]], y=[attackers_y[2][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A3", marker=dict(symbol="cross", size=5, color='green')))

    # plot attackers
    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 0
    sparsex1 = attackers_x[0][0:-1:5]
    sparsey1 = attackers_y[0][0:-1:5]
    sparsex1.append(attackers_x[0][-1])
    sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1]]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 5
    sparsex6 = attackers_x[5][0:-1:5]
    sparsey6 = attackers_y[5][0:-1:5]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][0:-1:8]
    d1sparsey = defenders_y[0][0:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    d2sparsex = defenders_x[1][24:-1:8]
    d2sparsey = defenders_y[1][24:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.280s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_3(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[0][-1]], y=[attackers_y[1][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A2", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1], attackers_x[3][-1]], y=[defenders_y[0][-1], attackers_y[3][-1]], mode="lines+markers", name="D1-A4", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[1][-1]], y=[attackers_y[2][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A3", marker=dict(symbol="cross", size=5, color='green')))

    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1]]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 5
    sparsex6 = attackers_x[5][0:-1:5]
    sparsey6 = attackers_y[5][0:-1:5]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][56:-1:8]
    d1sparsey = defenders_y[0][56:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    d2sparsex = defenders_x[1][24:-1:8]
    d2sparsey = defenders_y[1][24:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.460s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_4(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP resutls
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[0][-1]], y=[attackers_y[1][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A2", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[5][-1], defenders_x[0][-1]], y=[attackers_y[5][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A6", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[1][-1]], y=[attackers_y[2][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A3", marker=dict(symbol="cross", size=5, color='green')))

    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 3
    sparsex4 = [attackers_x[3][-1]]
    sparsey4 = [attackers_y[3][-1]]
    # sparsex4.append(attackers_x[3][-1])
    # sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1]]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 5
    sparsex6 = attackers_x[5][0:-1:5]
    sparsey6 = attackers_y[5][0:-1:5]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][92:-1:8]
    d1sparsey = defenders_y[0][92:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    d2sparsex = defenders_x[1][24:-1:8]
    d2sparsey = defenders_y[1][24:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.525s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_5(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[0][-1]], y=[attackers_y[1][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))

    # plot captured + stop in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[3][-1]], y=[attackers_y[3][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[defenders_x[1][-1]], y=[defenders_y[1][-1]], mode="markers", name='Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"


    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Our method, t=0.7s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = [attackers_x[3][-1]]
    sparsey4 = [attackers_y[3][-1]]
    # sparsex4.append(attackers_x[3][-1])
    # sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1]]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 5
    sparsex6 = [attackers_x[5][-1]]
    sparsey6 = [attackers_y[5][-1]]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][60:-1:8]
    d1sparsey = defenders_y[0][60:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = [defenders_x[1][-1]]
    d2sparsey = [defenders_y[1][-1]]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_6(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[0][-1]], y=[attackers_y[2][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A3", marker=dict(symbol="cross", size=5, color='green')))


    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 1
    sparsex2 = [attackers_x[1][-1]]
    sparsey2 = [attackers_y[1][-1]]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 3
    sparsex4 = [attackers_x[3][-1]]
    sparsey4 = [attackers_y[3][-1]]
    # sparsex4.append(attackers_x[3][-1])
    # sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1]]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 5
    sparsex6 = [attackers_x[5][-1]]
    sparsey6 = [attackers_y[5][-1]]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][140:-1:8]
    d1sparsey = defenders_y[0][140:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    d2sparsex = [defenders_x[1][-1]]
    d2sparsey = [defenders_y[1][-1]]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ stopped', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.955s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_4s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot captured + stop in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1]], y=[attackers_y[0][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1]], y=[defenders_y[0][-1]], mode="markers", name='Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"

    # plot MIP results
    # fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[0][-1]], y=[attackers_y[2][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A3", marker=dict(symbol="cross", size=5, color='green')))

    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # figure settings
    fig.update_layout(autosize=False, width=483, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Our method, t=1.0s<b>", 'y':0.85, 'x':0.438, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = [attackers_x[1][-1]]
    sparsey2 = [attackers_y[1][-1]]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = [attackers_x[2][-1]]
    sparsey3 = [attackers_y[2][-1]]
    # sparsex3.append(attackers_x[2][-1])
    # sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = [attackers_x[3][-1]]
    sparsey4 = [attackers_y[3][-1]]
    # sparsex4.append(attackers_x[3][-1])
    # sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1]]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 5
    sparsex6 = [attackers_x[5][-1]]
    sparsey6 = [attackers_y[5][-1]]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = [defenders_x[0][-1]]
    d1sparsey = [defenders_y[0][-1]]
    # d1sparsex.append(defenders_x[0][-1])
    # d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = [defenders_x[1][-1]]
    d2sparsey = [defenders_y[1][-1]]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_b1(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[0][-1]], y=[attackers_y[1][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A2", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[1][-1]], y=[attackers_y[0][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A1", marker=dict(symbol="cross", size=5, color='green')))


    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # plot attacker 0
    sparsex1 = attackers_x[0][0:-1:5]
    sparsey1 = attackers_y[0][0:-1:5]
    sparsex1.append(attackers_x[0][-1])
    sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 4
    sparsex5 = attackers_x[4][0:-1:5] 
    sparsey5 = attackers_y[4][0:-1:5] 
    sparsex5.append(attackers_x[4][-1])
    sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = attackers_x[5][0:-1:5]
    sparsey6 = attackers_y[5][0:-1:5]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][0:-1:8]
    d1sparsey = defenders_y[0][0:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=475, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.285s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_b1s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[0][-1]], y=[attackers_y[1][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[0][-1], y0=attackers_y[0][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Baseline, t=0.1s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attacker 0
    sparsex1 = attackers_x[0][0:-1:5]
    sparsey1 = attackers_y[0][0:-1:5]
    sparsex1.append(attackers_x[0][-1])
    sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = attackers_x[4][0:-1:5] 
    sparsey5 = attackers_y[4][0:-1:5] 
    sparsex5.append(attackers_x[4][-1])
    sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = attackers_x[5][0:-1:5]
    sparsey6 = attackers_y[5][0:-1:5]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][0:-1:8]
    d1sparsey = defenders_y[0][0:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_b2s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[0][-1]], y=[attackers_y[2][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[0][-1], y0=attackers_y[0][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))

    # plot captured in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1]], y=[attackers_y[1][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Baseline, t=0.3s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attacker 0
    sparsex1 = attackers_x[0][0:-1:5]
    sparsey1 = attackers_y[0][0:-1:5]
    sparsex1.append(attackers_x[0][-1])
    sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = [attackers_x[1][-1]]
    sparsey2 = [attackers_y[1][-1]]
    # sparsex2.append(attackers_x[1][-1])
    # sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = attackers_x[4][0:-1:5] 
    sparsey5 = attackers_y[4][0:-1:5] 
    sparsex5.append(attackers_x[4][-1])
    sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = attackers_x[5][0:-1:5]
    sparsey6 = attackers_y[5][0:-1:5]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][20:-1:8]
    d1sparsey = defenders_y[0][20:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = defenders_x[1][20:-1:8]
    d2sparsey = defenders_y[1][20:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_b2(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[0][-1]], y=[attackers_y[2][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A3", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[1][-1]], y=[attackers_y[0][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A1", marker=dict(symbol="cross", size=5, color='green')))

    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
   # plot attacker 0
    sparsex1 = attackers_x[0][0:-1:5]
    sparsey1 = attackers_y[0][0:-1:5]
    sparsex1.append(attackers_x[0][-1])
    sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 1
    sparsex2 = [attackers_x[1][-1]]
    sparsey2 = [attackers_y[1][-1]]
    # sparsex2.append(attackers_x[1][-1])
    # sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1] ]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ arrived", marker=dict(symbol="triangle-up", size=8, color='red'))) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = [attackers_x[5][-1]]
    sparsey6 = [attackers_y[5][-1]]
    # sparsex6.append(attackers_x[5][-1])
    # sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ arrived", marker=dict(symbol="triangle-up", size=8, color='red'))) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][57:-1:8]
    d1sparsey = defenders_y[0][57:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.665s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_b3(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot Maximum Matched
    fig.add_trace(go.Scatter(x=[attackers_x[3][-1], defenders_x[0][-1]], y=[attackers_y[3][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A4", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[1][-1]], y=[attackers_y[0][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A1", marker=dict(symbol="cross", size=5, color='green')))

    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # plot attacker 0
    sparsex1 = attackers_x[0][0:-1:5]
    sparsey1 = attackers_y[0][0:-1:5]
    sparsex1.append(attackers_x[0][-1])
    sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 1
    sparsex2 = [attackers_x[1][-1]]
    sparsey2 = [attackers_y[1][-1]]
    # sparsex2.append(attackers_x[1][-1])
    # sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 2
    sparsex3 = [attackers_x[2][-1]]
    sparsey3 = [attackers_y[2][-1]]
    # sparsex3.append(attackers_x[2][-1])
    # sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1] ]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ arrived", marker=dict(symbol="triangle-up", size=8, color='red'))) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = [attackers_x[5][-1]]
    sparsey6 = [attackers_y[5][-1]]
    # sparsex6.append(attackers_x[5][-1])
    # sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ arrived", marker=dict(symbol="triangle-up", size=8, color='red'))) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][133:-1:8]
    d1sparsey = defenders_y[0][133:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.750s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_b3s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot Maximum Matched
    fig.add_trace(go.Scatter(x=[attackers_x[3][-1], defenders_x[0][-1]], y=[attackers_y[3][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[3][-1], y0=attackers_y[3][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[0][-1], y0=attackers_y[0][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))

    # plot captured in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[2][-1]], y=[attackers_y[2][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Baseline, t=0.7s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attacker 0
    sparsex1 = attackers_x[0][0:-1:5]
    sparsey1 = attackers_y[0][0:-1:5]
    sparsex1.append(attackers_x[0][-1])
    sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = [attackers_x[1][-1]]
    sparsey2 = [attackers_y[1][-1]]
    # sparsex2.append(attackers_x[1][-1])
    # sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = [attackers_x[2][-1]]
    sparsey3 = [attackers_y[2][-1]]
    # sparsex3.append(attackers_x[2][-1])
    # sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1] ]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ arrived", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = [attackers_x[5][-1]]
    sparsey6 = [attackers_y[5][-1]]
    # sparsex6.append(attackers_x[5][-1])
    # sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ arrived", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][120:-1:8]
    d1sparsey = defenders_y[0][120:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = defenders_x[1][120:-1:8]
    d2sparsey = defenders_y[1][120:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_b4(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot Maximum Matched
    fig.add_trace(go.Scatter(x=[attackers_x[3][-1], defenders_x[0][-1]], y=[attackers_y[3][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A4", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[1][-1]], y=[attackers_y[0][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A1", marker=dict(symbol="cross", size=5, color='green')))

    # for i in range(len(attackers_x)):
    #     sparsex = attackers_x[i][0:-1:5]
    #     sparsey = attackers_y[i][0:-1:5]
    #     sparsex.append(attackers_x[i][-1])
    #     sparsey.append(attackers_y[i][-1])
    #     fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory

    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 1
    sparsex2 = [attackers_x[1][-1]]
    sparsey2 = [attackers_y[1][-1]]
    # sparsex2.append(attackers_x[1][-1])
    # sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 2
    sparsex3 = [attackers_x[2][-1]]
    sparsey3 = [attackers_y[2][-1]]
    # sparsex3.append(attackers_x[2][-1])
    # sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'))) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1] ]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ arrived", marker=dict(symbol="triangle-up", size=8, color='red'))) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = [attackers_x[5][-1]]
    sparsey6 = [attackers_y[5][-1]]
    # sparsex6.append(attackers_x[5][-1])
    # sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ arrived", marker=dict(symbol="triangle-up", size=8, color='red'))) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][133:-1:8]
    d1sparsey = defenders_y[0][133:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'))) # symbol="star"

    d2sparsex = [defenders_x[1][-1]]
    d2sparsey = [defenders_y[1][-1]]
    # d2sparsex.append(defenders_x[1][-1])
    # d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ stopped', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.850s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation6v2_b4s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot Maximum Matched
    # fig.add_trace(go.Scatter(x=[attackers_x[3][-1], defenders_x[0][-1]], y=[attackers_y[3][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A4", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[1][-1]], y=[attackers_y[0][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A1", marker=dict(symbol="cross", size=5, color='green')))

    # plot captured + stop in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1]], y=[attackers_y[0][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1]], y=[defenders_y[0][-1]], mode="markers", name='Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=483, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Baseline, t=1.0s<b>", 'y':0.85, 'x':0.438, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = [attackers_x[1][-1]]
    sparsey2 = [attackers_y[1][-1]]
    # sparsex2.append(attackers_x[1][-1])
    # sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = [attackers_x[2][-1]]
    sparsey3 = [attackers_y[2][-1]]
    # sparsex3.append(attackers_x[2][-1])
    # sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = [attackers_x[3][-1]]
    sparsey4 = [attackers_y[3][-1]]
    # sparsex4.append(attackers_x[3][-1])
    # sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1] ]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ arrived", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = [attackers_x[5][-1]]
    sparsey6 = [attackers_y[5][-1]]
    # sparsex6.append(attackers_x[5][-1])
    # sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ arrived", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = [defenders_x[0][-1]]
    d1sparsey = [defenders_y[0][-1]]
    # d1sparsex.append(defenders_x[0][-1])
    # d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = [defenders_x[1][-1]]
    d2sparsey = [defenders_y[1][-1]]
    # d2sparsex.append(defenders_x[1][-1])
    # d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation8v4_1(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_shape(type="line", x0=attackers_x[0][-1], y0=attackers_y[0][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[7][-1], y0=attackers_y[7][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[3][-1], y0=attackers_y[3][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[6][-1], y0=attackers_y[6][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[4][-1], y0=attackers_y[4][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[5][-1], y0=attackers_y[5][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))

    # fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A1", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[7][-1], defenders_x[0][-1]], y=[attackers_y[7][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A8", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[3][-1], defenders_x[1][-1]], y=[attackers_y[3][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A4", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[6][-1], defenders_x[1][-1]], y=[attackers_y[6][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A7", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[2][-1]], y=[attackers_y[1][-1], defenders_y[2][-1]], mode="lines+markers", name="D3-A2", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[2][-1]], y=[attackers_y[2][-1], defenders_y[2][-1]], mode="lines+markers", name="D3-A3", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[4][-1], defenders_x[3][-1]], y=[attackers_y[4][-1], defenders_y[3][-1]], mode="lines+markers", name="D4-A5", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[5][-1], defenders_x[3][-1]], y=[attackers_y[5][-1], defenders_y[3][-1]], mode="lines+markers", name="D4-A6", marker=dict(symbol="cross", size=5, color='green')))

    # plot attackers
    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$", marker=dict(symbol="triangle-up", size=8, color='red'))) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][0:-1:8]
    d1sparsey = defenders_y[0][0:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$', marker=dict(symbol="square", size=8, color='blue'))) # symbol="star"

    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$', marker=dict(symbol="square", size=8, color='blue'))) # symbol="star"

    d3sparsex = defenders_x[2][0:-1:8]
    d3sparsey = defenders_y[2][0:-1:8]
    d3sparsex.append(defenders_x[2][-1])
    d3sparsey.append(defenders_y[2][-1])
    fig.add_trace(go.Scatter(x=d3sparsex, y=d3sparsey, mode="markers", name='$D_3$', marker=dict(symbol="square", size=8, color='blue'))) # symbol="star"

    d4sparsex = defenders_x[3][0:-1:8]
    d4sparsey = defenders_y[3][0:-1:8]
    d4sparsex.append(defenders_x[3][-1])
    d4sparsey.append(defenders_y[3][-1])
    fig.add_trace(go.Scatter(x=d4sparsex, y=d4sparsey, mode="markers", name='$D_4$', marker=dict(symbol="square", size=8, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.000s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation8v4_1s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[0][-1], y0=attackers_y[0][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[7][-1], y0=attackers_y[7][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[3][-1], y0=attackers_y[3][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[6][-1], y0=attackers_y[6][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[4][-1], y0=attackers_y[4][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[5][-1], y0=attackers_y[5][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Our method, t=0.1s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attackers
    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][0:-1:8]
    d1sparsey = defenders_y[0][0:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d3sparsex = defenders_x[2][0:-1:8]
    d3sparsey = defenders_y[2][0:-1:8]
    d3sparsex.append(defenders_x[2][-1])
    d3sparsey.append(defenders_y[2][-1])
    fig.add_trace(go.Scatter(x=d3sparsex, y=d3sparsey, mode="markers", name='$D_3$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d4sparsex = defenders_x[3][0:-1:8]
    d4sparsey = defenders_y[3][0:-1:8]
    d4sparsex.append(defenders_x[3][-1])
    d4sparsey.append(defenders_y[3][-1])
    fig.add_trace(go.Scatter(x=d4sparsex, y=d4sparsey, mode="markers", name='$D_4$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation8v4_2s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[5][-1], defenders_x[0][-1]], y=[attackers_y[5][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[5][-1], y0=attackers_y[5][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[6][-1], y0=attackers_y[6][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[3][-1], y0=attackers_y[3][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    # fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    # fig.add_shape(type="line", x0=attackers_x[4][-1], y0=attackers_y[4][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    # fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))
    # fig.add_shape(type="line", x0=attackers_x[5][-1], y0=attackers_y[5][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))

    # plot captured + stop in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1]], y=[attackers_y[0][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[defenders_x[2][-1]], y=[defenders_y[2][-1]], mode="markers", name='Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"


    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Our method, t=0.5s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attackers
    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = [attackers_x[2][-1]]
    sparsey3 = [attackers_y[2][-1]]
    # sparsex3.append(attackers_x[2][-1])
    # sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = attackers_x[3][0:-1:5]
    sparsey4 = attackers_y[3][0:-1:5]
    sparsex4.append(attackers_x[3][-1])
    sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1]]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = attackers_x[5][0:-1:5]
    sparsey6 = attackers_y[5][0:-1:5]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot attacker 6
    sparsex7 = attackers_x[6][0:-1:5] 
    sparsey7 = attackers_y[6][0:-1:5] 
    sparsex7.append(attackers_x[6][-1])
    sparsey7.append(attackers_y[6][-1])
    fig.add_trace(go.Scatter(x=sparsex7, y=sparsey7, mode="markers", name=f"$A_{7}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 7
    sparsex8 = [attackers_x[7][-1]]
    sparsey8 = [attackers_y[7][-1]]
    # sparsex8.append(attackers_x[7][-1])
    # sparsey8.append(attackers_y[7][-1])
    fig.add_trace(go.Scatter(x=sparsex8, y=sparsey8, mode="markers", name=f"$A_{8}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][90:-1:8]
    d1sparsey = defenders_y[0][90:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = defenders_x[1][90:-1:8]
    d2sparsey = defenders_y[1][90:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d3sparsex = [defenders_x[2][-1]]
    d3sparsey = [defenders_y[2][-1]]
    # d3sparsex.append(defenders_x[2][-1])
    # d3sparsey.append(defenders_y[2][-1])
    fig.add_trace(go.Scatter(x=d3sparsex, y=d3sparsey, mode="markers", name='$D_3$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d4sparsex = [defenders_x[3][-1]]
    d4sparsey = [defenders_y[3][-1]]
    # d4sparsex.append(defenders_x[3][-1])
    # d4sparsey.append(defenders_y[3][-1])
    fig.add_trace(go.Scatter(x=d4sparsex, y=d4sparsey, mode="markers", name='$D_4$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation8v4_3s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[3][-1]], y=[attackers_y[1][-1], defenders_y[3][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))
    # fig.add_shape(type="line", x0=attackers_x[6][-1], y0=attackers_y[6][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    # fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    # fig.add_shape(type="line", x0=attackers_x[3][-1], y0=attackers_y[3][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    # # fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    # fig.add_shape(type="line", x0=attackers_x[4][-1], y0=attackers_y[4][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    # fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))
    # fig.add_shape(type="line", x0=attackers_x[5][-1], y0=attackers_y[5][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))

    # plot captured + stop in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1]], y=[attackers_y[0][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1]], y=[defenders_y[0][-1]], mode="markers", name='Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Our method, t=1.0s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attackers
    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = [attackers_x[2][-1]]
    sparsey3 = [attackers_y[2][-1]]
    # sparsex3.append(attackers_x[2][-1])
    # sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = [attackers_x[3][-1]]
    sparsey4 = [attackers_y[3][-1]]
    # sparsex4.append(attackers_x[3][-1])
    # sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1]]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = [attackers_x[5][-1]]
    sparsey6 = [attackers_y[5][-1]]
    # sparsex6.append(attackers_x[5][-1])
    # sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory

    # plot attacker 6
    sparsex7 = [attackers_x[6][-1]]
    sparsey7 = [attackers_y[6][-1]]
    # sparsex7.append(attackers_x[6][-1])
    # sparsey7.append(attackers_y[6][-1])
    fig.add_trace(go.Scatter(x=sparsex7, y=sparsey7, mode="markers", name=f"$A_{7}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 7
    sparsex8 = [attackers_x[7][-1]]
    sparsey8 = [attackers_y[7][-1]]
    # sparsex8.append(attackers_x[7][-1])
    # sparsey8.append(attackers_y[7][-1])
    fig.add_trace(go.Scatter(x=sparsex8, y=sparsey8, mode="markers", name=f"$A_{8}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = [defenders_x[0][-1]]
    d1sparsey = [defenders_y[0][-1]]
    # d1sparsex.append(defenders_x[0][-1])
    # d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = [defenders_x[1][-1]]
    d2sparsey = [defenders_y[1][-1]]
    # d2sparsex.append(defenders_x[1][-1])
    # d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d3sparsex = [defenders_x[2][-1]]
    d3sparsey = [defenders_y[2][-1]]
    # d3sparsex.append(defenders_x[2][-1])
    # d3sparsey.append(defenders_y[2][-1])
    fig.add_trace(go.Scatter(x=d3sparsex, y=d3sparsey, mode="markers", name='$D_3$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d4sparsex = defenders_x[3][100:-1:8]
    d4sparsey = defenders_y[3][100:-1:8]
    d4sparsex.append(defenders_x[3][-1])
    d4sparsey.append(defenders_y[3][-1])
    fig.add_trace(go.Scatter(x=d4sparsex, y=d4sparsey, mode="markers", name='$D_4$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation8v4_2(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    # fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A1", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[7][-1], defenders_x[0][-1]], y=[attackers_y[7][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A8", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[3][-1], defenders_x[1][-1]], y=[attackers_y[3][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A4", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[6][-1], defenders_x[1][-1]], y=[attackers_y[6][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A7", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[2][-1]], y=[attackers_y[1][-1], defenders_y[2][-1]], mode="lines+markers", name="D3-A2", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[2][-1]], y=[attackers_y[2][-1], defenders_y[2][-1]], mode="lines+markers", name="D3-A3", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[4][-1], defenders_x[3][-1]], y=[attackers_y[4][-1], defenders_y[3][-1]], mode="lines+markers", name="D4-A5", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[5][-1], defenders_x[3][-1]], y=[attackers_y[5][-1], defenders_y[3][-1]], mode="lines+markers", name="D4-A6", marker=dict(symbol="cross", size=5, color='green')))

    # plot captured + stop in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1]], y=[attackers_y[0][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[defenders_x[0][-1]], y=[defenders_y[0][-1]], mode="markers", name='Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=483, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Our method, t=1.5s<b>", 'y':0.85, 'x':0.438, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attackers
    for i in range(len(attackers_x)):
        sparsex = [attackers_x[i][-1]]
        sparsey = [attackers_y[i][-1]]
        # sparsex.append(attackers_x[i][-1])
        # sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = [defenders_x[0][-1]]
    d1sparsey = [defenders_y[0][-1]]
    # d1sparsex.append(defenders_x[0][-1])
    # d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = [defenders_x[1][-1]]
    d2sparsey = [defenders_y[1][-1]]
    # d2sparsex.append(defenders_x[1][-1])
    # d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d3sparsex = [defenders_x[2][-1]]
    d3sparsey = [defenders_y[2][-1]]
    # d3sparsex.append(defenders_x[2][-1])
    # d3sparsey.append(defenders_y[2][-1])
    fig.add_trace(go.Scatter(x=d3sparsex, y=d3sparsey, mode="markers", name='$D_3$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d4sparsex = [defenders_x[3][-1]]
    d4sparsey = [defenders_y[3][-1]]
    # d4sparsex.append(defenders_x[3][-1])
    # d4sparsey.append(defenders_y[3][-1])
    fig.add_trace(go.Scatter(x=d4sparsex, y=d4sparsey, mode="markers", name='$D_4$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation8v4_b1(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_shape(type="line", x0=attackers_x[0][-1], y0=attackers_y[0][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[3][-1], y0=attackers_y[3][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))

    # fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A1", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[3][-1], defenders_x[1][-1]], y=[attackers_y[3][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A4", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[2][-1]], y=[attackers_y[2][-1], defenders_y[2][-1]], mode="lines+markers", name="D3-A3", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[3][-1]], y=[attackers_y[1][-1], defenders_y[3][-1]], mode="lines+markers", name="D4-A2", marker=dict(symbol="cross", size=5, color='green')))


    # plot attackers
    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$", marker=dict(symbol="triangle-up", size=8, color='red'))) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][0:-1:8]
    d1sparsey = defenders_y[0][0:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$', marker=dict(symbol="square", size=8, color='blue'))) # symbol="star"

    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$', marker=dict(symbol="square", size=8, color='blue'))) # symbol="star"

    d3sparsex = defenders_x[2][0:-1:8]
    d3sparsey = defenders_y[2][0:-1:8]
    d3sparsex.append(defenders_x[2][-1])
    d3sparsey.append(defenders_y[2][-1])
    fig.add_trace(go.Scatter(x=d3sparsex, y=d3sparsey, mode="markers", name='$D_3$', marker=dict(symbol="square", size=8, color='blue'))) # symbol="star"

    d4sparsex = defenders_x[3][0:-1:8]
    d4sparsey = defenders_y[3][0:-1:8]
    d4sparsex.append(defenders_x[3][-1])
    d4sparsey.append(defenders_y[3][-1])
    fig.add_trace(go.Scatter(x=d4sparsex, y=d4sparsey, mode="markers", name='$D_4$', marker=dict(symbol="square", size=8, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>t=0.000s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation8v4_b1s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[0][-1], y0=attackers_y[0][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[3][-1], y0=attackers_y[3][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))

    # fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A1", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[3][-1], defenders_x[1][-1]], y=[attackers_y[3][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A4", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[2][-1]], y=[attackers_y[2][-1], defenders_y[2][-1]], mode="lines+markers", name="D3-A3", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[3][-1]], y=[attackers_y[1][-1], defenders_y[3][-1]], mode="lines+markers", name="D4-A2", marker=dict(symbol="cross", size=5, color='green')))

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Baseline, t=0.1s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,
    
    # plot attackers
    for i in range(len(attackers_x)):
        sparsex = attackers_x[i][0:-1:5]
        sparsey = attackers_y[i][0:-1:5]
        sparsex.append(attackers_x[i][-1])
        sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][0:-1:8]
    d1sparsey = defenders_y[0][0:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = defenders_x[1][0:-1:8]
    d2sparsey = defenders_y[1][0:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d3sparsex = defenders_x[2][0:-1:8]
    d3sparsey = defenders_y[2][0:-1:8]
    d3sparsex.append(defenders_x[2][-1])
    d3sparsey.append(defenders_y[2][-1])
    fig.add_trace(go.Scatter(x=d3sparsex, y=d3sparsey, mode="markers", name='$D_3$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d4sparsex = defenders_x[3][0:-1:8]
    d4sparsey = defenders_y[3][0:-1:8]
    d4sparsex.append(defenders_x[3][-1])
    d4sparsey.append(defenders_y[3][-1])
    fig.add_trace(go.Scatter(x=d4sparsex, y=d4sparsey, mode="markers", name='$D_4$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation8v4_b2s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[5][-1], defenders_x[0][-1]], y=[attackers_y[5][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[5][-1], y0=attackers_y[5][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[4][-1], y0=attackers_y[4][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[2][-1], y0=attackers_y[2][-1], x1=defenders_x[2][-1], y1=defenders_y[2][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[3][-1], y1=defenders_y[3][-1], line=dict(color="green",width=2))

    # plot captured in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1]], y=[attackers_y[0][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Baseline, t=0.5s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attackers
    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = attackers_x[2][0:-1:5]
    sparsey3 = attackers_y[2][0:-1:5]
    sparsex3.append(attackers_x[2][-1])
    sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = [attackers_x[3][-1]]
    sparsey4 = [attackers_y[3][-1]]
    # sparsex4.append(attackers_x[3][-1])
    # sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = attackers_x[4][0:-1:5]
    sparsey5 = attackers_y[4][0:-1:5]
    sparsex5.append(attackers_x[4][-1])
    sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = attackers_x[5][0:-1:5]
    sparsey6 = attackers_y[5][0:-1:5]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot attacker 6
    sparsex7 = attackers_x[6][0:-1:5] 
    sparsey7 = attackers_y[6][0:-1:5] 
    sparsex7.append(attackers_x[6][-1])
    sparsey7.append(attackers_y[6][-1])
    fig.add_trace(go.Scatter(x=sparsex7, y=sparsey7, mode="markers", name=f"$A_{7}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 7
    sparsex8 = attackers_x[7][0:-1:5]
    sparsey8 = attackers_y[7][0:-1:5]
    sparsex8.append(attackers_x[7][-1])
    sparsey8.append(attackers_y[7][-1])
    fig.add_trace(go.Scatter(x=sparsex8, y=sparsey8, mode="markers", name=f"$A_{8}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][50:-1:8]
    d1sparsey = defenders_y[0][50:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = defenders_x[1][50:-1:8]
    d2sparsey = defenders_y[1][50:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d3sparsex = defenders_x[2][50:-1:8]
    d3sparsey = defenders_y[2][50:-1:8]
    d3sparsex.append(defenders_x[2][-1])
    d3sparsey.append(defenders_y[2][-1])
    fig.add_trace(go.Scatter(x=d3sparsex, y=d3sparsey, mode="markers", name='$D_3$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d4sparsex = defenders_x[3][50:-1:8]
    d4sparsey = defenders_y[3][50:-1:8]
    d4sparsex.append(defenders_x[3][-1])
    d4sparsey.append(defenders_y[3][-1])
    fig.add_trace(go.Scatter(x=d4sparsex, y=d4sparsey, mode="markers", name='$D_4$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")

def plot_simulation8v4_b3s(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    fig.add_trace(go.Scatter(x=[attackers_x[5][-1], defenders_x[0][-1]], y=[attackers_y[5][-1], defenders_y[0][-1]], mode="lines+markers", name="Assignment", marker=dict(symbol="cross", size=5, color='green')))
    fig.add_shape(type="line", x0=attackers_x[5][-1], y0=attackers_y[5][-1], x1=defenders_x[0][-1], y1=defenders_y[0][-1], line=dict(color="green",width=2))
    fig.add_shape(type="line", x0=attackers_x[1][-1], y0=attackers_y[1][-1], x1=defenders_x[1][-1], y1=defenders_y[1][-1], line=dict(color="green",width=2))

    # plot captured + stop in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1]], y=[attackers_y[0][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[defenders_x[2][-1]], y=[defenders_y[2][-1]], mode="markers", name='Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=498, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Baseline, t=1.0s<b>", 'y':0.85, 'x':0.425, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attackers
    # plot attacker 0
    sparsex1 = [attackers_x[0][-1]]
    sparsey1 = [attackers_y[0][-1]]
    # sparsex1.append(attackers_x[0][-1])
    # sparsey1.append(attackers_y[0][-1])
    fig.add_trace(go.Scatter(x=sparsex1, y=sparsey1, mode="markers", name=f"$A_{1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 1
    sparsex2 = attackers_x[1][0:-1:5]
    sparsey2 = attackers_y[1][0:-1:5]
    sparsex2.append(attackers_x[1][-1])
    sparsey2.append(attackers_y[1][-1])
    fig.add_trace(go.Scatter(x=sparsex2, y=sparsey2, mode="markers", name=f"$A_{2}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 2
    sparsex3 = [attackers_x[2][-1]]
    sparsey3 = [attackers_y[2][-1]]
    # sparsex3.append(attackers_x[2][-1])
    # sparsey3.append(attackers_y[2][-1])
    fig.add_trace(go.Scatter(x=sparsex3, y=sparsey3, mode="markers", name=f"$A_{3}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 3
    sparsex4 = [attackers_x[3][-1]]
    sparsey4 = [attackers_y[3][-1]]
    # sparsex4.append(attackers_x[3][-1])
    # sparsey4.append(attackers_y[3][-1])
    fig.add_trace(go.Scatter(x=sparsex4, y=sparsey4, mode="markers", name=f"$A_{4}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    # plot attacker 4
    sparsex5 = [attackers_x[4][-1]]
    sparsey5 = [attackers_y[4][-1]]
    # sparsex5.append(attackers_x[4][-1])
    # sparsey5.append(attackers_y[4][-1])
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{5}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 5
    sparsex6 = attackers_x[5][0:-1:5]
    sparsey6 = attackers_y[5][0:-1:5]
    sparsex6.append(attackers_x[5][-1])
    sparsey6.append(attackers_y[5][-1])
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{6}$ traj", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    # plot attacker 6
    sparsex7 = [attackers_x[6][-1]]
    sparsey7 = [attackers_y[6][-1] ]
    # sparsex7.append(attackers_x[6][-1])
    # sparsey7.append(attackers_y[6][-1])
    fig.add_trace(go.Scatter(x=sparsex7, y=sparsey7, mode="markers", name=f"$A_{7}$ arrived", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # symbol="cross-open", size=8, color='red'
    
    # plot attacker 7
    sparsex8 = [attackers_x[7][-1]]
    sparsey8 = [attackers_y[7][-1]]
    # sparsex8.append(attackers_x[7][-1])
    # sparsey8.append(attackers_y[7][-1])
    fig.add_trace(go.Scatter(x=sparsex8, y=sparsey8, mode="markers", name=f"$A_{8}$ arrived", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory


    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = defenders_x[0][180:-1:8]
    d1sparsey = defenders_y[0][180:-1:8]
    d1sparsex.append(defenders_x[0][-1])
    d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = defenders_x[1][180:-1:8]
    d2sparsey = defenders_y[1][180:-1:8]
    d2sparsex.append(defenders_x[1][-1])
    d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ traj', marker=dict(symbol="square", size=4, color='blue'), showlegend=False)) # symbol="star"

    d3sparsex = [defenders_x[2][-1]]
    d3sparsey = [defenders_y[2][-1]]
    # d3sparsex.append(defenders_x[2][-1])
    # d3sparsey.append(defenders_y[2][-1])
    fig.add_trace(go.Scatter(x=d3sparsex, y=d3sparsey, mode="markers", name='$D_3$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d4sparsex = [defenders_x[3][-1]]
    d4sparsey = [defenders_y[3][-1]]
    # d4sparsex.append(defenders_x[3][-1])
    # d4sparsey.append(defenders_y[3][-1])
    fig.add_trace(go.Scatter(x=d4sparsex, y=d4sparsey, mode="markers", name='$D_4$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")


def plot_simulation8v4_b2(attackers_x, attackers_y, defenders_x, defenders_y):

    print("Plotting beautiful 2D plots. Please wait\n")

    fig = go.Figure(data = go.Scatter(x=[0.6, 0.8], y=[0.1, 0.1], mode='lines', name='Target', line=dict(color='purple')), 
                    layout=Layout(plot_bgcolor='rgba(0,0,0,0)')) # for the legend
    # plot target
    fig.add_shape(type='rect', x0=0.6, y0=0.1, x1=0.8, y1=0.3, line=dict(color='purple', width=3.0), name="Target")

    # plot obstacles
    fig.add_shape(type='rect', x0=-0.1, y0=0.3, x1=0.1, y1=0.6, line=dict(color='black', width=3.0), name="Obstacle")
    fig.add_shape(type='rect', x0=-0.1, y0=-1.0, x1=0.1, y1=-0.3, line=dict(color='black', width=3.0))
    fig.add_trace(go.Scatter(x=[-0.1, 0.1], y=[0.3, 0.3], mode='lines', name='Obstacle', line=dict(color='black')))
    
    # plot MIP results
    # fig.add_trace(go.Scatter(x=[attackers_x[0][-1], defenders_x[0][-1]], y=[attackers_y[0][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A1", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[7][-1], defenders_x[0][-1]], y=[attackers_y[7][-1], defenders_y[0][-1]], mode="lines+markers", name="D1-A8", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[3][-1], defenders_x[1][-1]], y=[attackers_y[3][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A4", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[6][-1], defenders_x[1][-1]], y=[attackers_y[6][-1], defenders_y[1][-1]], mode="lines+markers", name="D2-A7", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[1][-1], defenders_x[2][-1]], y=[attackers_y[1][-1], defenders_y[2][-1]], mode="lines+markers", name="D3-A2", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[2][-1], defenders_x[2][-1]], y=[attackers_y[2][-1], defenders_y[2][-1]], mode="lines+markers", name="D3-A3", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[4][-1], defenders_x[3][-1]], y=[attackers_y[4][-1], defenders_y[3][-1]], mode="lines+markers", name="D4-A5", marker=dict(symbol="cross", size=5, color='green')))
    # fig.add_trace(go.Scatter(x=[attackers_x[5][-1], defenders_x[3][-1]], y=[attackers_y[5][-1], defenders_y[3][-1]], mode="lines+markers", name="D4-A6", marker=dict(symbol="cross", size=5, color='green')))

    # plot captured + stop in the legend
    fig.add_trace(go.Scatter(x=[attackers_x[0][-1]], y=[attackers_y[0][-1]], mode="markers", name=f"Captured", marker=dict(symbol="cross-open", size=8, color='red'))) # trajectory
    fig.add_trace(go.Scatter(x=[defenders_x[2][-1]], y=[defenders_y[2][-1]], mode="markers", name='Stop', marker=dict(symbol="square-open", size=8, color='blue'))) # symbol="star"

    # figure settings
    fig.update_layout(autosize=False, width=483, height=500, margin=dict(l=50, r=50, b=100, t=100, pad=0), 
                      title={'text': "<b>Baseline, t=1.5s<b>", 'y':0.85, 'x':0.438, 'xanchor': 'center','yanchor': 'top', 'font_size': 20}, paper_bgcolor="White", xaxis_range=[-1, 1], yaxis_range=[-1, 1], font=dict(size=12)) # LightSteelBlue
    fig.update_xaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False
    fig.update_yaxes(showline = True, linecolor = 'black', linewidth = 2.0, griddash = 'dot', zeroline=False, gridcolor = 'Lightgrey', mirror=True, ticks='outside') # showgrid=False,

    # plot attackers
    for i in range(6):
        sparsex = [attackers_x[i][-1]]
        sparsey = [attackers_y[i][-1]]
        # sparsex.append(attackers_x[i][-1])
        # sparsey.append(attackers_y[i][-1])
        fig.add_trace(go.Scatter(x=sparsex, y=sparsey, mode="markers", name=f"$A_{i+1}$ captured", marker=dict(symbol="cross-open", size=8, color='red'), showlegend=False)) # trajectory
    
    sparsex5 = [attackers_x[6][-1]]
    sparsey5 = [attackers_y[6][-1]]
    fig.add_trace(go.Scatter(x=sparsex5, y=sparsey5, mode="markers", name=f"$A_{7}$ arrived", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory

    sparsex6 = [attackers_x[7][-1] ]
    sparsey6 = [attackers_y[7][-1]]
    fig.add_trace(go.Scatter(x=sparsex6, y=sparsey6, mode="markers", name=f"$A_{8}$ arrived", marker=dict(symbol="triangle-up", size=4, color='red'), showlegend=False)) # trajectory


    # plot defenders
    # for j in range(len(defenders_x)):
    d1sparsex = [defenders_x[0][-1]]
    d1sparsey = [defenders_y[0][-1]]
    # d1sparsex.append(defenders_x[0][-1])
    # d1sparsey.append(defenders_y[0][-1])
    fig.add_trace(go.Scatter(x=d1sparsex, y=d1sparsey, mode="markers", name='$D_1$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d2sparsex = [defenders_x[1][-1]]
    d2sparsey = [defenders_y[1][-1]]
    # d2sparsex.append(defenders_x[1][-1])
    # d2sparsey.append(defenders_y[1][-1])
    fig.add_trace(go.Scatter(x=d2sparsex, y=d2sparsey, mode="markers", name='$D_2$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d3sparsex = [defenders_x[2][-1]]
    d3sparsey = [defenders_y[2][-1]]
    # d3sparsex.append(defenders_x[2][-1])
    # d3sparsey.append(defenders_y[2][-1])
    fig.add_trace(go.Scatter(x=d3sparsex, y=d3sparsey, mode="markers", name='$D_3$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    d4sparsex = [defenders_x[3][-1]]
    d4sparsey = [defenders_y[3][-1]]
    # d4sparsex.append(defenders_x[3][-1])
    # d4sparsey.append(defenders_y[3][-1])
    fig.add_trace(go.Scatter(x=d4sparsex, y=d4sparsey, mode="markers", name='$D_4$ stopped', marker=dict(symbol="square-open", size=8, color='blue'), showlegend=False)) # symbol="star"

    fig.show()
    print("Please check the plot on your browser.")
=======
    # Local figure save
    if plot_option.save_fig:
        if plot_option.interactive_html:
            fig.write_html(plot_option.filename + ".html")
        else:
            fig.write_image(plot_option.filename)


def plot_valuefunction(grid, V_ori, plot_option):
    '''
    Plot value function V, 1D or 2D grid is allowed
    https://plotly.com/python/3d-surface-plots/
    '''   
    dims_plot = plot_option.dims_plot
    grid, my_V = pre_plot(plot_option, grid, V_ori)

    if len(dims_plot) != 2 and len(dims_plot) != 1:
        raise Exception('dims_plot length should be equal to 2 or 1\n')

    if len(dims_plot) == 2 and len(my_V.shape) == 2:
        # Plot 3D surface for only one time step
        # dim1, dim2 = dims_plot[0], dims_plot[1]

        my_X = np.linspace(grid.min[0], grid.max[0], grid.pts_each_dim[0])
        my_Y = np.linspace(grid.min[1], grid.max[1], grid.pts_each_dim[1])
        my_V = my_V

        print("Plotting beautiful plots. Please wait\n")
        fig = go.Figure(data=go.Surface(
            # TODO chong: allow multiple sub-level sets
            contours = {
            "z": {"show": True, "start": -1, "end": 1, "size": 1, "color":"white", },
            },
            x=my_X,
            y=my_Y,
            z=my_V,
            colorscale=plot_option.colorscale,
            opacity=plot_option.opacity,
            lighting=plot_option.lighting,
            lightposition=plot_option.lightposition
            ))

    if len(dims_plot) == 2 and len(my_V.shape) == 3:
        # ref: https://plotly.com/python/visualizing-mri-volume-slices/
        # Plot 3D surface with animation
        # dim1, dim2 = dims_plot[0], dims_plot[1]
        my_X = np.linspace(grid.min[0], grid.max[0], grid.pts_each_dim[0])
        my_Y = np.linspace(grid.min[1], grid.max[1], grid.pts_each_dim[1])
        N = my_V.shape[2]

        print("Plotting beautiful plots. Please wait\n")

        # Define frames
        fig = go.Figure(frames=[go.Frame(data = go.Surface(
            # TODO chong: allow multiple sub-level sets
            contours = {
            "z": {"show": True, "start": -1, "end": 1, "size": 1, "color":"white", },
            },
            x=my_X,
            y=my_Y,
            z=my_V[:, :, N-k-1],
            colorscale=plot_option.colorscale,
            opacity=plot_option.opacity,
            lighting=plot_option.lighting,
            lightposition=plot_option.lightposition
            ),
            name=str(k) # you need to name the frame for the animation to behave properly
            )
            for k in range(N)])

        # Add data to be displayed before animation starts
        fig.add_trace(go.Surface(
            # TODO chong: allow multiple sub-level sets
            contours = {
            "z": {"show": True, "start": -1, "end": 1, "size": 1, "color":"white", },
            },
            x=my_X,
            y=my_Y,
            z=my_V[:, :, N-1],
            colorscale=plot_option.colorscale,
            opacity=plot_option.opacity,
            lighting=plot_option.lighting,
            lightposition=plot_option.lightposition
            ))
        
        fig.update_layout(
            title='2D Value Function',
            scene=dict( xaxis={"nticks": 20},
                        zaxis={"nticks": 4},
                        camera_eye={"x": 0, "y": -1, "z": 0.5},
                        aspectratio={"x": 1, "y": 1, "z": 0.2}
                        ))
        
        fig = slider_define(fig)

    if len(dims_plot) == 1 and len(my_V.shape) == 1:
        # Plot 1D isosurface for only one time step
        # dim1 = dims_plot[0]
        complex_x = complex(0, grid.pts_each_dim[0])
        mg_X = np.mgrid[grid.min[0]:grid.max[0]: complex_x]


        if (my_V > 0.0).all():
            print("Implicit surface will not be shown since all values are positive ")
        if (my_V < 0.0).all():
            print("Implicit surface will not be shown since all values are negative ")

        print("Plotting beautiful 1D plots. Please wait\n")
        fig = go.Figure(data=px.line(
            x=mg_X.flatten(),
            y=my_V.flatten(),
            labels={'x','Vaue'}
        ), layout=go.Layout(plot_bgcolor='rgba(0,0,0,0)'))

        fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black')
        fig.update_yaxes(range=[-1, 1.5])



    if len(dims_plot) == 1 and len(my_V.shape) == 2:
        # Plot 1D isosurface with animation
        # dim1 = dims_plot[0]
        complex_x = complex(0, grid.pts_each_dim[0])
        mg_X = np.mgrid[grid.min[0]:grid.max[0]: complex_x]
        
        N = my_V.shape[1]

        # Define frames
        fig = go.Figure(frames=[go.Frame(data=go.Scatter(
            x=mg_X.flatten(),
            y=my_V[:,N-k-1].flatten()
            ), layout=go.Layout(plot_bgcolor='rgba(0,0,0,0)'),
            name=str(k) # you need to name the frame for the animation to behave properly
            )
            for k in range(N)])

        # Add data to be displayed before animation starts
        fig.add_trace(go.Scatter(
            x=mg_X.flatten(),
            y=my_V[:,N-1].flatten()))
        
        fig.update_layout(title='1D Value Function',)
        
        fig = slider_define(fig, duration=0)


        fig.update_yaxes(zeroline=True, zerolinewidth=1, zerolinecolor='black')
        fig.update_yaxes(range=[-1, 1.5])
        fig.update_layout(transition = {'duration':0})

    if plot_option.do_plot:
        fig.show()
        print("Please check the plot on your browser.")
        # Local figure save
    if plot_option.save_fig:
        if plot_option.interactive_html:
            fig.write_html(plot_option.filename + ".html")
        else:
            fig.write_image(plot_option.filename)

###################################################################################################################################
def slider_define(fig, duration=300):
    '''
    Internal function
    Define slider for the animation
    '''
    def frame_args(duration):
            return {
                    "frame": {"duration": duration},
                    "mode": "immediate",
                    "fromcurrent": True,
                    "transition": {"duration": duration},
                }
        
    sliders = [
            {
                "pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "currentvalue": {
                    "font": {"size": 20},
                    "prefix": "Time Step:",
                    "visible": True,
                    "xanchor": "right"
                },
                "steps": [
                    {
                        "args": [[f.name], frame_args(0)],
                        "label": str(k),
                        "method": "animate",
                    }
                    for k, f in enumerate(fig.frames)
                ],
            }
        ]

        # Layout
    fig.update_layout(
                updatemenus = [
                    {
                        "buttons": [
                            {
                                "args": [None, frame_args(duration)],
                                "label": "Play", # play symbol
                                "method": "animate",
                            },
                            {
                                "args": [[None], frame_args(0)],
                                "label": "pause", # pause symbol
                                "method": "animate",
                            },
                        ],
                        "direction": "left",
                        "pad": {"r": 10, "t": 70},
                        "type": "buttons",
                        "x": 0.1,
                        "y": 0,
                    }
                ],
                sliders=sliders
        )
    return fig


def pre_plot(plot_option, grid, V_ori):
    """
    Pre-processing steps for plotting
    """


    # Slicing process
    dims_plot = plot_option.dims_plot
    idx = [slice(None)] * grid.dims
    slice_idx = 0

    # Build new grid
    grid_min = grid.min
    grid_max = grid.max
    dims = grid.dims
    N = grid.pts_each_dim

    delete_idx = []
    dims_list = list(range(grid.dims))

    for i in dims_list:
        if i not in dims_plot:
            idx[i] = plot_option.slices[slice_idx]
            slice_idx += 1
            dims = dims -1
            delete_idx.append(i)
    N = np.delete(N, delete_idx)
    grid_min = np.delete(grid_min, delete_idx)
    grid_max = np.delete(grid_max, delete_idx)

    V = V_ori[tuple(idx)]
    
    grid = Grid(grid_min, grid_max, dims, N)

    # Downsamping process
    if plot_option.scale is not None:
        scale = plot_option.scale
    else:
        scale = [1] * grid.dims
        for i in range(grid.dims):
            if grid.pts_each_dim[i] > 30:
                scale[i] = np.floor(grid.pts_each_dim[i]/30).astype(int)
    grid, V = downsample(grid, V, scale)

    return grid, V

def downsample(g, data, scale):
    """
    Dowsampling for large 3D grid size, e.g. 100x100x100 for efficient plotting
    """

    if len(scale) != g.dims:
        raise Exception('scale length should be equal to grid dimension\n')

    odd_ind =[False] * g.dims
    for i in range(g.dims):
        if g.pts_each_dim[i] % scale[i] != 0:
            odd_ind[i] = True
    
    # Generate new data
    idx = [slice(0,None,scale[0])] * g.dims
    for i in range(g.dims):
        if odd_ind[i]:
                idx[i] = slice(0,-(g.pts_each_dim[i]%scale[i]),scale[i])
    data_out = data[tuple(idx)]
    # Generate new grid
    grid_min = g.min
    grid_max = g.max
    dims = g.dims
    N = g.pts_each_dim
    for i in range(g.dims):
        if odd_ind[i]:
            grid_max[i] = g.max[i]-(g.pts_each_dim[i]%scale[i])*(g.max[i]-g.min[i])/g.pts_each_dim[i]
            N[i] = ((g.pts_each_dim[i]-g.pts_each_dim[i]%scale[i])/scale[i]).astype(np.int64)
        else:
            N[i] = (g.pts_each_dim[i]/scale[i]).astype(np.int64)
    g_out = Grid(grid_min, grid_max, dims, N)

    return g_out, data_out
       
>>>>>>> dev_hhy
