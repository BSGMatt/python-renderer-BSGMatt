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
        print("Correct usage: spheremaptest.py [mesh_path] [texture_path] [render_mode]");
    
    screen = Screen(500,500)

    camera = PerspectiveCamera(1.0, -1.0, -1.0, 1.0, -1.0, -10)
    camera.transform.set_position(0, 2.5, 0)


    mesh = Mesh.from_stl(sys.argv[1], np.array([1.0, 1.0, 1.0]),\
        np.array([1.0, 1.0, 1.0]),0.2,1.0,1.0,10)
    mesh.transform.set_rotation(0, 45, 0)
    
    mesh.sphere_uvs()
    mesh.load_texture(TEX_MODE_SPHEREMAP, sys.argv[2]);

    light = PointLight(100.0, np.array([1, 1, 1]))
    light.transform.set_position(0, 5, 5)

    renderer = Renderer(screen, camera, [mesh], light)
    
    #Optional arg for rendering mode. 
    render_mode = "spheremap"; #No additional lighting, just the texture
    if (num_args > 3):
        val = int(sys.argv[3]);
        if (val == 1):
            render_mode = "spheremap-spec-diff"; #Texture + diffuse + ambient + specular
        if (val == 2):
            render_mode = "spheremap-spec"; #Texture + ambient + specular
    
    #Save render result to image.
    file_path = "renders/spheremap_render_" + time.strftime("%b_%d_%Y_%H_%M_%S.png", time.gmtime());
    
    if (num_args >= 4):
        file_path = sys.argv[4];
    
    renderer.render(render_mode,[80,80,80], [0.5, 0.5, 0.5])
    
    screen.show();
    
    if (file_path != "none"):
    
        #Flip render result to match results from window. 
        render = renderer.screen.image_buffer.astype(np.uint8);
        render = np.flipud(render);
            
        img = Image.fromarray(render);
        img.save(file_path);
    
    
    