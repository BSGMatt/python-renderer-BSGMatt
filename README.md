# finalProject-BSGMatt
Final Project for Computer Graphics course: reflections and environment mapping.

Code by Matthew Clifton

This project contains four main files:
    **spheremaptest.py, cubemaptest.py, cbgenerator.py, and compare_render.py**

## spheremaptest.py

This renders an image using a spheremap technique. 

### Usage: 

    spheremaptest.py [mesh_path] [texture_path] [render_mode]

Where: 
* **[mesh_path]** is the path of the .stl file to load
* **[texture_path]** is the path of the texture image. 
* **[render_mode]** is an integer to select different lighting conditions:
    * 0 for No lighting (Just the texture)
    * 1 for Specular + Diffuse lighting
    * 2 for just Specular lighting

## cubemaptest.py

This renders an image using a cube technique. 

### Usage: 

    cubemaptest.py [mesh_path] [texture_path] [render_mode] [render_path]

Where: 
* **[mesh_path]** is the path of the .stl file to load
* **[texture_path]** is the path of the texture image. 
* **[render_mode]** is an integer to select different texture modes:
    * 0 for Reflection Mapping
    * 1 for Direct Mapping

## cbgenerator.py

This script will render six meshes, each representing a face of a cube, and output the result to an image. 

### Usage: 

    spheremaptest.py [render_path] [top_mesh] [bottom_mesh] [left_mesh] [right_mesh] [front_mesh] [back_mesh]

Where: 
* **[render_path]** the filename for the final cubemap image. 
* **[top_mesh]** is the mesh to render for the top face. 
* **[bottom_mesh]** is the mesh to render for the bottom face. 
* **[left_mesh]** is the mesh to render for the left face. 
* **[right_mesh]** is the mesh to render for the right face. 
* **[front_mesh]** is the mesh to render for the front face. 
* **[back_mesh]** is the mesh to render for the back face. 

## compare_render.py

This renders a mesh in 2 different modes: Spheremap, Cubemap, and blinn-phong (no textures), outputting the rendering time of each.  

### Usage: 

    compare_render.py [mesh_path] 

Where **[mesh_path]** is the path of the .stl file to load






