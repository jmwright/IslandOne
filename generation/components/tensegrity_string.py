from math import sqrt
import cadquery as cq
from .common import Common

class TString:
    """
    Single string of the tensegrity structure that makes up the skeletal frame of the toroidal
    pressure hull. Each string has a start point (origin) and an endpoint. The direction on length
    of the string are determined based on those two points.

    Attributes
    ----------
    start : numpy.array
        A matrix containing both string starts for an ik unit of the DHT torus structure.
    end : numpy.array
        A matrix containing both string ends for an ik unit of the DHT torus structure.
    l : int
        Selects which DHT ik unit string to work with (1 or 2).
    """

    # Passed parameters
    start = None
    end = None
    l_start = None
    l_end = None

    # Computed parameters
    str_r = None


    def __init__(self, start, end, l_start, l_end, r):
        """
        Collects the attributes that allows the tensegrity string to be constructed.

        Parameters
        ----------
        start : numpy.array
            A matrix containing both string starts for an ik unit of the DHT torus structure.
        end : numpy.array
            A matrix containing both string ends for an ik unit of the DHT torus structure.
        l_start : int
            Selects which DHT ik unit node to work with (1 or 2).
        l_end : int
            Selects which DHT ik unit node to work with (1 or 2).
        r : float
            The radius of the pressurized habitat torus.
        """

        self.start = start
        self.end = end
        self.l_start = l_start - 1 # numpy arrays are 0 based and the node numbers are 1 based
        self.l_end = l_end - 1

        self.str_r = r / 100.0 # The radius of the string


    def get(self):
        """
        Constructs the CadQuery object the represents a tensegrity string with the correct
        location, orientation and length.

        Parameters
        ----------
        None
        """

        # Vector defining the direction of the bar
        direction = (self.end[0][self.l_end] - self.start[0][self.l_start],
                     self.end[1][self.l_end] - self.start[1][self.l_start],
                     self.end[2][self.l_end] - self.start[2][self.l_start])

        # The (vector) length of the bar
        magnitude = sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)

        # Build the bar at the specified location, in the specified direction, for the specified length
        return cq.Workplane(cq.Plane(origin=(self.start[0][self.l_start], self.start[1][self.l_start], self.start[2][self.l_start]),
                                     xDir=Common.computeXDir(direction),
                                     normal=direction)).circle(self.str_r).extrude(magnitude)
