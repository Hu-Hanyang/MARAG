import heterocl as hcl
from odp.computeGraphs.CustomGraphFunctions import *

################## 2D SPATIAL DERIVATIVE FUNCTION #################
def secondOrderX(i, j, V, g):
    left_deriv = hcl.scalar(0, "left_deriv")
    right_deriv = hcl.scalar(0, "right_deriv")

    dim_idx = 0

    u_i = V[i, j]

    with hcl.if_(i == 0):
        u_i_minus_1 = hcl.scalar(0, "u_i_minus_1")

        u_i_plus_1 = V[i + 1, j]
        u_i_plus_2 = V[i + 2, j]

        u_i_minus_1[0] = u_i + my_abs(u_i_plus_1 - u_i) * my_sign(u_i)

        D1_i_plus_half = (u_i_plus_1 - u_i) / g.dx[dim_idx]
        D1_i_minus_half = (u_i - u_i_minus_1[0]) / g.dx[dim_idx]

        Q1d_left = D1_i_minus_half
        Q1d_right = D1_i_plus_half

        D2_i = 0.5 * ((D1_i_plus_half - D1_i_minus_half) / g.dx[dim_idx])

        u_i_plus_1_plus_1 = u_i_plus_2
        D1_i_plus_1_plus_half = (u_i_plus_1_plus_1 - u_i_plus_1) / g.dx[dim_idx]
        D1_i_plus_1_minus_half = D1_i_plus_half
        D2_i_plus_1 = 0.5 * ((D1_i_plus_1_plus_half - D1_i_plus_1_minus_half) / g.dx[dim_idx])

        with hcl.if_(my_abs(D2_i) <= my_abs(D2_i_plus_1)):
            c = D2_i
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

        with hcl.else_():
            c = D2_i_plus_1
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

    with hcl.elif_(i == V.shape[dim_idx] - 1):
        u_i_plus_1 = hcl.scalar(0, "u_i_plus_1")
        u_i_plus_2 = hcl.scalar(0, "u_i_plus_2")

        u_i_minus_1 = V[i - 1, j]

        u_i_plus_1[0] = u_i + my_abs(u_i - u_i_minus_1) * my_sign(u_i)
        u_i_plus_2[0] = u_i_plus_1[0] + my_abs(u_i_plus_1[0] - u_i) * my_sign(u_i_plus_1[0])

        D1_i_plus_half = (u_i_plus_1[0] - u_i) / g.dx[dim_idx]
        D1_i_minus_half = (u_i - u_i_minus_1) / g.dx[dim_idx]

        Q1d_left = D1_i_minus_half
        Q1d_right = D1_i_plus_half

        D2_i = 0.5 * ((D1_i_plus_half - D1_i_minus_half) / g.dx[dim_idx])

        u_i_plus_1_plus_1 = u_i_plus_2[0]
        D1_i_plus_1_plus_half = (u_i_plus_1_plus_1 - u_i_plus_1[0]) / g.dx[dim_idx]
        D1_i_plus_1_minus_half = D1_i_plus_half
        D2_i_plus_1 = 0.5 * ((D1_i_plus_1_plus_half - D1_i_plus_1_minus_half) / g.dx[dim_idx])

        with hcl.if_(my_abs(D2_i) <= my_abs(D2_i_plus_1)):
            c = D2_i
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

        with hcl.else_():
            c = D2_i_plus_1
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

    with hcl.elif_(i == V.shape[dim_idx] - 2):
        u_i_plus_2 = hcl.scalar(0, "u_i_plus_2")

        u_i_plus_1 = V[i + 1, j]

        u_i_minus_1 = V[i - 1, j]

        u_i_plus_2[0] = u_i_plus_1 + my_abs(u_i_plus_1 - u_i) * my_sign(u_i_plus_1)

        D1_i_plus_half = (u_i_plus_1 - u_i) / g.dx[dim_idx]
        D1_i_minus_half = (u_i - u_i_minus_1) / g.dx[dim_idx]

        Q1d_left = D1_i_minus_half
        Q1d_right = D1_i_plus_half

        D2_i = 0.5 * ((D1_i_plus_half - D1_i_minus_half) / g.dx[dim_idx])

        u_i_plus_1_plus_1 = u_i_plus_2[0]
        D1_i_plus_1_plus_half = (u_i_plus_1_plus_1 - u_i_plus_1) / g.dx[dim_idx]
        D1_i_plus_1_minus_half = D1_i_plus_half
        D2_i_plus_1 = 0.5 * ((D1_i_plus_1_plus_half - D1_i_plus_1_minus_half) / g.dx[dim_idx])

        with hcl.if_(my_abs(D2_i) <= my_abs(D2_i_plus_1)):
            c = D2_i
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

        with hcl.else_():
            c = D2_i_plus_1
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

    with hcl.else_():
        u_i_minus_1 = V[i - 1, j]

        u_i_plus_1 = V[i + 1, j]
        u_i_plus_2 = V[i + 2, j]

        D1_i_plus_half = (u_i_plus_1 - u_i) / g.dx[dim_idx]
        D1_i_minus_half = (u_i - u_i_minus_1) / g.dx[dim_idx]

        Q1d_left = D1_i_minus_half
        Q1d_right = D1_i_plus_half

        D2_i = 0.5 * ((D1_i_plus_half - D1_i_minus_half) / g.dx[dim_idx])

        u_i_plus_1_plus_1 = u_i_plus_2
        D1_i_plus_1_plus_half = (u_i_plus_1_plus_1 - u_i_plus_1) / g.dx[dim_idx]
        D1_i_plus_1_minus_half = D1_i_plus_half
        D2_i_plus_1 = 0.5 * ((D1_i_plus_1_plus_half - D1_i_plus_1_minus_half) / g.dx[dim_idx])

        with hcl.if_(my_abs(D2_i) <= my_abs(D2_i_plus_1)):
            c = D2_i
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

        with hcl.else_():
            c = D2_i_plus_1
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

    return left_deriv[0], right_deriv[0]


