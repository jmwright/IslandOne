from math import sqrt
import cadquery as cq
import numpy as np
from .model.node_matrix import N
from .tensegrity_node import Node
from .tensegrity_bar import Bar
from .tensegrity_string import TString

class TensegrityStructure:
    """
    Generated tensegrity structure that makes up the skeletal frame of the toroidal
    pressure hull.

    Attributes
    ----------
    p : int
        Complexity of the torus structure, number of units in the k axis.
    q : int
        Complexity of the torus structure, number of units in the i axis.
    R : float
        The radius from the center of the station to the center line of the habitat torus.
    r : float
        The radius of the pressurized habitat torus.
    cutaway : bool
        Whether or not the torus structure should encompass the entire 360 degree envelope.
        Has no effect currently, but is designed to allow the inside of the torus to be visible.
    simplified : bool
        Whether or not to use simplified primitives to decrease generation and rendering time.
    """

    p = None
    q = None
    R = None
    r = None
    cutaway = None
    simplified = False
    structure = cq.Assembly()

    def __init__(self, p, q, R, r, cutaway=False, simplified=False):
        """
        Collects the attributes that allow the tensegrity structure to be built.

        Parameters
        ----------
        p : int
            Complexity of the torus structure, number of units in the k axis.
        q : int
            Complexity of the torus structure, number of units in the i axis.
        R : float
            The radius from the center of the station to the center line of the habitat torus.
        r : float
            The radius of the pressurized habitat torus.
        cutaway : bool
            Whether or not the torus structure should encompass the entire 360 degree envelope.
            Has no effect currently, but is designed to allow the inside of the torus to be visible.
        simplified : bool
            Whether or not to use simplified primitives to decrease generation and rendering time.
        """

        self.p = p
        self.q = q
        self.R = R
        self.r = r
        self.cutaway = cutaway
        self.simplified = simplified

    def get(self):
        """
        Constructs the CadQuery assembly the represents the tensegrity structure of the toroidal  
        pressure hull.

        Parameters
        ----------
        None
        """

        # Step through all the q and p units and place the nodes for them
        for i in range(0, self.q):
            for k in range(0, self.p):
                # Add the current node
                N_1_2 = N(i, k, self.R, self.r, self.p, self.q).get()
                self.structure.add(Node(N_1_2[0], 1, self.r, simplified=True).get(), color=cq.Color(1, 1, 1, 1))
                self.structure.add(Node(N_1_2[0], 2, self.r, simplified=True).get(), color=cq.Color(1, 1, 1, 1))

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
                self.structure.add(Bar(N_1_2[0], N_1_2_plus[0], 1, self.r).get(), color=cq.Color(0, 0, 1))
                self.structure.add(Bar(N_1_2[0], N_1_2_minus[0], 2, self.r).get(), color=cq.Color(0, 0, 1))

                # Add the strings between the appropriate nodes
                self.structure.add(TString(N_1_2[0], N_1_2[0], 1, self.r).get(), color=cq.Color(1, 0, 0))

        return self.structure
