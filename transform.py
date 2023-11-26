import numpy as np
from vector3 import *

class Transform:

    def __init__(self):
        self.matrix = np.identity(4);
        return;

    def transformation_matrix(self):
        return self.matrix;
    
    def position(self):
        return self.matrix[:3, 3];

    def set_position(self, x: float, y: float, z: float):
        self.matrix[0][3] = x;
        self.matrix[1][3] = y;
        self.matrix[2][3] = z;
        return;

    def set_rotation(self, x: float, y: float, z: float):

        #BUILD THE ROTATION MATRIX
        x = np.radians(x);
        y = np.radians(y);
        z = np.radians(z);

        r_z = np.identity(4);
        r_y = np.identity(4);
        r_x = np.identity(4);

        #Z-Matrix :
        r_z[0][0] = np.cos(z);
        r_z[0][1] = -np.sin(z);
        r_z[1][0] = np.sin(z);
        r_z[1][1] = np.cos(z);

        #print("Rz matrix: \n{0}".format(r_z));

        #Y-Matrix:
        r_y[0][0] = np.cos(y);
        r_y[0][2] = np.sin(y);
        r_y[2][0] = -np.sin(y);
        r_y[2][2] = np.cos(y);

        #print("Ry matrix: \n{0}".format(r_y));

        #X-Matrix:
        r_x[1][1] = np.cos(x);
        r_x[1][2] = -np.sin(x);
        r_x[2][1] = np.sin(x);
        r_x[2][2] = np.cos(x);

        #print("Rx matrix: \n{0}".format(r_x));

        #MULTIPLY MATRICES:
        rotation = np.dot(r_x, r_y);

        #print("Rz * Ry matrix: \n{0}".format(rotation));

        rotation = np.dot(rotation, r_z);

        #print("Final R matrix: \n{0}".format(rotation));

        self.matrix = np.dot(self.matrix, rotation);

        return;

    def inverse_matrix(self):
        return np.linalg.inv(self.matrix);

    def apply_to_point(self, p):
        p = self.ensure_numpy_array(p);
        p4 = np.append(p, 1);
        apply = np.dot(self.matrix, p4);
        return apply[:3];

    def apply_inverse_to_point(self, p):
        p = self.ensure_numpy_array(p);
        p4 = np.append(p, 1);
        apply = np.dot(self.inverse_matrix(), p4);
        return apply[:3];

    def apply_to_normal(self, n):
        n = self.ensure_numpy_array(n);
        p4 = np.append(n, 0);
        apply = np.dot(self.matrix, p4);
        return self.normalize_array(apply[:3]);
    
    def apply_inverse_to_normal(self, n):
        n = self.ensure_numpy_array(n);
        p4 = np.append(n, 0);
        apply = np.dot(self.inverse_matrix(), p4);
        return self.normalize_array(apply[:3]);

    #Converts p into a numpy array, if not
    #so already. 
    def ensure_numpy_array(self, p):
        if (isinstance(p, Vertex)):
            return p.position.as_numpy_array();
        return p;

    def normalize_array(self, p):
        norm_p = np.linalg.norm(p);
        normal = [];
        for i in p:
            normal.append(i / norm_p);
        return np.array(normal);

