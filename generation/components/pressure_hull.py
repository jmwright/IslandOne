import cadquery as cq

class PressureHull:
    R = None
    r = None
    cutaway = False
    rev_angle = 360
    torus = None

    def __init__(self, R, r, cutaway=False):
        self.R = R
        self.r = r
        self.cutaway = cutaway

        # If the caller wants a cutaway view, do not revolve the who 360 degrees
        if cutaway:
            self.rev_angle = 180

        return None

    def get(self):
        return (cq.Workplane('YZ')
                    .center(-self.R, 0)
                    .circle(self.r)
                    .circle(self.r - (self.r * 0.01))
                    .revolve(self.rev_angle, [self.R, 0], [self.R, 1], clean=True))