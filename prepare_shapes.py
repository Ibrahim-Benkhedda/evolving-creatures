import random
import math
from noise import pnoise2

# def write_to_obj(filename, vertices, indices):
#     with open(filename, 'w') as f:
#         # Write vertices to the file
#         for vertex in vertices:
#             f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

#         # Write faces to the file
#         for face in indices:
#             # OBJ indices start from 1, not 0
#             f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

def write_to_obj(filename, vertices, indices):
    with open(filename, 'w') as f:
        # Write vertices to the file
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

        # Write faces to the file
        for face in indices:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

def make_pyramid(filename):
    # Define the tetrahedron vertices and indices
    vertices = [
        [-5, -5, 0],  # Base vertex 1
        [5, -5, 0],   # Base vertex 2
        [0, 5, 0],    # Base vertex 3
        [0, 0, 5]     # Apex vertex
    ]
    indices = [
        [0, 1, 2],  # Base triangle
        [0, 1, 3],  # Side triangle 1
        [1, 2, 3],  # Side triangle 2
        [2, 0, 3]   # Side triangle 3
    ]
    # Write the tetrahedron to an OBJ file
    write_to_obj(filename, vertices, indices)


def make_rocky_moutain(filename):

    # Define the pyramid vertices and indices
    vertices = [
        [-5, -5, 0],  # Base vertex 1
        [5, -5, 0],   # Base vertex 2
        [5, 5, 0],    # Base vertex 3
        [-5, 5, 0],   # Base vertex 4
        [0, 0, 5]     # Apex vertex
    ]
    indices = [
        [0, 1, 4],  # Side triangle 1
        [1, 2, 4],  # Side triangle 2
        [2, 3, 4],  # Side triangle 3
        [3, 0, 4],  # Side triangle 4
        [0, 1, 2],  # Base triangle 1
        [2, 3, 0]   # Base triangle 2
    ]

    # Add random cubes embedded in the pyramid
    num_cubes = 5
    for _ in range(num_cubes):
        size = random.uniform(0.5, 2)
        x = random.uniform(-4, 4)
        y = random.uniform(-4, 4)
        z = random.uniform(0.5, 4.5)
        
        # Define cube vertices
        cube_vertices = [
            [x-size/2, y-size/2, z-size/2],
            [x+size/2, y-size/2, z-size/2],
            [x+size/2, y+size/2, z-size/2],
            [x-size/2, y+size/2, z-size/2],
            [x-size/2, y-size/2, z+size/2],
            [x+size/2, y-size/2, z+size/2],
            [x+size/2, y+size/2, z+size/2],
            [x-size/2, y+size/2, z+size/2]
        ]
        
        # Define cube faces
        cube_indices = [
            [0, 1, 2], [2, 3, 0],  # Bottom
            [4, 5, 6], [6, 7, 4],  # Top
            [0, 1, 5], [5, 4, 0],  # Front
            [1, 2, 6], [6, 5, 1],  # Right
            [2, 3, 7], [7, 6, 2],  # Back
            [3, 0, 4], [4, 7, 3]   # Left
        ]
        
        # Offset cube indices by the current number of vertices
        offset = len(vertices)
        cube_indices = [[i+offset for i in face] for face in cube_indices]
        
        # Add cube vertices and indices to the main lists
        vertices.extend(cube_vertices)
        indices.extend(cube_indices)

    # Write the combined vertices and indices to an OBJ file
    write_to_obj(filename, vertices, indices)



def gaussian(x, y, sigma):
    """Return the height of the shape at position (x, y) using a Gaussian function."""
    return math.exp(-((x**2 + y**2) / (2 * sigma**2)))

