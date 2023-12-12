#This script is for comparing the rendering times of the different modes. 

import numpy as np
import sys

from screen import Screen
from camera import PerspectiveCamera,OrthoCamera
from mesh import Mesh
from renderer import Renderer
from light import PointLight
from texture import *
from PIL import Image
import time
import copy

if __name__ == '__main__':
    
    num_args = len(sys.argv);
    
    if (num_args < 3):
        print("Correct usage: compare_render.py [mesh_path]");
    
    screen = Screen(500,500)

    camera = PerspectiveCamera(1.0, -1.0, -1.0, 1.0, -1.0, -10)
    camera.transform.set_position(0, 2.5, 0)
    
    #-----------------------------------------------SPHEREMAP

    spheremesh = Mesh.from_stl(sys.argv[1], np.array([1.0, 1.0, 1.0]),\
        np.array([1.0, 1.0, 1.0]),0.2,1.0,1.0,10)
    spheremesh.transform.set_rotation(0, 0, 0)
    
    spheremesh.sphere_uvs()
    spheremesh.load_texture(TEX_MODE_SPHEREMAP, "test_images/bar.jpg");

    light = PointLight(100.0, np.array([1, 1, 1]))
    light.transform.set_position(0, 5, 5)

    renderer = Renderer(screen, camera, [spheremesh], light)
    
    start_time = time.time_ns();
    
    renderer.render("spheremap-spec-diff", [80,80,80], [0.5, 0.5, 0.5])
    
    render_time = (time.time_ns() - start_time) / 1000000;
    
    print(f"\nRENDERING_TIME: {render_time} milliseconds");
    
    #-----------------------------------------------CUBEMAP
    
    spheremesh = Mesh.from_stl(sys.argv[1], np.array([1.0, 1.0, 1.0]),\
        np.array([1.0, 1.0, 1.0]),0.2,1.0,1.0,10)
    spheremesh.transform.set_rotation(0, 0, 0)
    
    spheremesh.sphere_uvs()
    spheremesh.load_texture(TEX_MODE_CUBEMAP_REFLECT, "test_images/cubemaps/yokohama.jpg");

    light = PointLight(100.0, np.array([1, 1, 1]))
    light.transform.set_position(0, 5, 5)

    renderer = Renderer(screen, camera, [spheremesh], light)
    
    start_time = time.time_ns();
    
    renderer.render("cubemap", [80,80,80], [0.5, 0.5, 0.5])
    
    render_time = (time.time_ns() - start_time) / 1000000;
    
    print(f"\nRENDERING_TIME: {render_time} milliseconds");
    
    #-----------------------------------------------NO TEXTURE
    
    spheremesh = Mesh.from_stl(sys.argv[1], np.array([1.0, 1.0, 1.0]),\
        np.array([1.0, 1.0, 1.0]),0.2,1.0,1.0,10)
    spheremesh.transform.set_rotation(0, 0, 0)
    
    spheremesh.sphere_uvs()
    #spheremesh.load_texture(TEX_MODE_CUBEMAP_REFLECT, "test_images/cubemaps/yokohama.jpg");

    light = PointLight(100.0, np.array([1, 1, 1]))
    light.transform.set_position(0, 5, 5)

    renderer = Renderer(screen, camera, [spheremesh], light)
    
    start_time = time.time_ns();
    
    renderer.render("blinn-phong", [80,80,80], [0.5, 0.5, 0.5])
    
    render_time = (time.time_ns() - start_time) / 1000000;
    
    print(f"\nRENDERING_TIME: {render_time} milliseconds");
    
    
    