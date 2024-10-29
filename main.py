import pygame
import pymunk
import random
import asyncio


def clear_all(space, circles, balls):
    # Remove circles and corresponding bodies from space
    for circle, _ in circles:
        space.remove(circle.body, circle)
    # Remove static balls and corresponding bodies from space
    for ball in balls:
        space.remove(ball.body, ball)

    # Clear the lists
    circles.clear()
    balls.clear()


def create_circle(space, pos, color):
    body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
    body.position = pos
    shape = pymunk.Circle(body, 10)
    shape.elasticity = 1
    shape.friction = 1000
    space.add(body, shape)
    return shape, color


def draw_circles(screen, circles):
    for circle, color in circles:
        x = int(circle.body.position.x)
        y = int(circle.body.position.y)
        pygame.draw.circle(screen, color, (x, y), 10)


def create_static_ball(space, pos):
    body = pymunk.Body(1, 100, body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, 50)
    shape.elasticity = 0.2
    shape.friction = 2
    space.add(body, shape)
    return shape


def draw_static_balls(screen, balls):
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


async def main():
    pygame.init()
    info = pygame.display.Info()
    WIDTH, HEIGHT = 1080, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    space = pymunk.Space()
    space.gravity = (0, 1000)

    font = pygame.font.Font(None, 30)

    fps = 60
    balls_per_tick = 1
    circles = []
    balls = []
    create_boundaries(space, WIDTH, HEIGHT)

    counter = 0
    bpt_up_counter = 0
    bpt_low_counter = 0

    running = True
    drawing = False
    bpt_up = False
    bpt_low = False
    hold = False
    bpt_up_hold = False
    bpt_low_hold = False
    change_bpt_up = 0
    change_bpt_low = 0
    render_brush_size = False

    while running:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                elif event.button == 3:
                    balls.append(create_static_ball(space, pygame.mouse.get_pos()))
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    hold = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    clear_all(space, circles, balls)

                if event.key == pygame.K_UP:
                    bpt_up = True
                    render_brush_size = True

                if event.key == pygame.K_DOWN:
                    bpt_low = True
                    render_brush_size = True

                # if event.key == pygame.K_q:
                #     running = False
                #     break

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    bpt_up = False
                    bpt_up_hold = False
                    change_bpt_up = 0
                    render_brush_size = False

                if event.key == pygame.K_DOWN:
                    bpt_low = False
                    bpt_low_hold = False
                    change_bpt_low = 0
                    render_brush_size = False

        if drawing:
            if counter == 24 and not hold:
                color = (random.choice(range(256)),
                         random.choice(range(256)),
                         random.choice(range(256)))
                circles.append(create_circle(space, pygame.mouse.get_pos(), color))
                counter = 0
                hold = True
            elif counter == 24 and hold:
                for _ in range(balls_per_tick):
                    color = (random.choice(range(256)),
                             random.choice(range(256)),
                             random.choice(range(256)))
                    x, y = pygame.mouse.get_pos()
                    x += random.randrange(0, 10) - random.randrange(0, 10)
                    y += random.randrange(0, 10) - random.randrange(0, 10)
                    circles.append(create_circle(space, (x, y), color))
            else:
                counter += 1
        else:
            counter = 24

        if balls_per_tick + 1 <= 10:
            if bpt_up:
                if bpt_up_counter == 24 and not bpt_up_hold:
                    bpt_up_counter = 0
                    balls_per_tick += 1
                    bpt_up_hold = True
                elif bpt_up_counter == 24 and bpt_up_hold:
                    change_bpt_up += 1
                    if change_bpt_up == 20:
                        balls_per_tick += 1
                        change_bpt_up = 0
                else:
                    bpt_up_counter += 1
            else:
                bpt_up_counter = 24

        if balls_per_tick - 1 >= 1:
            if bpt_low:
                if bpt_low_counter == 24 and not bpt_low_hold:
                    bpt_low_counter = 0
                    balls_per_tick -= 1
                    bpt_low_hold = True
                elif bpt_low_counter == 24 and bpt_low_hold:
                    change_bpt_low += 1
                    if change_bpt_low == 20:
                        balls_per_tick -= 1
                        change_bpt_low = 0
                else:
                    bpt_low_counter += 1
            else:
                bpt_low_counter = 24

        screen.fill((223, 184, 243))

        # text_surface = font.render(
        #     f'LMB hold to draw. RMB to place static ball. '
        #     f'[R] to clear. Brush size: {balls_per_tick} (use arrows to change).',
        #     True, 'white')
        # text_width, text_height = text_surface.get_size()
        #
        # brush_size_text = font.render(f'{balls_per_tick}', True, 'white')
        # screen.blit(text_surface, ((WIDTH - text_width) // 2, 20))

        draw_circles(screen, circles)
        draw_static_balls(screen, balls)
        space.step(1 / fps / 2)

        # if render_brush_size:
        #     x, y = pygame.mouse.get_pos()
        #     screen.blit(brush_size_text, (x - 20, y - 20))
        #
        pygame.display.flip()
        await asyncio.sleep(0)


if __name__ == '__main__':
    asyncio.run(main())
