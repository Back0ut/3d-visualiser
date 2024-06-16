import pygame
import numpy as np
from math import sin, cos

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 400
pygame.display.set_caption('3D Projection')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

scale = 100
circle_pos = [WIDTH / 2, HEIGHT / 2]

points = [
    np.matrix([-1, -1, 1]),
    np.matrix([1, -1, 1]),
    np.matrix([1, 1, 1]),
    np.matrix([-1, 1, 1]),
    np.matrix([-1, -1, -1]),
    np.matrix([1, -1, -1]),
    np.matrix([1, 1, -1]),
    np.matrix([-1, 1, -1])
]

projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
])

projected_points = [
    [n, n] for n in range(len(points))
]

def connect_points(i, j, points):
    pygame.draw.line(screen, BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))

def main():
    angle_x, angle_y, angle_z = 0, 0, 0
    
    clock = pygame.time.Clock()
    running = True
    
    while running:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                elif event.key == pygame.K_x:
                    angle_x += 0.1
                
                elif event.key == pygame.K_y:
                    angle_y += 0.1
                
                elif event.key == pygame.K_z:
                    angle_z += 0.1
        
        rotation_z = np.matrix([
            [cos(angle_z), -sin(angle_z), 0],
            [sin(angle_z), cos(angle_z), 0],
            [0, 0, 1]
        ])

        rotation_y = np.matrix([
            [cos(angle_y), 0, sin(angle_y)],
            [0, 1, 0],
            [-sin(angle_y), 0, cos(angle_y)]
        ])

        rotation_x = np.matrix([
            [1, 0, 0],
            [0, cos(angle_x), -sin(angle_x)],
            [0, sin(angle_x), cos(angle_x)]
        ])
        
        screen.fill(WHITE)

        for i, point in enumerate(points):
            rotated2d = point.reshape(3, 1)
            
            rotated2d = np.dot(rotation_z, rotated2d)
            rotated2d = np.dot(rotation_y, rotated2d)
            rotated2d = np.dot(rotation_x, rotated2d)

            projected2d = np.dot(projection_matrix, rotated2d)
            
            x, y = int(projected2d[0][0] * scale) + circle_pos[0], int(projected2d[1][0] * scale) + circle_pos[1]        
            
            projected_points[i] = [x, y]
            pygame.draw.circle(screen, RED, (x, y), 5)

        for p in range(4):
            connect_points(p, (p + 1) % 4, projected_points)
            connect_points(p + 4, ((p + 1) % 4) + 4, projected_points)
            connect_points(p, p + 4, projected_points)

        pygame.display.update()

    pygame.quit()
    exit()

if __name__ == '__main__':
    main()