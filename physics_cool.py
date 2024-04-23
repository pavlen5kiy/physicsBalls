import pygame
import pymunk
import random


def create_circle(space, pos, color):
    body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, 10)
    shape.elasticity = 1
    shape.friction = 1000
    space.add(body, shape)
    return shape, color


def draw_circles(circles):
    for circle, color in circles:
        x = int(circle.body.position.x)
        y = int(circle.body.position.y)
        pygame.draw.circle(screen, color, (x, y), 10)


def create_static_ball(space):
    body = pymunk.Body(1, 100, body_type=pymunk.Body.STATIC)
    body.position = (450, 400)
    shape = pymunk.Circle(body, 50)
    shape.elasticity = 0.2
    shape.friction = 2
    space.add(body, shape)
    return shape


def draw_static_balls(balls):
    for ball in balls:
        x = int(ball.body.position.x)
        y = int(ball.body.position.y)
        pygame.draw.circle(screen, 'black', (x, y), 50)


def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height), (width, 0)],
        [(width / 2, 0), (width, 0)],
        [(0, height / 2), (0, height)],
        [(width, height / 2), (0, height)]
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 1
        shape.friction = 1000
        space.add(body, shape)


pygame.init()
screen = pygame.display.set_mode((1080, 720))
clock = pygame.time.Clock()
space = pymunk.Space()
space.gravity = (0, 1000)

font = pygame.font.Font(None, 100)

fps = 120
circles = []
balls = [create_static_ball(space)]
create_boundaries(space, 1080, 720)

counter = 0

running = True
drawing = False
hold = False

while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            hold = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Remove all non-static circles
                circles_to_remove = []
                for i, (circle, _) in enumerate(circles):
                    if circle.body.body_type == pymunk.Body.DYNAMIC:
                        circles_to_remove.append(i)

                # Remove circles after iterating over all circles
                for index in reversed(circles_to_remove):
                    circle, _ = circles.pop(index)
                    space.remove(circle.body, circle)

    if drawing:
        if counter == 24 and not hold:
            color = (random.choice(range(256)),
                     random.choice(range(256)),
                     random.choice(range(256)))
            circles.append(create_circle(space, pygame.mouse.get_pos(), color))
            counter = 0
            hold = True
        elif counter == 24 and hold:
            color = (random.choice(range(256)),
                     random.choice(range(256)),
                     random.choice(range(256)))
            circles.append(create_circle(space, pygame.mouse.get_pos(), color))
        else:
            counter += 1
    else:
        counter = 24

    screen.fill('white')

    text_surface = font.render('Hold to draw. Press [R] to clear.',
                               True, 'black')
    text_width, text_height = text_surface.get_size()
    screen.blit(text_surface, ((1080 - text_width) // 2, 100))

    draw_circles(circles)
    draw_static_balls(balls)
    space.step(1 / fps / 2)
    pygame.display.flip()
