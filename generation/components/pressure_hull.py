import cadquery as cq

class PressureHull:
    """
    Stand-in for the as-launched pressure hull on the outside of the tensegrity
    structure and/or the expansion hull on the inside before an expansion.

    Attributes
    ----------
    R : float
        The radius from the center of the station to the center line of the habitat torus.
    r : float
        The radius of the pressurized habitat torus.
    cutaway : bool
        Whether or not the torus should only be revolved 180 degrees so that the inside
        of the torus is visible.
    """

    R = None
    r = None
    cutaway = False
    rev_angle = 360
    torus = None

    def __init__(self, R, r, cutaway=False):
        """
        Captures all the attributes that define how the torus will be constructed.

        Parameters
        ----------
        R : float
            The radius from the center of the station to the center line of the habitat torus.
        r : float
            The radius of the pressurized habitat torus.
        cutaway : bool
            Whether or not the torus should only be revolved 180 degrees so that the inside
            of the torus is visible.
        """

        self.R = R
        self.r = r
        self.cutaway = cutaway

        # If the caller wants a cutaway view, do not revolve the who 360 degrees
        if cutaway:
            self.rev_angle = 180

        return None

    def get(self):
        """
        Constructs the CadQuery object (not an Assembly) representing the pressure hull torus.

        Parameters
        ----------
        None
        """

        return (cq.Workplane('YZ')
                    .center(-self.R, 0)
                    .circle(self.r)
                    .circle(self.r - (self.r * 0.01))
                    .revolve(self.rev_angle, [self.R, 0], [self.R, 1], clean=True))