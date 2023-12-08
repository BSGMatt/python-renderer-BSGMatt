#This module generates a set of images

import numpy as np
import sys

from screen import Screen
from camera import PerspectiveCamera,OrthoCamera
from mesh import Mesh
from renderer import Renderer
from light import PointLight
from texture import *
from PIL import Image

CUBE_SIZE = 256;
    
def start():
    
    num_args = len(sys.argv);
    
    if (num_args < 3):
        print("Correct usage: cubemaptest.py [mesh_path] [texture_path] [0 for reflect, 1 for direct]");
        sys.exit();
    
    screen = Screen(CUBE_SIZE,CUBE_SIZE)

    camera = PerspectiveCamera(1.0, -1.0, -1.0, 1.0, -1.0, -10)
    camera.transform.set_position(0, 2.5, 0)
    
    light = PointLight(100.0, np.array([1, 1, 1]))
    light.transform.set_position(0, 5, 5)
    
    #floor = Mesh.from_stl("unit_cube.stl", np.array([1,1,1]),\
        #np.array([1.0, 1.0, 1.0]),0.2,1.0,1.0,100)
    #floor.sphere_uvs();
    floor = Mesh.textured_plane()
    floor.diffuse_color = np.array([1,1,1]);
    floor.specular_color = np.array([1.0, 1.0, 1.0]);
    floor.ka = 0.2;
    floor.kd = 1.0;
    floor.ks = 1.0;
    floor.ke = 100;
    floor.transform.set_rotation(45, 0, 0);
    floor.transform.set_position(0, 1.5, -1);

    #Build scene
    renders = [];
    
    mesh_positions = np.array([[0.0, -2.5, 0.0],[-2.5,0.0,0.0],[2.5,0.0,0.0],[0.0,2.5,0.0]])
    mesh_colors = np.array([[1.0, 0.0, 0.0],[0.0,1.0,0.0],[0.0,0.0,1.0],[1.0,1.0,0.0],[1.0,0.0,1.0],[0.0,1.0,1.0]])
    
    mesh_args = sys.argv[1:];
    z_rot = 0;
    
    for i in range(len(mesh_args)):
        mesh = Mesh.from_stl(sys.argv[i+1], mesh_colors[i],\
        np.array([1.0, 1.0, 1.0]),0.2,1.0,1.0,100)
        mesh.sphere_uvs();
    
        renderer = Renderer(screen, camera, [floor, mesh], light)
    
        renderer.render("flat",[80,80,80], [0.5, 0.5, 0.5])
        #screen.show()
        renders.append(renderer.screen.image_buffer);
        
    #Test result by displaying it in the window
    screen = Screen(CUBE_SIZE * 4,CUBE_SIZE * 3)
    img_buffer = build_cubemap(renders)
    screen.draw(img_buffer)
    screen.show();
    
    cubemap_image = Image.fromarray(img_buffer)
    cubemap_image.save("cbgeneratortest.png");
    
    
def build_cubemap(images: np.ndarray):
    
    
    #Create array to store image data
    cubemap_image = np.empty((CUBE_SIZE *3, CUBE_SIZE * 4, 3), dtype=np.uint8);
    
    #TOP PART OF CUBE MAP
    images[0] = np.rot90(images[0]);
    for y in range(CUBE_SIZE):
        for x in range(CUBE_SIZE):
            cubemap_image[y][CUBE_SIZE + x] = images[0][y][x];
            
    #BOTTOM PART OF CUBE MAP
    images[1] = np.rot90(images[1]);
    for y in range(CUBE_SIZE):
        for x in range(CUBE_SIZE):
            cubemap_image[(CUBE_SIZE * 2) + y][CUBE_SIZE + x] = images[1][y][x];
            
    #LEFT PART OF CUBE MAP
    images[2] = np.rot90(images[2]);
    for y in range(CUBE_SIZE):
        for x in range(CUBE_SIZE):
            cubemap_image[(CUBE_SIZE) + y][x] = images[2][y][x];
            
    #RIGHT PART OF CUBE MAP
    images[3] = np.rot90(images[3]);
    for y in range(CUBE_SIZE):
        for x in range(CUBE_SIZE):
            cubemap_image[(CUBE_SIZE) + y][(CUBE_SIZE * 2) + x] = images[3][y][x];
            
    #FRONT PART OF CUBE MAP
    images[4] = np.rot90(images[4]);
    for y in range(CUBE_SIZE):
        for x in range(CUBE_SIZE):
            cubemap_image[(CUBE_SIZE) + y][CUBE_SIZE + x] = images[4][y][x];
            
    #BACK PART OF CUBE MAP
    images[5] = np.rot90(images[5]);
    for y in range(CUBE_SIZE):
        for x in range(CUBE_SIZE):
            cubemap_image[(CUBE_SIZE) + y][(CUBE_SIZE * 3) + x] = images[5][y][x];
            
    cubemap_image = np.flipud(cubemap_image);
    
    return cubemap_image;

if __name__ == '__main__':
    start();
    