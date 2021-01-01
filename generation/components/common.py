import cadquery as cq

class Common:
    @staticmethod
    def computeXDir(normal):
        """
        Computes the X direction given the normal.
        """
        xd = cq.Vector(0, 0, 1).cross(cq.Vector(normal))
        if xd.Length < 0.0001:
            # this face is parallel with the x-y plane, so choose x to be in global coordinates
            xd = cq.Vector(1, 0, 0)

        return xd.toTuple()