def secondOrderY(i, j, V, g):
    left_deriv = hcl.scalar(0, "left_deriv")
    right_deriv = hcl.scalar(0, "right_deriv")

    dim_idx = 1

    u_i = V[i, j]

    with hcl.if_(j == 0):
        u_i_minus_1 = hcl.scalar(0, "u_i_minus_1")

        u_i_plus_1 = V[i, j + 1]
        u_i_plus_2 = V[i, j + 2]

        u_i_minus_1[0] = u_i + my_abs(u_i_plus_1 - u_i) * my_sign(u_i)

        D1_i_plus_half = (u_i_plus_1 - u_i) / g.dx[dim_idx]
        D1_i_minus_half = (u_i - u_i_minus_1[0]) / g.dx[dim_idx]

        Q1d_left = D1_i_minus_half
        Q1d_right = D1_i_plus_half

        D2_i = 0.5 * ((D1_i_plus_half - D1_i_minus_half) / g.dx[dim_idx])

        u_i_plus_1_plus_1 = u_i_plus_2
        D1_i_plus_1_plus_half = (u_i_plus_1_plus_1 - u_i_plus_1) / g.dx[dim_idx]
        D1_i_plus_1_minus_half = D1_i_plus_half
        D2_i_plus_1 = 0.5 * ((D1_i_plus_1_plus_half - D1_i_plus_1_minus_half) / g.dx[dim_idx])

        with hcl.if_(my_abs(D2_i) <= my_abs(D2_i_plus_1)):
            c = D2_i
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

        with hcl.else_():
            c = D2_i_plus_1
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

    with hcl.elif_(j == V.shape[dim_idx] - 1):
        u_i_plus_1 = hcl.scalar(0, "u_i_plus_1")
        u_i_plus_2 = hcl.scalar(0, "u_i_plus_2")

        u_i_minus_1 = V[i, j - 1]

        u_i_plus_1[0] = u_i + my_abs(u_i - u_i_minus_1) * my_sign(u_i)
        u_i_plus_2[0] = u_i_plus_1[0] + my_abs(u_i_plus_1[0] - u_i) * my_sign(u_i_plus_1[0])

        D1_i_plus_half = (u_i_plus_1[0] - u_i) / g.dx[dim_idx]
        D1_i_minus_half = (u_i - u_i_minus_1) / g.dx[dim_idx]

        Q1d_left = D1_i_minus_half
        Q1d_right = D1_i_plus_half

        D2_i = 0.5 * ((D1_i_plus_half - D1_i_minus_half) / g.dx[dim_idx])

        u_i_plus_1_plus_1 = u_i_plus_2[0]
        D1_i_plus_1_plus_half = (u_i_plus_1_plus_1 - u_i_plus_1[0]) / g.dx[dim_idx]
        D1_i_plus_1_minus_half = D1_i_plus_half
        D2_i_plus_1 = 0.5 * ((D1_i_plus_1_plus_half - D1_i_plus_1_minus_half) / g.dx[dim_idx])

        with hcl.if_(my_abs(D2_i) <= my_abs(D2_i_plus_1)):
            c = D2_i
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

        with hcl.else_():
            c = D2_i_plus_1
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

    with hcl.elif_(j == V.shape[dim_idx] - 2):
        u_i_plus_2 = hcl.scalar(0, "u_i_plus_2")

        u_i_plus_1 = V[i, j + 1]

        u_i_minus_1 = V[i, j - 1]

        u_i_plus_2[0] = u_i_plus_1 + my_abs(u_i_plus_1 - u_i) * my_sign(u_i_plus_1)

        D1_i_plus_half = (u_i_plus_1 - u_i) / g.dx[dim_idx]
        D1_i_minus_half = (u_i - u_i_minus_1) / g.dx[dim_idx]

        Q1d_left = D1_i_minus_half
        Q1d_right = D1_i_plus_half

        D2_i = 0.5 * ((D1_i_plus_half - D1_i_minus_half) / g.dx[dim_idx])

        u_i_plus_1_plus_1 = u_i_plus_2[0]
        D1_i_plus_1_plus_half = (u_i_plus_1_plus_1 - u_i_plus_1) / g.dx[dim_idx]
        D1_i_plus_1_minus_half = D1_i_plus_half
        D2_i_plus_1 = 0.5 * ((D1_i_plus_1_plus_half - D1_i_plus_1_minus_half) / g.dx[dim_idx])

        with hcl.if_(my_abs(D2_i) <= my_abs(D2_i_plus_1)):
            c = D2_i
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

        with hcl.else_():
            c = D2_i_plus_1
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

    with hcl.else_():
        u_i_minus_1 = V[i, j - 1]

        u_i_plus_1 = V[i, j + 1]
        u_i_plus_2 = V[i, j + 2]

        D1_i_plus_half = (u_i_plus_1 - u_i) / g.dx[dim_idx]
        D1_i_minus_half = (u_i - u_i_minus_1) / g.dx[dim_idx]

        Q1d_left = D1_i_minus_half
        Q1d_right = D1_i_plus_half

        D2_i = 0.5 * ((D1_i_plus_half - D1_i_minus_half) / g.dx[dim_idx])

        u_i_plus_1_plus_1 = u_i_plus_2
        D1_i_plus_1_plus_half = (u_i_plus_1_plus_1 - u_i_plus_1) / g.dx[dim_idx]
        D1_i_plus_1_minus_half = D1_i_plus_half
        D2_i_plus_1 = 0.5 * ((D1_i_plus_1_plus_half - D1_i_plus_1_minus_half) / g.dx[dim_idx])

        with hcl.if_(my_abs(D2_i) <= my_abs(D2_i_plus_1)):
            c = D2_i
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

        with hcl.else_():
            c = D2_i_plus_1
            Q2d = c * g.dx[dim_idx]

            left_deriv[0] = Q1d_left + Q2d
            right_deriv[0] = Q1d_right - Q2d

    return left_deriv[0], right_deriv[0]