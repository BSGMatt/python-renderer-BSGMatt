from transform import Transform
import numpy as np;


class Camera():
    
    transform = None;
    
    def __init__(self, left, right, bottom, top, near, far):
        pass
    
    def ratio(self):
        return (self.left - self.right) / (self.top - self.bottom);
    
    def project_point(self, p):
        pass
        
    def inverse_project_point(self, p):
        pass
    
    

class OrthoCamera(Camera):

    ortho_transform = None;
    inverse_ortho_transform = None;

    def __init__(self, left, right, bottom, top, near, far):

        self.left = left;
        self.right = right;
        self.top = top;
        self.bottom = bottom;
        self.near = near;
        self.far = far;

        self.transform = Transform();
        self.ortho_transform = np.identity(4);
        self.ortho_transform[0] = np.array([2/(right - left), 0, 0, -((right + left)/(right - left))]);
        self.ortho_transform[1] = np.array([0, 0, 2/(top - bottom), -((top + bottom)/(top - bottom))]);
        self.ortho_transform[2] = np.array([0, 2/(near - far), 0, -((near + far)/(near - far))]);

        self.inverse_ortho_transform = np.linalg.inv(self.ortho_transform);

        return;

    def project_point(self, p):

        #Convert from world space to camera space:
        cam_p = self.transform.apply_inverse_to_point(p);
        cam_p = np.append(cam_p, 1);

        #Convert from camera space to normal viewport space
        norm_p = np.dot(self.ortho_transform, cam_p);
        return norm_p[:3];

    def inverse_project_point(self, p):
        p = np.append(p, 1);
        inv_p = np.dot(self.inverse_ortho_transform, p);
        return self.transform.apply_to_point(inv_p[:3]);
    
class PerspectiveCamera(Camera):
    
    ortho_transform = None;
    pers_transform = None;
    inv_ortho_transform = None;
    inv_pers_transform = None;
    
    def __init__(self, left, right, bottom, top, near, far):

        self.left = left;
        self.right = right;
        self.top = top;
        self.bottom = bottom;
        self.near = near;
        self.far = far;

        self.transform = Transform();
        self.ortho_transform = np.identity(4);
        self.ortho_transform[0] = np.array([2/(right - left), 0, 0, -((right + left)/(right - left))]);
        self.ortho_transform[1] = np.array([0, 0, 2/(top - bottom), -((top + bottom)/(top - bottom))]);
        self.ortho_transform[2] = np.array([0, 2/(near - far), 0, -((near + far)/(near - far))]);
        
        print(self.ortho_transform);
        
        self.pers_transform = np.zeros((4,4));
        self.pers_transform[0] = np.array([near, 0, 0, 0]);
        self.pers_transform[1] = np.array([0,(near + far), 0, -(far * near)]);
        self.pers_transform[2] = np.array([0, 0, near, 0]);
        self.pers_transform[3] = np.array([0, 1, 0, 0]);
        
        print(self.pers_transform);
        
        self.inv_ortho_transform = np.linalg.inv(self.ortho_transform);
        self.inv_pers_transform = np.linalg.inv(self.pers_transform);
        
        return;
    
    def project_point(self, p):

        #Convert from world space to camera space:
        cam_p = self.transform.apply_inverse_to_point(p);
        cam_p = np.append(cam_p, 1);

        #Convert from camera space to normal viewport space
        norm_p = np.dot(self.pers_transform, cam_p);
        norm_p = np.divide(norm_p, norm_p[3]);
        norm_p = np.dot(self.ortho_transform, norm_p);
        
        return norm_p[:3];

    def inverse_project_point(self, p):
        #Un-applying O
        p = np.append(p, 1);
        inv_p = np.dot(self.inv_ortho_transform, p);
        
        #Un-applying P
        y = -(self.near * self.far) / (inv_p[1] - (self.near + self.far));
        inv_p = np.multiply(inv_p, y);
        
        inv_p = np.dot(self.inv_pers_transform, inv_p);
        
        return self.transform.apply_to_point(inv_p[:3]);
    
    
    #Calculates the scalar w, used for perspective correct texture mapping. 
    def calculate_w(self, v):
        
        p = np.append(v, 1);
        
        inv_p = np.dot(self.inv_ortho_transform, p);
        w = (self.near * self.far) / ((self.near + self.far) - inv_p[1]);
        
        return w;
    
    

