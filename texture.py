from PIL import Image
import numpy as np

TEX_MODE_CUSTOM = -1
TEX_MODE_QUAD = 0
TEX_MODE_SPHEREMAP = 1
TEX_MODE_CUBEMAP_REFLECT = 2
TEX_MODE_CUBEMAP_DIRECT = 3

CUBEMAP_NEG_Z = 0
CUBEMAP_POS_Z = 1
CUBEMAP_NEG_X = 2
CUBEMAP_POS_X = 3
CUBEMAP_NEG_Y = 4
CUBEMAP_POS_Y = 5

#Class for handling loading and accessing texture images
class Texture:
    
    images = [];
    
    #Constructor 
    def __init__(self, tex_mode, *img_paths):
        print(img_paths);
        for img in img_paths:
            i = Image.open(img).convert('RGB');
            self.images.append(i);
            
        self.tex_mode = tex_mode;
            
    #Calculates the uv-coordinates and returns a numpy array of the color at that coordinate. 
    #Arguments depend on the texture mode, 
    def get_color(self, *tex_args):
        
        if (self.tex_mode == TEX_MODE_QUAD):
            return self.quad_uv(tex_args[0], tex_args[1], tex_args[2], tex_args[3], tex_args[4]);
        if (self.tex_mode == TEX_MODE_SPHEREMAP):
            return self.spheremap_uv(tex_args[0], tex_args[1]);
        if (self.tex_mode == TEX_MODE_CUBEMAP_REFLECT):
            return self.cubemap_reflect_uv(tex_args[0], tex_args[1]);
        if (self.tex_mode == TEX_MODE_CUBEMAP_DIRECT):
            return self.cubemap_direct_uv(tex_args[0]);
            
        
        return self.custom_uv(0, tex_args[0]);
    
    def custom_uv(self, imgIdx, UV):
        px_coords = (round((UV[0] * self.images[imgIdx].width - 0.5)), round((UV[1] * self.images[imgIdx].height - 0.5)))
        r, g, b = self.images[imgIdx].getpixel(px_coords);
        return np.array([r,g,b]);
    
    def quad_uv(self, Z, P, alpha, beta, gamma):
        
        interp_Z = alpha * Z[0] +  beta * Z[1] +  gamma * Z[2];
        uv_coords = (alpha * P[0] + beta * P[1] + gamma * P[2]) / interp_Z;
                                
        return self.custom_uv(0, uv_coords);
    
    def spheremap_uv(self, N, E):
        
        #Use eye and surface normal to calculate the reflect vector. 
        R = E - 2 * np.dot(N, E) * N;
        
        #print(R);
                                
        #Taken from this pdf: https://web.cse.ohio-state.edu/~shen.94/781/Site/Slides_files/env.pdf
        #Used to map the reflect vector to a position of a sphere map. 
        #This version is slightly modified to account for our render's coordinate system. (Z is up, Camera looks down negative Y) 
        M = 2*np.sqrt(R[0]**2 + (R[1]-1)**2 + R[2]**2) #We use Ry - 1 because our camera looks down -Y
        uv = np.array([R[0] / M + 0.5, R[2] / M + 0.5]);
        
        return self.custom_uv(0, uv);
    
    def cubemap_reflect_uv(self, N, E):
        
        #Use eye and surface normal to calculate the reflect vector. 
        R = E - 2 * np.dot(N, E) * N;
        #print(f"R: {R}");
        
        #Find the largest component of R
        max_comp = 0;
        if (abs(R[1]) > abs(R[max_comp])): max_comp = 1;
        if (abs(R[2]) > abs(R[max_comp])): max_comp = 2;
        
        #print(f"max_comp: {R[max_comp]}");
        
        img_index = CUBEMAP_POS_Z;
        new_R = R / abs(R[max_comp]);
        
        #print(f"New R: {new_R}");
        uv = [];
        
        #X faces
        if (max_comp == 0):
            if (R[0] < 0):
                #print("R faces -X plane");
                img_index = CUBEMAP_NEG_X;
                uv = np.array([new_R[1], new_R[2]]);
            else:
                #print("R faces +X plane");
                img_index = CUBEMAP_POS_X;
                uv = np.array([-new_R[1], new_R[2]]);
        elif (max_comp == 1):
            if (R[1] < 0):
                #print("R faces -Y plane");
                img_index = CUBEMAP_POS_Y;
                uv = np.array([-new_R[0], new_R[2]]);
            else:
                #print("R faces +Y plane");
                img_index = CUBEMAP_NEG_Y;
                uv = np.array([new_R[0], new_R[2]]);
        else:
            if (R[2] < 0):
                #print("R faces -Z plane");
                img_index = CUBEMAP_NEG_Z;
                uv = np.array([new_R[0], new_R[1]]);
            else:
                #print("R faces +Z plane");
                img_index = CUBEMAP_POS_Z;
                uv = np.array([new_R[0], -new_R[1]]);
                
        uv[0] = uv[0]/2 + 0.5;
        uv[1] = -(uv[1]/2 + 0.5);
        
        #print(f"Image Index, UV: {img_index}, {uv}");
            
        return self.custom_uv(img_index, uv);
    
    def cubemap_direct_uv(self, N):
        
        #print(f"N: {N}");
        
        #Find the largest component of N
        max_comp = 0;
        if (abs(N[1]) > abs(N[max_comp])): max_comp = 1;
        if (abs(N[2]) > abs(N[max_comp])): max_comp = 2;
        
        #print(f"max_comp: {R[max_comp]}");
        
        img_index = CUBEMAP_POS_Z;
        N = N / abs(N[max_comp]);
        
        #print(f"New N: {N}");
        
        if (max_comp == 0):
            if (N[0] < 0):
                #print("R faces -X plane");
                img_index = CUBEMAP_POS_X;
                uv = np.array([N[1], N[2]]);
            else:
                #print("R faces +X plane");
                img_index = CUBEMAP_NEG_X;
                uv = np.array([-N[1], N[2]]);
        elif (max_comp == 1):
            if (N[1] < 0):
                #print("R faces -Y plane");
                img_index = CUBEMAP_POS_Y;
                uv = np.array([-N[0], N[2]]);
            else:
                #print("R faces +Y plane");
                img_index = CUBEMAP_NEG_Y;
                uv = np.array([N[0], N[2]]);
        else:
            if (N[2] < 0):
                #print("R faces -Z plane");
                img_index = CUBEMAP_POS_Z;
                uv = np.array([N[0], N[1]]);
            else:
                #print("R faces +Z plane");
                img_index = CUBEMAP_NEG_Z;
                uv = np.array([N[0], -N[1]]);
                
        uv[0] = -(uv[0]/2 + 0.5);
        uv[1] = (uv[1]/2 + 0.5);
        
        #print(f"Image Index, UV: {img_index}, {uv}");
            
        return self.custom_uv(img_index, uv);
    
    #Creates a Texture object containing the spliced images from the original cubemap texture.
    @staticmethod
    def create_cubemap(map_path, tex_mode):
        
        ret = Texture(tex_mode);
        
        #Assume the cubemap is in the 'sideways cross format'
        cubemap = Image.open(map_path).convert('RGB');
        
        #Convert the image into a 3D array of values
        cmap_array = np.asarray(cubemap);
        cmap_array = np.flipud(cmap_array)
        
        print(np.shape(cmap_array));
        
        cb_sector_w = cubemap.width // 4;
        cb_sector_h = cubemap.height // 3;
        
        cb_images = [];
        
        #Extract +Z (top face)
        z_face = np.empty((cb_sector_h, cb_sector_w, 3), dtype=np.uint8);
        for y in range(2 * (cb_sector_h), 3 * (cb_sector_h)):
            for x in range(1 * (cb_sector_w), 2 * (cb_sector_w)):
                #print(cmap_array[y][x]);
                z_face[y % (cb_sector_h)][x % (cb_sector_w)] = cmap_array[y][x];
                
        cb_images.append(Image.fromarray(z_face, mode='RGB'));
                
        #Extract -Z (bottom face)
        z_face = np.empty((cb_sector_h, cb_sector_w, 3), dtype=np.uint8);
        for y in range(0, 1 * (cb_sector_h)):
            for x in range(1 * (cb_sector_w), 2 * (cb_sector_w)):
                #print(cmap_array[y][x]);
                z_face[y % (cb_sector_h)][x % (cb_sector_w)] = cmap_array[y][x];
        
        cb_images.append(Image.fromarray(z_face, mode='RGB'));
        
        #Extract +X (left face)
        z_face = np.empty((cb_sector_h, cb_sector_w, 3), dtype=np.uint8);
        for y in range(1 * (cb_sector_h), 2 * (cb_sector_h)):
            for x in range(0, 1 * (cb_sector_w)):
                #print(cmap_array[y][x]);
                z_face[y % (cb_sector_h)][x % (cb_sector_w)] = cmap_array[y][x];
        
        cb_images.append(Image.fromarray(z_face, mode='RGB'));
        
        #Extract -X (right face)
        z_face = np.empty((cb_sector_h, cb_sector_w, 3), dtype=np.uint8);
        for y in range(1 * (cb_sector_h), 2 * (cb_sector_h)):
            for x in range(2 * (cb_sector_w), 3 * (cb_sector_w)):
                #print(cmap_array[y][x]);
                z_face[y % (cb_sector_h)][x % (cb_sector_w)] = cmap_array[y][x];
        
        cb_images.append(Image.fromarray(z_face, mode='RGB'));
        
        #Extract +Y (front face)
        z_face = np.empty((cb_sector_h, cb_sector_w, 3), dtype=np.uint8);
        for y in range(1 * (cb_sector_h), 2 * (cb_sector_h)):
            for x in range(1 * (cb_sector_w), 2 * (cb_sector_w)):
                #print(cmap_array[y][x]);
                z_face[y % (cb_sector_h)][x % (cb_sector_w)] = cmap_array[y][x];
        
        cb_images.append(Image.fromarray(z_face, mode='RGB'));
        
        #Extract -Y (back face)
        z_face = np.empty((cb_sector_h, cb_sector_w, 3), dtype=np.uint8);
        for y in range(1 * (cb_sector_h), 2 * (cb_sector_h)):
            for x in range(3 * (cb_sector_w), 4 * (cb_sector_w)):
                #print(cmap_array[y][x]);
                z_face[y % (cb_sector_h)][x % (cb_sector_w)] = cmap_array[y][x];
        
        cb_images.append(Image.fromarray(z_face, mode='RGB'));
        
        ret.images = cb_images;
        
        for i in ret.images:
            print(f'W: {i.width}, H: {i.height}');
        
        return ret;