def generate_gaussian_pyramid(filename, size=10, resolution=0.5, sigma=3):
    vertices = []
    faces = []

    # Generate vertices using the Gaussian function
    for i in range(int(size / resolution)):
        for j in range(int(size / resolution)):
            x = -size/2 + i * resolution
            y = -size/2 + j * resolution
            z = gaussian(x, y, sigma)
            vertices.append([x, y, z])

    # Generate faces by connecting vertices
    for i in range(int(size / resolution) - 1):
        for j in range(int(size / resolution) - 1):
            # Calculate indices for the current square
            bottom_left = i * int(size / resolution) + j
            bottom_right = i * int(size / resolution) + j + 1
            top_left = (i + 1) * int(size / resolution) + j
            top_right = (i + 1) * int(size / resolution) + j + 1

            # Create two triangles for the current square
            faces.append([bottom_left, bottom_right, top_left])
            faces.append([top_left, bottom_right, top_right])

    # Write to OBJ file
    with open(filename, 'w') as f:
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")


import math

def gaussian2(x, y, sigma, height):
    """Return the height of the shape at position (x, y) using a Gaussian function."""
    return height * math.exp(-((x**2 + y**2) / (2 * sigma**2)))

def generate_gaussian_pyramid2(filename, size=10, resolution=0.5, sigma=3, height=5):
    vertices = []
    faces = []

    # Generate vertices using the Gaussian function for the pyramid
    for i in range(int(size / resolution)):
        for j in range(int(size / resolution)):
            x = -size/2 + i * resolution
            y = -size/2 + j * resolution
            z = gaussian2(x, y, sigma, height)
            vertices.append([x, y, z])

    # Generate vertices for the flat base
    for i in range(int(size / resolution)):
        for j in range(int(size / resolution)):
            x = -size/2 + i * resolution
            y = -size/2 + j * resolution
            z = 0
            vertices.append([x, y, z])

    # Generate faces by connecting vertices
    for i in range(int(size / resolution) - 1):
        for j in range(int(size / resolution) - 1):
            # Calculate indices for the current square on the pyramid
            bottom_left = i * int(size / resolution) + j
            bottom_right = i * int(size / resolution) + j + 1
            top_left = (i + 1) * int(size / resolution) + j
            top_right = (i + 1) * int(size / resolution) + j + 1

            # Create two triangles for the current square on the pyramid
            faces.append([bottom_left, bottom_right, top_left])
            faces.append([top_left, bottom_right, top_right])

            # Calculate indices for the current square on the base
            base_offset = int(size / resolution) * int(size / resolution)
            bottom_left_base = base_offset + bottom_left
            bottom_right_base = base_offset + bottom_right
            top_left_base = base_offset + top_left
            top_right_base = base_offset + top_right

            # Create two triangles for the current square on the base
            faces.append([bottom_left_base, top_left_base, bottom_right_base])
            faces.append([top_left_base, top_right_base, bottom_right_base])

    # Write to OBJ file
    with open(filename, 'w') as f:
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")


def generate_gaussian_pyramid3(filename, size=10, resolution=0.5, sigma=3, height=5, noise_scale=0.5, noise_factor=1.0):
    """
    pyramid with noise
    """
    vertices = []
    faces = []

    # Generate vertices using the Gaussian function for the pyramid
    for i in range(int(size / resolution)):
        for j in range(int(size / resolution)):
            x = -size/2 + i * resolution
            y = -size/2 + j * resolution
            z = gaussian2(x, y, sigma, height)

            # Add Perlin noise to the z-coordinate
            z += pnoise2(x * noise_scale, y * noise_scale) * noise_factor

            vertices.append([x, y, z])

 # Generate vertices for the flat base
    for i in range(int(size / resolution)):
        for j in range(int(size / resolution)):
            x = -size/2 + i * resolution
            y = -size/2 + j * resolution
            z = 0
            vertices.append([x, y, z])

    # Generate faces by connecting vertices
    for i in range(int(size / resolution) - 1):
        for j in range(int(size / resolution) - 1):
            # Calculate indices for the current square on the pyramid
            bottom_left = i * int(size / resolution) + j
            bottom_right = i * int(size / resolution) + j + 1
            top_left = (i + 1) * int(size / resolution) + j
            top_right = (i + 1) * int(size / resolution) + j + 1

            # Create two triangles for the current square on the pyramid
            faces.append([bottom_left, bottom_right, top_left])
            faces.append([top_left, bottom_right, top_right])

            # Calculate indices for the current square on the base
            base_offset = int(size / resolution) * int(size / resolution)
            bottom_left_base = base_offset + bottom_left
            bottom_right_base = base_offset + bottom_right
            top_left_base = base_offset + top_left
            top_right_base = base_offset + top_right

            # Create two triangles for the current square on the base
            faces.append([bottom_left_base, top_left_base, bottom_right_base])
            faces.append([top_left_base, top_right_base, bottom_right_base])

    # Write to OBJ file
    with open(filename, 'w') as f:
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")




