import cadquery as cq

class Node:
    """
    Single connectivity node of the tensegrity structure that makes up the skeletal frame of the toroidal
    pressure hull. Each node is modelled as a frictionless ball joint in calculations. Each node has only
    a position that fixes it in space at the intersection of two bars and four strings.

    Attributes
    ----------
    pos : numpy.array
        A matrix containing the positions for both of the DHT ik unit nodes (1 and 2).
    l : int
        Selects which DHT ik unit bar to work with (1 or 2).
    r : float
        The radius of the pressurized habitat torus.
    simplified : bool
        Whether or not to use simplified primitives to decrease generation and rendering time.
    """

    pos = None
    l = None
    simplified = False
    node_r = None

    def __init__(self, pos, l, r, simplified=False):
        """
        Collects the attributes that allows the tensegrity connectivity node to be constructed.

        Parameters
        ----------
        pos : numpy.array
            A matrix containing the positions for both of the DHT ik unit nodes (1 and 2).
        l : int
            Selects which DHT ik unit bar to work with (1 or 2).
        r : float
            The radius of the pressurized habitat torus.
        simplified : bool
            Whether or not to use simplified primitives to decrease generation and rendering time.
        """

        self.pos = pos
        self.l = l
        self.simplified = simplified

        # The radius of the connection nodes is based on the pressure hull radius
        self.node_r = r / 50.0

    def get(self):
        """
        Constructs the CadQuery object the represents a tensegrity node with the correct
        position and size, depending on whether it is simplified (cube) or not (sphere).

        Parameters
        ----------
        None
        """

        new_node = None

        # If the node is simplified it is a cube, otherwise it is a sphere
        if self.simplified:
            new_node = cq.Workplane().box(self.node_r * 2.0, self.node_r * 2.0, self.node_r * 2.0)
        else:
            new_node = cq.Workplane().sphere(self.node_r)
        
        return new_node.translate((self.pos[0][self.l - 1], self.pos[1][self.l - 1], self.pos[2][self.l - 1]))