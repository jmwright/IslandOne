from math import pi, cos, sin
import cadquery as cq

class IslandOne():
    # The major radii of the torus
    r = 5000
    R = 10000

    # Measures of complexity
    q_units = 12 # in the i direction
    p_units = 6 # in the k direction

    """
    Calculates the phi angle for the R radius.
    """
    def phi_l(self, l, i, k):
        return ((2 * i) + (l - 1)) * (pi / self.q_units)

    """
    Calculates the theta angle for the r radius.
    """
    def theta_l(self, l, i, k):
        return ((2 * k) + l) * (pi / self.p_units)
        
    """
    Calculates the radius to the centerline of the torus.
    """
    def Rl(self, l, i, k):
        phi = self.phi_l(l, i, k)

        return (self.R * cos(phi), self.R * sin(phi), 0)
    
    """
    Calculates the radius of the torus pressure tube.
    """
    def rl(self, l, i, k):
        # Get the angles of the R and r radii
        phi = self.phi_l(l, i, k)
        theta = self.theta_l(l, i, k)
        
        return (self.r * cos(theta) * cos(phi),
                self.r * cos(theta) * sin(phi),
                -self.r * sin(theta))
    
    """
    Returns the 3D representation of a connectivity node.
    """
    def node(self, pos):
        return cq.Workplane("XY").box(500, 500, 500).translate(pos)
    
    def build(self):
        # How far to revolve the structure (cutaway vs whole)
        rev_angle = 360
        
        # Pressurized torus
        torus = (cq.Workplane('YZ')
                    .center(-self.R, 0)
                    .circle(self.r)
                    .circle(self.r - 10)
                    .revolve(rev_angle, [self.R, 0], [self.R, 1], clean=True))
        
        # Ground of torus habitat
        ground = (cq.Workplane('ZY')
                    .center(0, -self.R)
                    .rect(self.r * 2., 100)
                    .revolve(rev_angle, [0, self.R], [1, self.R], clean=True))
        
        # Stand-in for a human male of average height
        person = (cq.Workplane('YZ')
                    .circle(400)
                    .extrude(1753))
        
        # Person on the other side of the torus
        person2 = person.translate((0, 0, -self.R * 2.)).rotate((0, 0, 0), (1, 0, 0), 180)
        
        # Add placeholders for the nodes of the connectivity matrix
        #node1 = 
        
        show_object(torus, options={"alpha":0.9, "color": (64, 164, 223)})
        show_object(ground, options={"alpha":0.9, "color": (44, 176, 55)})
        show_object(person, options={"alpha":0.0, "color": (37, 29, 22)})
        show_object(person2, options={"alpha":0.0, "color": (68, 59, 49)})
        
        # Draw all the n1 and n2 nodes
        for l in range(1, 3):
            # Step through all the q and p units and place the nodes for them
            for i in range(0, self.q_units):
                for k in range(0, self.p_units):
                    # Add the components of both radius vectors
                    radii_tuple = tuple(map(sum, zip(self.Rl(l, i, k), self.rl(l, i, k))))

                    show_object(self.node(radii_tuple), options={"alpha":0.5, "color": (255, 255, 255)})

# Trigger the build and render
IslandOne().build()