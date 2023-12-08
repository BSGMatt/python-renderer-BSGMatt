import numpy as np

from screen import Screen
from camera import PerspectiveCamera,OrthoCamera
from mesh import Mesh
from renderer import Renderer
from light import PointLight



if __name__ == '__main__':
    screen = Screen(500,500)

    camera = PerspectiveCamera(1.0, -1.0, -1.0, 1.0, -1.0, -100)
    camera.transform.set_position(0, 2.0, 0)


    mesh1 = Mesh.textured_plane()
    mesh1.load_texture("checker.jpg")


    light = PointLight(50.0, np.array([1, 1, 1]))
    light.transform.set_position(0, 5, 5)

    renderer = Renderer(screen, camera, [mesh1], light)
    renderer.render("flat",[80,80,80], [0.2, 0.2, 0.2])

    screen.show()