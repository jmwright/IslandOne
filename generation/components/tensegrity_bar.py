from math import sqrt
import cadquery as cq

class Bar:
    """
    Single bar of the tensegrity structure that makes up the skeletal frame of the toroidal
    pressure hull. Each bar has a start point (origin) and an endpoint. The direction on length 
    of the bar are determined based on those two points.

    Attributes
    ----------
    start : numpy.array
        A matrix containing both bar starts for an ik unit of the DHT torus structure.
    end : numpy.array
        A matrix containing both bar ends for an ik unit of the DHT torus structure.
    l : int
        Selects which DHT ik unit bar to work with (1 or 2).
    """

    # Passed parameters
    start = None
    end = None
    l = None

    # Computed parameters
    bar_w = None
    bar_h = None

    def __init__(self, start, end, l, r):
        """
        Collects the attributes that allows the tensegrity bar to be constructed.

        Parameters
        ----------
        start : numpy.array
            A matrix containing both bar starts for an ik unit of the DHT torus structure.
        end : numpy.array
            A matrix containing both bar ends for an ik unit of the DHT torus structure.
        l : int
            Selects which DHT ik unit bar to work with (1 or 2).
        r : float
            The radius of the pressurized habitat torus.
        """

        self.start = start
        self.end = end
        self.l = l

        self.bar_w = r / 50.0 # The width of a bar 
        self.bar_h = r / 50.0 # The height of a bar

    def get(self):
        """
        Constructs the CadQuery object the represents a tensegrity bar with the correct
        location, orientation and length.

        Parameters
        ----------
        None
        """

        # Vector defining the direction of the bar
        direction = (self.end[0][self.l - 1] - self.start[0][self.l - 1], 
                     self.end[1][self.l - 1] - self.start[1][self.l - 1],
                     self.end[2][self.l - 1] - self.start[2][self.l - 1])

        # The (vector) length of the bar
        magnitude = sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)

        # Build the bar at the specified location, in the specified direction, for the specified length
        return cq.Workplane(cq.Plane(origin=(self.start[0][self.l - 1], self.start[1][self.l - 1], self.start[2][self.l - 1]),
                                     xDir=(1,0,0),
                                     normal=direction)).rect(self.bar_w, self.bar_h).extrude(magnitude)
