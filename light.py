from transform import Transform;
import numpy as np;

class PointLight():
    
    def __init__(self, intensity, color):
        self.transform = Transform();
        self.intensity = intensity;
        self.color = color;