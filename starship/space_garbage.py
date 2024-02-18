import os
from random import randint, choice

from curses_tools import draw_frame, get_frame_size
import asyncio

from common_tools import read_from_file, sleep, get_frames_list
from settings import GARBAGE_COROUTINES, OBSTACLES, OBSTACLES_IN_LAST_COLLISION
from obstacles import Obstacle


async def fly_garbage(canvas, column, garbage_frame, obstacle, speed=0.5):
    """
    Animate garbage, flying from top to bottom.
    Column position will stay same, as specified on start.
    """
    rows_number, columns_number = canvas.getmaxyx()

    row = 0

    while row < rows_number:

        if obstacle in OBSTACLES_IN_LAST_COLLISION:
            OBSTACLES_IN_LAST_COLLISION.remove(obstacle)
            OBSTACLES.remove(obstacle)
            return

        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        obstacle.row = row

    OBSTACLES.remove(obstacle)


async def fill_orbit_with_garbage(canvas, garbage_count=3):

    garbage_frames = get_frames_list(
        'frames/trash_small.txt',
        'frames/trash_large.txt',
        'frames/trash_xl.txt',
        'frames/duck.txt',
        'frames/hubble.txt',
        'frames/lamp.txt'
    )

    obstacle_id = 0

    while True:

        # if len(GARBAGE_COROUTINES) < garbage_count:

        _, max_x = canvas.getmaxyx()

        random_speed = randint(30, 70) / 100
        frame = choice(garbage_frames)

        frame_height, frame_width = get_frame_size(frame)
        entrance_column = randint(1, max_x - frame_width)

        obstacle_id += 1
        obstacle = Obstacle(
            row=0,
            column=entrance_column,
            rows_size=frame_height,
            columns_size=frame_width,
            uid=obstacle_id
        )

        garbage_coroutine = fly_garbage(
            canvas,
            column=entrance_column,
            garbage_frame=frame,
            speed=random_speed,
            obstacle=obstacle
        )

        OBSTACLES.append(obstacle)
        GARBAGE_COROUTINES.append(garbage_coroutine)

        await sleep(tics=15)
