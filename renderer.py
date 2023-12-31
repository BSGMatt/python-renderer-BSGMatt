from screen import Screen
from mesh import Mesh
from camera import Camera
from light import PointLight
import numpy as np;
from texture import *
import sys

class Renderer:

    screen = None;
    camera = None;
    meshes = None;
    light = None;

    def __init__(self, screen: Screen, camera: Camera, meshes: list[Mesh], light: PointLight):
        self.screen = screen;
        self.camera = camera;
        self.meshes = meshes;
        self.light = light;

    def render(self, shading, bg_color, ambient_light):
        
        image_buffer = np.full((self.screen.height, self.screen.width, 3), bg_color)
        z_buffer = np.full((self.screen.height, self.screen.width), -np.inf);
        obj_color = np.array([1,1,1]);
        light_pos = self.light.transform.position();
        cam_pos = self.camera.transform.position();
        
        for mesh in self.meshes:
                       
            A = mesh.ka * np.array(ambient_light);
            mesh_pos = mesh.transform.position();
            
            progress = 0;
            max_progress = len(mesh.faces);
            
            print(f"NUM vertices: {len(mesh.verts)}");
                    
            for t in mesh.faces:
                
                sys.stdout.write(f"\rRendering: {progress}/{max_progress}")
                sys.stdout.flush()
                progress += 1;
                
                normal = mesh.transform.apply_to_normal(mesh.find_normal(t).as_numpy_array());
                #normal = normal / np.linalg.norm(normal); #Ensure face normal is normalized after the thing. 
                
                
                vertA_normal = mesh.transform.apply_to_normal(mesh.verts[t.a].normal);
                vertB_normal = mesh.transform.apply_to_normal(mesh.verts[t.b].normal);
                vertC_normal = mesh.transform.apply_to_normal(mesh.verts[t.c].normal);
                
                vert_normals = [vertA_normal, vertB_normal, vertC_normal];
                
                #print(f"A: {vertA_normal}\n, B: {vertB_normal}\n, C: {vertC_normal}\n");
                
                #Used for gourad shading:
                vert_intensities = [];
                vert_positions = []
                if (shading == "gouraud" or shading == "cubemap-direct"):
                    #Calculate the intensities at each vertex. 
                    k = 0;
                    for v_id in t.as_list():
                        
                        v = mesh.transform.apply_to_point(mesh.verts[v_id]);
                        vert_positions.append(v);
                        
                        vL = (light_pos - v) / np.linalg.norm(light_pos - v);
                        V = (cam_pos - v) / np.linalg.norm(cam_pos - v);
                        H = (vL + V) / np.linalg.norm(vL + V);
                                    
                        I_d = (np.array(self.light.color) * self.light.intensity) / (np.linalg.norm(light_pos - v) ** 2)
                        phi_d = (mesh.kd * mesh.diffuse_color * max(0, np.dot(vL, vert_normals[k]))) / np.pi;
                        spec = mesh.ks * (max(0, np.dot(H, vert_normals[k])) ** mesh.ke) * mesh.specular_color;
                        diff = I_d * phi_d;
                        
                        vert_intensities.append(A + diff + spec);
                        k += 1;
                
                
                #Get the device coordinates for each of the triangles vertices. 
                verts_device_coords = [self.camera.project_point(mesh.transform.apply_to_point(mesh.verts[p])) for p in t.as_list()]
                
                #Find the bounding box of each triangle
                min_x = 1000000;
                max_x = -1000000;
                min_y = 1000000;
                max_y = -10000000;
                
                #TODO: determine which pixels to check for rendering triangle (bounding box in screen coordinates)
                screen_coords = [];
                vert_depth = [];
                z_depth = [];
                for p in verts_device_coords:
                    vert_depth.append(p[2]);
                    #print(f'P: {p}');
                    
                    z_depth.append(self.camera.calculate_w(np.copy(p)));
                    
                    #print(f'z: {z_depth[-1]}');
                    
                    s = self.screen.device_to_screen(np.copy(p));
                    #print(f'S: {s}');
                    screen_coords.append(s);
                    if (s[0] < min_x):
                        min_x = round(s[0]);
                    if (s[0] > max_x):
                        max_x = round(s[0]);
                    if (s[1] < min_y):
                        min_y = round(s[1]);
                    if (s[1] > max_y):
                        max_y = round(s[1]);
                
                #print(f"Min: [{min_x},{min_y}], Max: [{max_x},{max_y}]");
                Z = np.array([1 / z_depth[0], 1 / z_depth[1], 1 / z_depth[2]]);
                P = np.array([mesh.uvs[t.a] / z_depth[0], mesh.uvs[t.b] / z_depth[1], mesh.uvs[t.c] / z_depth[2]]);

                #TODO: loop over pixels, check which are inside the triangle and set image_buffer at that pixel = obj_color.

                #The denomitator for gamma and beta are constant, so I'm doing the math for them outside the main loop. 

                gamma_d = ((verts_device_coords[0][1] - verts_device_coords[1][1]) * verts_device_coords[2][0]) + ((verts_device_coords[1][0] - verts_device_coords[0][0]) * verts_device_coords[2][1])+ (verts_device_coords[0][0]*verts_device_coords[1][1] - verts_device_coords[1][0]*verts_device_coords[0][1]) 
                beta_d = ((verts_device_coords[0][1] - verts_device_coords[2][1]) * verts_device_coords[1][0]) + ((verts_device_coords[2][0] - verts_device_coords[0][0]) * verts_device_coords[1][1]) + (verts_device_coords[0][0]*verts_device_coords[2][1] - verts_device_coords[2][0]*verts_device_coords[0][1])

                #print(f"GammaD: {gamma_d}, BetaD: {beta_d}")
                #min_y = max(min_y, 0);
                #min_x = max(max_x, 0);
                #max_x = min(max_x, self.screen.width - 1);
                #max_y = min(max_y, self.screen.height - 1);

                for y in range(min_y, max_y+1):
                    for x in range(min_x, max_x+1):
                        
                        #Rendering progress
                        if (x < 0 or x >= self.screen.width): continue;
                        if (y < 0 or y >= self.screen.height): continue;
                        
                        device_pixel = self.screen.screen_to_device(np.array([x,y,1]));
                        #print(device_pixel);

                        gamma = ((verts_device_coords[0][1] - verts_device_coords[1][1]) * device_pixel[0]) + ((verts_device_coords[1][0] - verts_device_coords[0][0]) * device_pixel[1]) + (verts_device_coords[0][0]*verts_device_coords[1][1] - verts_device_coords[1][0]*verts_device_coords[0][1])
                        gamma = gamma / gamma_d;
                        beta = ((verts_device_coords[0][1] - verts_device_coords[2][1]) * device_pixel[0])  + ((verts_device_coords[2][0] - verts_device_coords[0][0]) * device_pixel[1]) + (verts_device_coords[0][0]*verts_device_coords[2][1] - verts_device_coords[2][0]*verts_device_coords[0][1])
                        beta = beta / beta_d;
                        alpha = 1 - beta - gamma;
                        #print(f'({x},{y}): {alpha} {beta} {gamma}');
                        #print(pixel_depth);
                        
                        if (beta > 0 and gamma > 0 and alpha > 0):
                            
                            pixel_depth = alpha * vert_depth[0] + beta * vert_depth[1] + gamma * vert_depth[2];
                            
                            if (pixel_depth < z_buffer[y][x]):
                                continue;
                        
                            z_buffer[y][x] = pixel_depth;
                            depth = pixel_depth / 2 + 0.5;
                            
                            if (shading == "barycentric"):
                                image_buffer[y][x] = (alpha * 255, beta * 255, gamma * 255);
                            elif (shading == "flat"):
                                
                                p_world = self.camera.inverse_project_point(alpha * verts_device_coords[0] + beta * verts_device_coords[1] + gamma * verts_device_coords[2]);
                                p_to_l = (light_pos - p_world);
                                
                                l = p_to_l / np.linalg.norm(p_to_l)
                                
                                I_d = (np.array(self.light.color) * self.light.intensity) / (np.linalg.norm(p_to_l) ** 2)
                                
                                phi_d = (mesh.kd * mesh.diffuse_color * max(0, np.dot(l, normal))) / np.pi;
                                
                                diff = I_d * phi_d;

                                final_I = (A + diff);
                                final_color = final_I * 255;

                                image_buffer[y][x] = final_color;
                                
                            elif (shading == "phong-blinn"):
                                
                                p_normal = alpha * vertA_normal + beta * vertB_normal + gamma * vertC_normal;
                                N = p_normal / np.linalg.norm(p_normal);
                                p_world = self.camera.inverse_project_point(alpha * verts_device_coords[0] + beta * verts_device_coords[1] + gamma * verts_device_coords[2]);
                                p_to_l = (light_pos - p_world);
                                
                                L = p_to_l / np.linalg.norm(p_to_l);
                                V = (cam_pos - p_world) / np.linalg.norm(cam_pos - p_world);
                                H = (L + V) / np.linalg.norm(L + V);
                                
                                I_d = (np.array(self.light.color) * self.light.intensity) / (np.linalg.norm(p_to_l) ** 2)
                                phi_d = (mesh.kd * mesh.diffuse_color * max(0, np.dot(L, N))) / np.pi;
                                diff = I_d * phi_d;
                                
                                spec = mesh.ks * (max(0, np.dot(H, N)) ** mesh.ke) * mesh.specular_color;
                                image_buffer[y][x] = (diff + A + spec) * 255;
                                
                            elif (shading == "gouraud"):                          
                                image_buffer[y][x] = (alpha * vert_intensities[0] + beta * vert_intensities[1] + gamma * vert_intensities[2]) * 255;
                            elif (shading == "texture"):
                                
                                uv_coords = alpha * mesh.uvs[t.a] + beta * mesh.uvs[t.b] + gamma * mesh.uvs[t.c];
                                uv_coords[1] *= -1;
                                image_buffer[y][x] = mesh.texture.custom_uv(0, uv_coords);
                                
                            elif (shading == "texture-correct"):
                                image_buffer[y][x] = mesh.texture.get_color(Z, P, alpha, beta, gamma);
                            elif (shading == "spheremap"):
                                
                                #Calculate the interpolated surface normal and eye vectors and normalize them.
                                p_normal = alpha * vertA_normal + beta * vertB_normal + gamma * vertC_normal;
                                N = p_normal / np.linalg.norm(p_normal);
                                p_world = self.camera.inverse_project_point(alpha * verts_device_coords[0] + beta * verts_device_coords[1] + gamma * verts_device_coords[2]);
                                p_to_c = (cam_pos - p_world);
                                E = p_to_c / np.linalg.norm(p_to_c);
                                
                                image_buffer[y][x] = mesh.texture.get_color(N, E); 
                               
                            elif (shading == "spheremap-spec-diff"):
                                
                                #Calculate the interpolated surface normal and eye vectors and normalize them.
                                p_normal = alpha * vertA_normal + beta * vertB_normal + gamma * vertC_normal;
                                N = p_normal / np.linalg.norm(p_normal);
                                p_world = self.camera.inverse_project_point(alpha * verts_device_coords[0] + beta * verts_device_coords[1] + gamma * verts_device_coords[2]);
                                p_to_c = (cam_pos - p_world);
                                p_to_l = (light_pos - p_world);
                                L = p_to_l / np.linalg.norm(p_to_l);
                                V = p_to_c / np.linalg.norm(p_to_c);
                                H = (L + V) / np.linalg.norm(L + V);
                                spec = mesh.ks * (max(0, np.dot(H, N)) ** mesh.ke) * mesh.specular_color;
                                
                                texture_color = mesh.texture.get_color(N, V) / 255;
                                
                                #diffuse_color = mesh.diffuse_color * texture_color;
                                diffuse_color = self.overlay_color(texture_color, mesh.diffuse_color);
                                
                                I_d = (np.array(self.light.color) * self.light.intensity) / (np.linalg.norm(p_to_l) ** 2)
                                phi_d = (mesh.kd * diffuse_color * max(0, np.dot(L, N))) / np.pi;
                                diff = I_d * phi_d;
                                
                                final_color = np.array([min(255, (diff[0] + A[0] + spec[0]) * 255), min(255, (diff[1] + A[1] + spec[1]) * 255), min(255, (diff[2] + A[2] + spec[2]) * 255)])
                                
                                image_buffer[y][x] = final_color; 
                            elif (shading == "spheremap-spec"):
                                
                                #Calculate the interpolated surface normal and eye vectors and normalize them.
                                p_normal = alpha * vertA_normal + beta * vertB_normal + gamma * vertC_normal;
                                N = p_normal / np.linalg.norm(p_normal);
                                p_world = self.camera.inverse_project_point(alpha * verts_device_coords[0] + beta * verts_device_coords[1] + gamma * verts_device_coords[2]);
                                p_to_c = (cam_pos - p_world);
                                p_to_l = (light_pos - p_world);
                                L = p_to_l / np.linalg.norm(p_to_l);
                                V = p_to_c / np.linalg.norm(p_to_c);
                                H = (L + V) / np.linalg.norm(L + V);
                                spec = mesh.ks * (max(0, np.dot(H, N)) ** mesh.ke) * mesh.specular_color;
                                
                                diff = mesh.texture.get_color(N, V) / 255;
                                
                                final_color = np.array([min(255, (diff[0] + A[0] + spec[0]) * 255), min(255, (diff[1] + A[1] + spec[1]) * 255), min(255, (diff[2] + A[2] + spec[2]) * 255)])
                                
                                image_buffer[y][x] = final_color;
                            elif (shading == "cubemap"):
                                #Calculate the interpolated surface normal and eye vectors and normalize them.
                                p_normal = alpha * vertA_normal + beta * vertB_normal + gamma * vertC_normal;
                                N = p_normal / np.linalg.norm(p_normal);
                                p_world = self.camera.inverse_project_point(alpha * verts_device_coords[0] + beta * verts_device_coords[1] + gamma * verts_device_coords[2]);
                                p_to_c = (cam_pos - p_world);
                                p_to_l = (light_pos - p_world);
                                L = p_to_l / np.linalg.norm(p_to_l);
                                V = p_to_c / np.linalg.norm(p_to_c);
                                H = (L + V) / np.linalg.norm(L + V);
                                spec = mesh.ks * (max(0, np.dot(H, N)) ** mesh.ke) * mesh.specular_color;
                                
                                
                                
                                if (mesh.texture.tex_mode == TEX_MODE_CUBEMAP_REFLECT):
                                    texture_color = mesh.texture.get_color(N, V) / 255;
                                else:
                                    #Calculate sphere_normal
                                    S = alpha * mesh.verts[t.a].as_array() + beta * mesh.verts[t.b].as_array() + gamma * mesh.verts[t.c].as_array();
                                    S = S / np.linalg.norm(S);
                                    texture_color = mesh.texture.get_color(S) / 255;
                                    
                                spec = self.overlay_color(texture_color, spec);
                                
                                diffuse_color = mesh.diffuse_color * texture_color;
                                #diffuse_color = self.overlay_color(texture_color, mesh.diffuse_color);
                                
                                I_d = (np.array(self.light.color) * self.light.intensity) / (np.linalg.norm(p_to_l) ** 2)
                                phi_d = (mesh.kd * diffuse_color * max(0, np.dot(L, N))) / np.pi;
                                diff = I_d * phi_d;
                                
                                final_color = np.array([min(255, (diff[0] + A[0] + spec[0]) * 255), min(255, (diff[1] + A[1] + spec[1]) * 255), min(255, (diff[2] + A[2] + spec[2]) * 255)])
                                         
                                image_buffer[y][x] = final_color;
                            else:
                                image_buffer[y][x] = np.array([1,1,1]) * depth * 255;

        self.screen.draw(image_buffer);
        
    #Blends to color values together. 
    def overlay_color(self, r_color: np.ndarray, obj_color: np.ndarray) -> np.ndarray:
        
        #Calculate the luminance of the given color
        Y = 0.2126 * r_color[0] + 0.7152 * r_color[1] + 0.0722 * r_color[2]; 
        
        ret = (Y * 0.5 * obj_color) / 2 + obj_color / 2;
        
        return np.array(ret);