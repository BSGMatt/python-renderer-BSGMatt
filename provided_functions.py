#z is 'up', theta is azimith angle, phi is elevation
#used for texture coordinates of sphere, so it only returns theta and phi angle
def cart2sph(v):
    x = v[0]
    y = v[1]
    z = v[2]

    theta = np.arctan2(y,x)
    phi   = np.arctan2(z,np.sqrt(x**2 + y**2))
    return np.array([theta, phi])


def sphere_uvs(self):
    uvs = []
    verts = self.verts

    #loop over each vertex
    for v in verts:
        #convert cartesian to spherical
        uv = cart2sph(v)

        #convert theta and phi to u and v by normalizing angles
        uv[0] += np.pi
        uv[1] += np.pi/2.0

        uv[0] /= 2.0*np.pi
        uv[1] /= np.pi

        uvs.append(uv)

    self.uvs = uvs

    return uvs

@staticmethod
def textured_plane():
    mesh = Mesh() 
    # mesh.verts = [np.array([0.4, 0.5, -0.5]),
    #     np.array([-0.4, 0.5, -0.4]),
    #     np.array([0.4, -0.5, 0.4]),
    #     np.array([-0.4, -0.9, 0.4])
    #     ]

    mesh.verts = [np.array([0.4, 0.5, -0.5]),
        np.array([-0.4, 0.5, -0.5]),
        np.array([0.5, -0.5, 0.4]),
        np.array([-0.4, -0.55, 0.4])
        ]

    mesh.faces = [[0, 1, 2],[3, 2, 1]]

    #todo: once happy, print the normals and set manually to avoid dependency on vector3 class
    normals = []
    for face in mesh.faces:
        a = Vector3.from_array(mesh.verts[face[0]])
        b = Vector3.from_array(mesh.verts[face[1]])
        c = Vector3.from_array(mesh.verts[face[2]])
        n = Vector3.cross(b - a, c - a)

        normals.append(n.normalized())

    mesh.normals = normals 

    mesh.uvs = [np.array([0.0,0.0]),np.array([1.0,0.0]),np.array([0.0,1.0]),np.array([1.0,1.0])]

    return mesh