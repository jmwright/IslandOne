import cadquery as cq
from components.tensegrity_structure import  TensegrityStructure
from components.pressure_hull import PressureHull

# vr (VR scaling in meters) or mm (millimeter scaling)
scale_mode = "VR"

# The complexity values
p = 12 # ik strip
q = 30 # Strips in torus along centerline

# The centerline radius of the torus and the radius of the pressure tube
if scale_mode == "VR":
    r = 5
    R = 10
else:
    r = 5000
    R = 10000

# Add the tensegrity structure
i1 = TensegrityStructure(p, q, R, r, simplified=True).get()

# Add the pressure hull
i1.add(PressureHull(R, r).get(), loc=cq.Location(cq.Vector(0, 0, 0)), color=cq.Color(0.25, 0.64, 0.88, 0.2))

show_object(i1)
