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
    
    screen = Screen(500,500)

    camera = PerspectiveCamera(1.0, -1.0, -1.0, 1.0, -1.0, -10)
    camera.transform.set_position(0, 3.5, 0)


    mesh = Mesh.from_stl(sys.argv[1], np.array([1.0, 0.0, 1.0]),\
        np.array([1.0, 1.0, 1.0]),0.05,1.0,1.0,100)
    mesh.transform.set_rotation(0, 0, 0)
    
    mesh.sphere_uvs()
    mesh.load_texture(TEX_MODE_SPHEREMAP, sys.argv[2]);

    light = PointLight(100.0, np.array([1, 1, 1]))
    light.transform.set_position(0, 5, 5)

    renderer = Renderer(screen, camera, [mesh], light)
    
    #Optional arg for rendering mode. 
    render_mode = "spheremap"; #No additional lighting, just the texture
    if (num_args == 4):
        val = int(sys.argv[3]);
        if (val == 1):
            render_mode = "spheremap-spec-diff"; #Texture + diffuse + ambient + specular
        if (val == 2):
            render_mode = "spheremap-spec"; #Texture + ambient + specular
    
    renderer.render(render_mode,[80,80,80], [0.5, 0.5, 0.0])

    screen.show()