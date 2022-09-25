from vec3 import *
from math import floor, sin, pi, cos

class Volume():
    def Normal(self, pos):
        eps = 0.001

        v1 = Vector3(self.SDF(pos + Vector3(eps,0,0)), 
                    self.SDF(pos + Vector3(0,eps,0)), 
                    self.SDF(pos + Vector3(0,0,eps)))

        v2 = Vector3(self.SDF(pos - Vector3(eps,0,0)), 
                    self.SDF(pos - Vector3(0,eps,0)), 
                    self.SDF(pos - Vector3(0,0,eps)))

        return (v1 - v2).unit_vector()

class Sphere(Volume):
    def __init__(self, pos, radius, colour):
        self.pos = pos
        self.radius = radius
        self.colour = colour

    def SDF(self, castpos):
        return (self.pos - castpos).magnitude() - self.radius

    def Colour(self, pos):
        return self.colour

class WavySphere(Volume):
    def __init__(self, pos, radius, amplitude, colour):
        self.pos = pos
        self.radius = radius
        self.amplitude = amplitude
        self.colour = colour

    def SDF(self, castpos):
        dot1 = Vector3(0, 0, 1).dot((castpos - self.pos).unit_vector())
        dot2 = Vector3(1, 0, 0).dot((castpos - self.pos).unit_vector())
        dot3 = Vector3(0, 1, 0).dot((castpos - self.pos).unit_vector())

        finaldot = dot1 - dot2 + dot3

        return (self.pos - castpos).magnitude() - (self.radius + sin(finaldot * 4 * pi) * self.amplitude)

    def Colour(self, pos):
        return self.colour

class Plane(Volume):
    def __init__(self, pos, colour1, colour2):
        self.pos = pos
        self.colour1 = colour1
        self.colour2 = colour2

    def SDF(self, castpos):
        return castpos.z - self.pos.z

    def Colour(self, pos):
        if floor(pos.x) % 2 != floor(pos.y) % 2:
            return self.colour1
        else:
            return self.colour2

class WavyPlane(Volume):
    def __init__(self, pos, colour1, colour2):
        self.pos = pos
        self.colour1 = colour1
        self.colour2 = colour2

    def SDF(self, castpos):
        return castpos.z - (self.pos.z + sin(castpos.x * pi) * 0.1 + cos(castpos.y * pi) * 0.1)

    def Colour(self, pos):
        if floor(pos.x) % 2 != floor(pos.y) % 2:
            return self.colour1
        else:
            return self.colour2

class Torus(Volume):
    def __init__(self, pos, radius, thickness, colour):
        self.pos = pos
        self.radius = radius
        self.thickness = thickness
        self.colour = colour

    def SDF(self, pos):
        unittopos = (pos - self.pos)
        unittopos.z = 0
        unittopos = unittopos.unit_vector()

        pointintorus = self.pos + unittopos * self.radius
        intorustopos = pos - pointintorus
        mag = intorustopos.magnitude()

        return mag - self.thickness

    def Colour(self, pos):
        return self.colour

class Union(Volume):
    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2

    def SDF(self, castpos):
        return min(self.v1.SDF(castpos), self.v2.SDF(castpos))

    def Colour(self, pos):
        v1, v2 = self.v1.SDF(pos), self.v2.SDF(pos)
        return self.v1.Colour(pos) if v1 < v2 else self.v2.Colour(pos)

class SmoothUnion(Volume):
    def __init__(self, v1, v2, k):
        self.v1 = v1
        self.v2 = v2
        self.k = k

    def SDF(self, castpos):
        v1, v2 = self.v1.SDF(castpos), self.v2.SDF(castpos)
        
        h = max(self.k - abs(v1 - v2), 0) / self.k
        return min(v1, v2) - h*h*h*self.k/6.0

    def Colour(self, pos):
        return Vector3(255, 0, 0)
        v1, v2 = self.v1.SDF(pos), self.v2.SDF(pos)
        return self.v1.Colour(pos) if v1 < v2 else self.v2.Colour(pos)