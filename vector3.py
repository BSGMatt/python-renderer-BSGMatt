import numpy
class Vector3:

    def __init__(self, x: float, y: float, z: float):
        self.x = x;
        self.y = y;
        self.z = z;

    def __str__(self):
        return f'({self.x}, {self.y}, {self.z})'
    
    def equals(self, x: float, y: float, z: float):
        return self.x == x and self.y == y and self.z == z;

    def from_list(l: list):
        if (len(l) < 3): return None;
        return Vector3(l[0], l[1], l[2]);

    def as_numpy_array(self):
        return numpy.array([self.x, self.y, self.z]);

    #returns a normalized version of this vector
    def normalized(self):
        mag = self.magnitude();
        return Vector3(self.x / mag, self.y / mag, self.z / mag);

    def magnitude(self):
        mag_sq = self.x**2 + self.y**2 + self.z**2;
        return numpy.sqrt([mag_sq])[0];


    from_list = staticmethod(from_list);
    __repr__ = __str__

class Vertex:

    def __init__(self, idx, x: float, y: float, z: float):
        self.position = Vector3(x, y, z);
        self.index = idx;
        self.normal = numpy.array([0.0,0.0,0.0]);

    def __str__(self):
        return f'{self.position}'
    
    def as_array(self):
        return self.position.as_numpy_array();
    
    __repr__ = __str__


#Structure containing 3 ID's representing the Vertex ID's in a mesh. 
class Triangle:

    def __init__(self, a: int, b: int, c: int):
        self.a = a;
        self.b = b;
        self.c = c;

    def __str__(self):
        return f'[{self.a}, {self.b}, {self.c}]';
    
    def as_list(self):
        return [self.a, self.b, self.c];

    __repr__ = __str__