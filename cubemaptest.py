import numpy as np
import sys

from screen import Screen
from camera import PerspectiveCamera,OrthoCamera
from mesh import Mesh
from renderer import Renderer
from light import PointLight
from texture import *


if __name__ == '__main__':
    
    num_args = len(sys.argv);
    
    if (num_args < 3):
        print("Correct usage: cubemaptest.py [mesh_path] [texture_path] [0 for reflect, 1 for direct]");
        sys.exit();
    
    screen = Screen(400,400)

    camera = PerspectiveCamera(1.0, -1.0, -1.0, 1.0, -1.0, -10)
    camera.transform.set_position(0, 2.5, 0)


    mesh = Mesh.from_stl(sys.argv[1], np.array([1.0, 1.0, 1.0]),\
        np.array([1.0, 1.0, 1.0]),0.2,1.0,1.0,100)
    mesh.transform.set_rotation(0, 0, 0)
    
    mesh.sphere_uvs()
    
    tex_mode = TEX_MODE_CUBEMAP_REFLECT;
    if (num_args > 3):
        choice = int(sys.argv[3]);
        if(choice == 1):
            tex_mode = TEX_MODE_CUBEMAP_DIRECT;
            
    print(f"Texture mode: {tex_mode}");
            
    mesh.load_texture(tex_mode, sys.argv[2]);

    light = PointLight(100.0, np.array([1, 1, 1]))
    light.transform.set_position(0, 5, 5)
    
    renderer = Renderer(screen, camera, [mesh], light)
    
    #FOV Stats: fovX = 2*atan[ (right-left)/(2*near) ].
    FOV_H = np.degrees(2 * np.arctan((camera.right - camera.left)/(2*camera.near)))
    print(f"FOV_H: {FOV_H}");
    
    renderer.render("cubemap",[80,80,80], [0.5, 0.5, 0.5])

    screen.show()
    