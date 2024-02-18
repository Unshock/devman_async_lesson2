from random import randint, choice

import asyncio

from tools.curses_tools import draw_frame, get_frame_size
from tools.common_tools import sleep, get_frames_list
from settings.game_state import GARBAGE_COROUTINES, OBSTACLES, \
    OBSTACLES_IN_LAST_COLLISION
from settings import game_state, settings
from obstacles import Obstacle
from explosion import explode
from game_scenario import get_garbage_delay_tics


async def fly_garbage(canvas, column, garbage_frame, obstacle, speed=0.5):
    """
    Animate garbage, flying from top to bottom.
    Column position will stay same, as specified on start.
    """
    rows_number, columns_number = canvas.getmaxyx()
    garbage_height, _ = get_frame_size(garbage_frame)

    row = -garbage_height

    while row < rows_number - settings.BORDER_WIDTH:

        if obstacle in OBSTACLES_IN_LAST_COLLISION:
            OBSTACLES_IN_LAST_COLLISION.remove(obstacle)
            OBSTACLES.remove(obstacle)

            explosion_row = row + obstacle.rows_size // 2
            explosion_column = column + obstacle.columns_size // 2
            await explode(canvas, explosion_row, explosion_column)

            return

        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        obstacle.row = row


async def fill_orbit_with_garbage(window):

    garbage_frames = get_frames_list(
        'frames/trash_small.txt',
        'frames/trash_large.txt',
        'frames/trash_xl.txt',
        'frames/duck.txt',
        'frames/hubble.txt',
        'frames/lamp.txt'
    )

    canvas = window.canvas
    obstacle_id = 0

    while True:
        garbage_delay = get_garbage_delay_tics(game_state.YEAR)

        if not garbage_delay:
            await sleep(1)

        else:
            speed = settings.GARBAGE_SPEED
            frame = choice(garbage_frames)

            frame_height, frame_width = get_frame_size(frame)
            entrance_column = randint(1, window.columns - frame_width)

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
                speed=speed,
                obstacle=obstacle
            )

            OBSTACLES.add(obstacle)
            GARBAGE_COROUTINES.append(garbage_coroutine)

            await sleep(garbage_delay)
