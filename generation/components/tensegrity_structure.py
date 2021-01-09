from math import sqrt
import cadquery as cq
import numpy as np
from .model.node_matrix import N
from .tensegrity_node import Node
from .tensegrity_bar import TBar
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
                # Get the indexes of the next and previous strips
                ip = i + 1
                im = i - 1
                kp = k + 1
                km = k - 1

                # If we have looped around, reset the adjacent i and k indices for the boundary conditions
                if ip > self.q:
                    ip = 0
                if im < 0:
                    im = self.q - 1
                if kp > self.p:
                    kp = 0
                if km < 0:
                    km = self.p - 1

                # Find the adjacent bar node connections for the current ik unit
                # ip = i + 1
                # kp = k + 1
                # im = i - 1
                # km = k - 1
                N_i_k = N(i, k, self.R, self.r, self.p, self.q).get()
                N_ip_kp = N(ip, kp, self.R, self.r, self.p, self.q).get()
                N_ip_km = N(ip, km, self.R, self.r, self.p, self.q).get()
                N_ip_k = N(ip, k, self.R, self.r, self.p, self.q).get()
                N_i_kp = N(i, kp, self.R, self.r, self.p, self.q).get()
                N_im_k = N(im, k, self.R, self.r, self.p, self.q).get()
                N_im_km = N(im, km, self.R, self.r, self.p, self.q).get()

                # Add the current node
                self.structure.add(Node(N_i_k[0], 1, self.r, simplified=self.simplified).get(), color=cq.Color(1, 1, 1, 1))
                self.structure.add(Node(N_i_k[0], 2, self.r, simplified=self.simplified).get(), color=cq.Color(1, 1, 1, 1))

                # Create a bar between the n1 node of the current unit to the n1 node of the i+1,k+1 unit
                self.structure.add(TBar(N_i_k[0], N_ip_kp[0], 1, self.r).get(), color=cq.Color(0, 0, 1))
                self.structure.add(TBar(N_i_k[0], N_ip_km[0], 2, self.r).get(), color=cq.Color(0, 0, 1))

                # Add the strings between the appropriate nodes
                self.structure.add(TString(N_i_k[0], N_i_k[0], 1, 2, self.r).get(), color=cq.Color(1, 0, 0)) # N(i,k) n1 to N(i,k) n2
                self.structure.add(TString(N_i_k[0], N_ip_k[0], 2, 1, self.r).get(), color=cq.Color(1, 0, 0)) # N(i,k) n2 to N(i+1,k) n1
                self.structure.add(TString(N_i_k[0], N_im_km[0], 1, 2, self.r).get(), color=cq.Color(1, 0, 0)) # N(i,k) n1 to N(i-1,k-1) n2
                self.structure.add(TString(N_i_k[0], N_i_kp[0], 2, 1, self.r).get(), color=cq.Color(1, 0, 0)) # N(i,k) n2 to N(i,k+1) n1
                self.structure.add(TString(N_i_k[0], N_i_kp[0], 2, 2, self.r).get(), color=cq.Color(1, 0, 0)) # N(i,k) n2 to N(i,k+1) n2
                self.structure.add(TString(N_i_k[0], N_ip_k[0], 1, 1, self.r).get(), color=cq.Color(1, 0, 0)) # N(i,k) n1 to N(i+1,k) n1
                self.structure.add(TString(N_i_k[0], N_i_kp[0], 1, 1, self.r).get(), color=cq.Color(1, 0, 0)) # N(i,k) n1 to N(i,k+1) n1
                self.structure.add(TString(N_i_k[0], N_ip_k[0], 2, 2, self.r).get(), color=cq.Color(1, 0, 0)) # N(i,k) n2 to N(i+1,k) n2

        return self.structure
