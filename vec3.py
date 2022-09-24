from math import sqrt


class Vector3(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"

    def __eq__(self, other):
        if not isinstance(other, Vector3):
            return False
        return (self.x == other.x) and (self.y == other.y) and (self.z == other.z)

    def __add__(self, other):
        if isinstance(other, Vector3):
            x = self.x + other.x
            y = self.y + other.y
            z = self.z + other.z
        else:
            x = self.x + other
            y = self.y + other
            z = self.z + other
        return Vector3(x, y, z)

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, Vector3):
            x = self.x - other.x
            y = self.y - other.y
            z = self.z - other.z
        else:
            x = self.x - other
            y = self.y - other
            z = self.z - other
        return Vector3(x, y, z)

    def __rsub__(self, other):
        if isinstance(other, Vector3):
            x = other.x - self.x
            y = other.y - self.y
            z = other.z - self.z
        else:
            x = other - self.x
            y = other - self.y
            z = other - self.z
        return Vector3(x, y, z)

    def __mul__(self, other):
        if isinstance(other, Vector3):
            x = self.x * other.x
            y = self.y * other.y
            z = self.z * other.z
        else:
            x = self.x * other
            y = self.y * other
            z = self.z * other
        return Vector3(x, y, z)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Vector3):
            x = self.x / other.x
            y = self.y / other.y
            z = self.z / other.z
        else:
            x = self.x / other
            y = self.y / other
            z = self.z / other
        return Vector3(x, y, z)

    def __rtruediv__(self, other):
        if isinstance(other, Vector3):
            x = other.x / self.x
            y = other.y / self.y
            z = other.z / self.z
        else:
            x = other / self.x
            y = other / self.y
            z = other / self.z
        return Vector3(x, y, z)

    def magnitude(self):
        x = self.x**2
        y = self.y**2
        z = self.z**2
        return sqrt(x + y + z)

    def dot(self, other):
        a = self.x * other.x
        b = self.y * other.y
        c = self.z * other.z
        return a + b + c

    def cross(self, other):
        x = (self.y * other.z) - (self.z * other.y)
        y = (self.z * other.x) - (self.x * other.z)
        z = (self.x * other.y) - (self.y * other.x)
        return Vector3(x, y, z)

    def unit_vector(self):
        return self / self.magnitude()

    def to_tuple(self):
        return (self.x, self.y, self.z)

    def clamplerp(self, v2, t):
        to = v2 - self
        tval = min(1, max(0, t))
        return self + to * tval