def generate_gaussian_pyramid4(filename, size=10, resolution=0.5, sigma=3, height=5, noise_scale=0.5, noise_factor=1.0):
    vertices = []
    faces = []

    # Generate vertices using the Gaussian function for the top surface of the pyramid
    for i in range(int(size / resolution)):
        for j in range(int(size / resolution)):
            x = -size/2 + i * resolution
            y = -size/2 + j * resolution
            z = gaussian2(x, y, sigma, height)

            # Add Perlin noise to the z-coordinate
            z += pnoise2(x * noise_scale, y * noise_scale) * noise_factor

            vertices.append([x, y, z])

    # Generate vertices for the bottom surface (flat base) of the pyramid
    for i in range(int(size / resolution)):
        for j in range(int(size / resolution)):
            x = -size/2 + i * resolution
            y = -size/2 + j * resolution
            z = 0
            vertices.append([x, y, z])

    # Generate faces for the top surface
    for i in range(int(size / resolution) - 1):
        for j in range(int(size / resolution) - 1):
            bottom_left = i * int(size / resolution) + j
            bottom_right = i * int(size / resolution) + j + 1
            top_left = (i + 1) * int(size / resolution) + j
            top_right = (i + 1) * int(size / resolution) + j + 1

            faces.append([bottom_left, bottom_right, top_left])
            faces.append([top_left, bottom_right, top_right])

    # Generate faces for the bottom surface
    base_offset = int(size / resolution) * int(size / resolution)
    for i in range(int(size / resolution) - 1):
        for j in range(int(size / resolution) - 1):
            bottom_left_base = base_offset + i * int(size / resolution) + j
            bottom_right_base = base_offset + i * int(size / resolution) + j + 1
            top_left_base = base_offset + (i + 1) * int(size / resolution) + j
            top_right_base = base_offset + (i + 1) * int(size / resolution) + j + 1

            faces.append([bottom_left_base, top_left_base, bottom_right_base])
            faces.append([top_left_base, top_right_base, bottom_right_base])

    # Generate faces for the sides
    for i in range(int(size / resolution) - 1):
        for j in range(int(size / resolution)):
            top = i * int(size / resolution) + j
            bottom = base_offset + i * int(size / resolution) + j
            top_next = (i + 1) * int(size / resolution) + j
            bottom_next = base_offset + (i + 1) * int(size / resolution) + j

            faces.append([top, bottom, top_next])
            faces.append([top_next, bottom, bottom_next])

    # Write to OBJ file
    with open(filename, 'w') as f:
        for vertex in vertices:
            f.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

# Generate the OBJ file
generate_gaussian_pyramid4("./shapes/gaussian_pyramid.obj")


# Generate the OBJ file
# generate_gaussian_pyramid3("./shapes/gaussian_pyramid.obj")


# Generate the OBJ file
# generate_gaussian_pyramid("./shapes/gaussian_pyramid.obj")


# make_pyramid('./shapes/pyramid.obj')
# make_rocky_moutain('./shapes/mountain_with_cubes.obj')

# make_pyramid('mountain.obj')
# make_rocky_moutain('./shapes/mountain_with_cubes.obj')
