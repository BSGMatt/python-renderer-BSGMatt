from PIL import Image
import numpy as np

TEX_MODE_CUSTOM = -1
TEX_MODE_QUAD = 0
TEX_MODE_SPHEREMAP = 1
TEX_MODE_CUBEMAP = 2

#Class for handling loading and accessing texture images
class Texture:
    
    images = [];
    
    #Constructor 
    def __init__(self, tex_mode, *img_paths):
        for img in img_paths:
            self.img = Image.open(img_path);
        self.tex_mode = tex_mode;
            
    #Calculates the uv-coordinates and returns a numpy array of the color at that coordinate. 
    #Arguments depend on the texture mode, 
    def get_color(self, *tex_args):
        
        if (self.tex_mode == TEX_MODE_QUAD):
            return self.quad_uv(tex_args[0], tex_args[1], tex_args[2], tex_args[3], tex_args[4]);
        if (self.tex_mode == TEX_MODE_SPHEREMAP):
            return self.spheremap_uv(tex_args[0], tex_args[1]);
            
        
        return custom_uv(self, tex_args[0]);
    
    def custom_uv(self, UV):
        px_coords = (round((UV[0] * mesh.texture.width - 0.5)), round((-UV[1] * mesh.texture.height - 0.5)))
        r, g, b = mesh.texture.getpixel(px_coords);
        return np.array([r,g,b]);
    
    def quad_uv(self, Z, P, alpha, beta, gamma):
        
        interp_Z = alpha * Z[0] +  beta * Z[1] +  gamma * Z[2];
        uv_coords = (alpha * P[0] + beta * P[1] + gamma * P[2]) / interp_Z;
                                
        return custom_uv(uv_coords);
    
    def spheremap_uv(self, N, E):
        
        #Use eye and surface normal to calculate the reflect vector. 
        R = V - 2 * np.dot(N, V) * N;
                                
        #Taken from this pdf: https://web.cse.ohio-state.edu/~shen.94/781/Site/Slides_files/env.pdf
        #Used to map the reflect vector to a position of a sphere map. 
        #This version is slightly modified to account for our render's coordinate system. (Z is up, Camera looks down negative Y) 
        M = 2*np.sqrt(R[0]**2 + (R[1]-1)**2 + R[2]**2) #We use Ry - 1 because our camera looks down -Y
        uv = np.array([R[0] / M + 0.5, R[2] / M + 0.5]);
        
        return custom_uv(uv);