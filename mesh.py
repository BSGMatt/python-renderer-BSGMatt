import numpy 
from stl import mesh
from pprint import pprint
from transform import Transform
from vector3 import *
from PIL import Image

class Mesh:

    def __init__(self, diffuse_color, specular_color, ka, kd, ks, ke):
        self.verts = [];
        self.faces = [];
        self.normals = [];
        self.uvs = [];
        self.texture = None;
        self.minBounds = None;
        self.maxBounds = None;
        self.transform = Transform();
        
        
        #Define material
        self.diffuse_color = diffuse_color;
        self.specular_color = specular_color;
        self.ka = ka;
        self.kd = kd;
        self.ks = ks;
        self.ke = ke;
        
    def find_normal(self, tri: Triangle):
        
        for i in range(len(self.faces)):
            if (self.faces[i] == tri):
                return self.normals[i];
            
        return None;

    def from_stl(stl_path: str, diffuse_color, specular_color, ka, kd, ks, ke):

        numpyMesh = mesh.Mesh.from_file(stl_path);
        points = numpyMesh.points;

        verts = [];
        faces = [];

        verts.append(Vertex(0, points[0][0], points[0][1], points[0][2]));
        verts.append(Vertex(1, points[0][3], points[0][4], points[0][5]));
        verts.append(Vertex(2, points[0][6], points[0][7], points[0][8]));
        faces.append(Triangle(0, 1, 2));

        for i in range(1, len(points)):
            tri = []; #temp list to store vertex indices that will make a triangle. 
            for j in range(0, len(points[i]), 3):
                unique = True;
                #Check through previous vertices to ensure that this is a new vertex. 
                for k in range(0, len(verts)):
                    if (verts[k].position.equals(points[i][j], points[i][j+1], points[i][j+2])):
                        tri.append(k); #save the index for later. 
                        unique = False;
                        break;
                if (unique):
                    id = len(verts);
                    verts.append(Vertex(id, points[i][j], points[i][j+1], points[i][j+2]));
                    tri.append(id);
            faces.append(Triangle(tri[0], tri[1], tri[2]));
        
        normals = [];
        for i in range(0, len(numpyMesh.normals)):
            normals.append(Vector3.from_list(numpyMesh.normals[i]).normalized());
            
        #Calculate the vertex normals
        for i in range(0, len(faces)):
            
            n = normals[i].as_numpy_array();
            
            verts[faces[i].a].normal += n;
            verts[faces[i].b].normal += n;
            verts[faces[i].c].normal += n;
            
        for v in verts:
            v.normal = v.normal / numpy.linalg.norm(v.normal);
            #print(v.normal);

        ret = Mesh(diffuse_color, specular_color, ka, kd, ks, ke);
        ret.verts = verts;
        ret.faces = faces;
        ret.normals = normals;
        ret.minBounds = Vector3.from_list(numpyMesh.min_);
        ret.maxBounds = Vector3.from_list(numpyMesh.max_);

        return ret;
    
    def load_texture(self, img_path, tex_mode = -1):
        
        tex = Image.open(img_path);
        self.texture = tex.convert('RGB');
        
        return;
    
    #z is 'up', theta is azimith angle, phi is elevation
    #used for texture coordinates of sphere, so it only returns theta and phi angle
    def cart2sph(self, v):
        
        v = v.as_array();
        
        x = v[0]
        y = v[1]
        z = v[2]

        theta = numpy.arctan2(y,x)
        phi   = numpy.arctan2(z,numpy.sqrt(x**2 + y**2))
        return numpy.array([theta, phi])

    def sphere_uvs(self):
        uvs = []
        verts = self.verts

        #loop over each vertex
        for v in verts:
            #convert cartesian to spherical
            uv = self.cart2sph(v)

            #convert theta and phi to u and v by normalizing angles
            uv[0] += numpy.pi
            uv[1] += numpy.pi/2.0

            uv[0] /= 2.0*numpy.pi
            uv[1] /= numpy.pi

            uvs.append(uv)

        self.uvs = uvs

        return uvs

    @staticmethod
    def textured_plane():
        mesh = Mesh([],[],0,0,0,0) 
        # mesh.verts = [np.array([0.4, 0.5, -0.5]),
        #     np.array([-0.4, 0.5, -0.4]),
        #     np.array([0.4, -0.5, 0.4]),
        #     np.array([-0.4, -0.9, 0.4])
        #     ]

        mesh.verts = [Vertex(0, 0.4, 0.5, -0.5),
            Vertex(1, -0.4, 0.5, -0.5),
            Vertex(2, 0.5, -0.5, 0.4),
            Vertex(3, -0.4, -0.55, 0.4)
            ]

        mesh.faces = [Triangle(0, 1, 2),Triangle(3, 2, 1)]

        #todo: once happy, print the normals and set manually to avoid dependency on vector3 class
        normals = []
        for t in mesh.faces:
            
            #Grab the vertices position. 
            
            a = mesh.verts[t.a].as_array();
            b = mesh.verts[t.b].as_array();
            c = mesh.verts[t.c].as_array();
            n = numpy.cross(b - a, c - a)

            normals.append(Vector3.from_list(n / numpy.linalg.norm(n)));
        
        #Calculate the vertex normals
        for i in range(0, len(mesh.faces)):
            
            n = normals[i].as_numpy_array();
            
            mesh.verts[mesh.faces[i].a].normal += n;
            mesh.verts[mesh.faces[i].b].normal += n;
            mesh.verts[mesh.faces[i].c].normal += n;
            
        for v in mesh.verts:
            v.normal = v.normal / numpy.linalg.norm(v.normal);
            
        mesh.normals = normals 

        mesh.uvs = [numpy.array([0.0,0.0]),numpy.array([1.0,0.0]),numpy.array([0.0,1.0]),numpy.array([1.0,1.0])]

        return mesh

    from_stl = staticmethod(from_stl);