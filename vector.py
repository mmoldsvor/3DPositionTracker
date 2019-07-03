import math


class Vector:
    def __init__(self, x=0, y=0, z=0):
        self.x, self.y, self.z = x, y, z

    @property
    def xy(self):
        return self.x, self.y

    @property
    def xz(self):
        return self.x, self.z

    @property
    def yz(self):
        return self.y, self.z

    def set_x(self, x):
        return Vector(x, *self.yz)

    def set_y(self, y):
        return Vector(self.x, y, self.z)

    def set_z(self, z):
        return Vector(*self.xy, z)

    def __getitem__(self, item):
        return (self.x, self.y, self.z)[item]

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, factor):
        return Vector(self.x * factor, self.y * factor, self.z * factor)

    def __truediv__(self, divisor):
        return Vector(self.x / divisor, self.y / divisor, self.z / divisor)

    def __abs__(self):
        return math.sqrt((self.x * self.x) + (self.y * self.y) + (self.z * self.z))

    def angle_between(self, other):
        return math.acos(self.dot(other) / (abs(self) * abs(other)))

    def dot(self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    def cross(self, other):
        return abs(self) * abs(other) * math.sin(self.angle_between(other))

    def normalized(self):
        return self / abs(self)

    def max(self, other):
        return Vector(max(self.x, other.x), max(self.y, other.y), max(self.z, other.z))

    def min(self, other):
        return Vector(min(self.x, other.x), min(self.y, other.y), min(self.z, other.z))

    def __repr__(self):
        return 'Vector({}, {}, {})'.format(self.x, self.y, self.z)

