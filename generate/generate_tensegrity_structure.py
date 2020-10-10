#!/usr/bin/env python3

from math import pi, cos, sin
import cadquery as cq
import numpy as np

# vr (VR scaling in meters) or mm (millimeter scaling)
scale_mode = "vr"

# The complexity values
p = 12 # ik strip
q = 30 # Strips in torus along centerline

# The centerline radius of the torus and the radius of the pressure tube
if scale_mode == "vr":
    r = 5
    R = 10
    node_r = 0.05 # The radius of the connection nodes
    bar_w = 0.05 # The width of a bar 
    bar_h = 0.05 # The height of a bar
else:
    r = 5000
    R = 10000
    node_r = 500 # The radius of the connection nodes
    bar_w = 500 # The width of a bar 
    bar_h = 500 # The height of a bar

# How far to revolve the structure (cutaway vs whole)
rev_angle = 360

# A few variables just to help clean the code up
zMat = np.array([[0, 0]])

# Constant arrays for defining connectivity matrices
e1 = np.array([[1, 0]])
e2 = np.array([[0, 1]])
E1 = np.concatenate( (e1, zMat) )
E2 = np.concatenate( (zMat, e2) )
T1 = np.concatenate( (zMat, zMat, e2, np.negative(e2), np.negative(e2), zMat, zMat, np.negative(e2)) ) # Capital Theta 1
T2 = np.concatenate( (e2, np.negative(e1), np.negative(e2), zMat, e1, e2, np.negative(e1), zMat, zMat) ) # Capital Theta 2
T3 = np.concatenate( (zMat, zMat, zMat, zMat, zMat, zMat, np.negative(e1), e2) ) # Capital Theta 3
T4 = np.concatenate( (zMat, e1, np.negative(e1), zMat, zMat, e1, e1, zMat) ) # Capital Theta 4

"""
Returns a reference representation of a connectivity node.
"""
def node(pos, l):
    return cq.Workplane("XY").box(node_r, node_r, node_r).translate((pos[0][l - 1], pos[1][l - 1], pos[2][l - 1]))

"""
Returns a 3D representation of a bar.
"""
def bar(start, end):
    return cq.Workplane("XY").box(bar_w, bar_h, 0.5).translate(start[0, 0], start[0, 1], start[0, 2])

"""
Given the i, k and l, returns the node vector.
"""
def N(i, k):
    Nl = None

    for l in range(1, 3):
        # The angles
        phil = (2 * i + (l - 1)) * pi / q
        thetal = (2 * k + l) + pi / p

        # The torus radii
        Rl = np.array([R * cos(phil), R * sin(phil), 0])
        rl = np.array([r * cos(thetal) * cos(phil),
                    r * cos(thetal) * sin(phil),
                    -r * sin(thetal)])

        rs_added = np.add(Rl, rl)

        # Either start the array off, or dstack the two 1D arrays together into a 2D array
        if l == 1:
            Nl = np.array(rs_added)
        else:
            Nl = np.dstack((Nl, rs_added))

    return Nl

# Reference torus to make sure the generated structure looks generally correct
torus = (cq.Workplane('YZ')
            .center(-R, 0)
            .circle(r)
            .circle(r - (r * 0.01))
            .revolve(rev_angle, [R, 0], [R, 1], clean=True))
assy = cq.Assembly(torus, loc=cq.Location(cq.Vector(0, 0, 0)), color=cq.Color(0.25, 0.64, 0.88, 0.5))

# Step through all the q and p units and place the nodes for them
i_adj = 0
k_adj = 0
for i in range(0, q):
    for k in range(0, p):
        # Add the current node
        N_1_2 = N(i, k)
        assy.add(node(N_1_2[0], 1), color=cq.Color(1, 1, 1, 0))
        assy.add(node(N_1_2[0], 2), color=cq.Color(1, 1, 1, 0))

        # Make sure we do not overstep the boundary conditions
        i_adj += 1
        k_adj += 1
        if i_adj == (q - 1):
            i_adj = 0
        if k == (p - 1):
            k_adj = 0

        # Find the adjacent bar node connections for the current ik unit
        N_1_2_plus = N(i_adj, k_adj)

        # Create a bar between the n1 node of the current unit to the n1 node of the i+1,k+1 unit
        # assy.add(bar(N_1_2[0], N_1_2_plus[0]), color=cq.Color(0, 0, 1))

show_object(assy)
            