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
        print("Correct usage: spheremaptest.py [mesh_path] [texture_path]");
    
    screen = Screen(400,400)

    camera = PerspectiveCamera(1.0, -1.0, -1.0, 1.0, -1.0, -10)
    camera.transform.set_position(0, 2.5, 0)


    mesh = Mesh.from_stl(sys.argv[1], np.array([1.0, 0.0, 1.0]),\
        np.array([1.0, 1.0, 1.0]),0.05,1.0,1.0,10)
    mesh.transform.set_rotation(0, 45, 0)
    
    mesh.sphere_uvs()
    mesh.load_texture(TEX_MODE_CUBEMAP, sys.argv[2]);

    light = PointLight(100.0, np.array([1, 1, 1]))
    light.transform.set_position(0, 5, 5)
    
    renderer = Renderer(screen, camera, [mesh], light)
    
    renderer.render("cubemap",[80,80,80], [0.5, 0.5, 0.0])

    screen.show()
    