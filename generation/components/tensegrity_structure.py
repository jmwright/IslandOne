from math import sqrt
import cadquery as cq
import numpy as np
from .model.node_matrix import N

class TensegrityStructure:
    p = None
    q = None
    R = None
    r = None
    node_r = None
    bar_w = None
    bar_h = None
    simplified = False
    structure = cq.Assembly()

    def __init__(self, p, q, R, r, cutaway=False, simplified=False):
        self.p = p
        self.q = q
        self.R = R
        self.r = r

        # Derived sizes for nodes, bars and strings
        self.node_r = r / 50.0 # The radius of the connection nodes
        self.bar_w = r / 10.0 # The width of a bar 
        self.bar_h = r / 10.0 # The height of a bar

        self.simplified = simplified

    def get(self):
        # Step through all the q and p units and place the nodes for them
        for i in range(0, self.q):
            for k in range(0, self.p):
                # Add the current node
                N_1_2 = N(i, k, self.R, self.r, self.p, self.q).get()
                self.structure.add(self.node(N_1_2[0], 1), color=cq.Color(1, 1, 1, 1))
                self.structure.add(self.node(N_1_2[0], 2), color=cq.Color(1, 1, 1, 1))

                # Get the indexes of the next and previous strips
                i_adj = i + 1
                k_adj = k + 1
                k_m_adj = k - 1

                # If we have looped around, reset the adjacent i and k indices for the boundary conditions
                if i_adj > self.q:
                    i_adj = 0
                if k_adj > self.p:
                    k_adj = 0
                if k_m_adj < 0:
                    k_m_adj = self.p - 1

                # Find the adjacent bar node connections for the current ik unit
                N_1_2_plus = N(i_adj, k_adj, self.R, self.r, self.p, self.q).get()
                N_1_2_minus = N(i_adj, k_m_adj, self.R, self.r, self.p, self.q).get()

                # Create a bar between the n1 node of the current unit to the n1 node of the i+1,k+1 unit
                self.structure.add(self.bar(N_1_2[0], N_1_2_plus[0], 1), color=cq.Color(0, 0, 1))
                self.structure.add(self.bar(N_1_2[0], N_1_2_minus[0], 2), color=cq.Color(0, 0, 1))

        return self.structure

    """
    Returns a reference representation of a connectivity node.
    """
    def node(self, pos, l):
        new_node = None

        if self.simplified:
            new_node = cq.Workplane().box(self.node_r * 2.0, self.node_r * 2.0, self.node_r * 2.0)
        else:
            new_node = cq.Workplane().sphere(self.node_r)
        
        return new_node.translate((pos[0][l - 1], pos[1][l - 1], pos[2][l - 1]))

    """
    Returns a 3D representation of a bar.
    """
    def bar(self, start, end, l):
        direction = (end[0][l - 1] - start[0][l - 1], end[1][l - 1] - start[1][l - 1], end[2][l - 1] - start[2][l - 1])
        magnitude = sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)

        return cq.Workplane(cq.Plane(origin=(start[0][l - 1], start[1][l - 1], start[2][l - 1]), xDir=(1,0,0), normal=direction)).rect(0.1, 0.1).extrude(magnitude)
            