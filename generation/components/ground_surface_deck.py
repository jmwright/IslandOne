from math import sqrt
import cadquery as cq

class GroundSurfaceDeck:
    R = None
    r = None
    plane_width = None
    plane_thickness = None
    rev_angle = 360.0

    def __init__(self, R, r, cutaway=False):
        self.R = R
        self.r = r

        # Calculate the plane dimesions based on the pressure hull radius
        self.plane_thickness = r * 0.07 # 0.07 is taken as a proportion from Figure 4.3, pg 24 of Growth Adapted Tensegrity Structure

        # Position ground deck so that basement deck will have the proper headroom
        self.g_deck_center_line = (self.R + self.r) - 0.5 - 2.7 - self.plane_thickness

        # Calculate the width of the ground surface deck based on the radius (the ground deck is not at R)
        # 0.93 is a correction factor that is used to make sure the deck does not interfere with any of the
        # bars or strings from the structure. Ideally this would be calculated based on the string and bar
        # locations. 
        sq = self.r**2 - (self.r / 3.0)**2
        self.plane_width = 2 * sqrt(sq) * 0.93

        # If a cutaway has been selected, only revolve 180 degrees
        if cutaway:
            self.rev_angle = 180.0

    def get(self):
        return (cq.Workplane("YZ")
                  .center(-self.g_deck_center_line, 0)
                  .rect(self.plane_thickness, self.plane_width)
                  .revolve(self.rev_angle, [self.g_deck_center_line, 0], [self.g_deck_center_line, 1], clean=True))