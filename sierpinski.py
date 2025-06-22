import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import math

# --- Constants ---
WIDTH, HEIGHT = 800, 600
NUM_POINTS = 30000
BLUE = (0.2, 0.6, 1.0) 

def get_initial_vertices():
    """Defines the 4 vertices of a tetrahedron."""
    return [
        (1.0, 1.0, 1.0),
        (-1.0, -1.0, 1.0),
        (-1.0, 1.0, -1.0),
        (1.0, -1.0, -1.0)
    ]

def generate_sierpinski_points(vertices, num_points):
    """Generates a list of 3D points for the Sierpinski tetrahedron."""
    points = []
    px, py, pz = (0.0, 0.0, 0.0)

    for _ in range(num_points):
        vx, vy, vz = random.choice(vertices)
        px = (px + vx) / 2
        py = (py + vy) / 2
        pz = (pz + vz) / 2
        points.append((px, py, pz))
    return points

def init_gl():
    """Initializes the OpenGL context."""
    glClearColor(1.0, 1.0, 1.0, 1.0) # White background
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (WIDTH / HEIGHT), 0.1, 50.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -5) # Move camera back
    glEnable(GL_DEPTH_TEST)
    glPointSize(1.5)

def main():
    """Main function to run the interactive 3D visualization."""
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("3D Sierpinski Tetrahedron")
    init_gl()

    points = generate_sierpinski_points(get_initial_vertices(), NUM_POINTS)
    
    # --- Transformation state ---
    rotation_x, rotation_y = 0, 0
    zoom = -5.0
    last_mouse_pos = None
    panning = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEWHEEL:
                zoom += event.y * 0.5
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    panning = True
                    last_mouse_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    panning = False
            elif event.type == pygame.MOUSEMOTION:
                if panning:
                    dx = event.pos[0] - last_mouse_pos[0]
                    dy = event.pos[1] - last_mouse_pos[1]
                    rotation_y += dx * 0.2
                    rotation_x += dy * 0.2
                    last_mouse_pos = event.pos

        # --- Drawing ---
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glPushMatrix()
        
        # Apply transformations
        glTranslatef(0.0, 0.0, zoom)
        glRotatef(rotation_x, 1, 0, 0)
        glRotatef(rotation_y, 0, 1, 0)
        
        # Draw points
        glBegin(GL_POINTS)
        glColor3f(*BLUE)
        for point in points:
            glVertex3fv(point)
        glEnd()
        
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)

    pygame.quit()

if __name__ == "__main__":
    main() 