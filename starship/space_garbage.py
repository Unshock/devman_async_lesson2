import os
from random import randint, choice

from curses_tools import draw_frame, get_frame_size
import asyncio

from common_tools import read_from_file, sleep
from settings import GARBAGE_COROUTINES


async def fly_garbage(canvas, column, garbage_frame, speed=0.5):
    """
    Animate garbage, flying from top to bottom.
    Column position will stay same, as specified on start.
    """
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas, garbage_count=3):

    garbage_frames = [
        'frames/trash_small.txt',
        'frames/trash_large.txt',
        'frames/trash_xl.txt',
        'frames/duck.txt',
        'frames/hubble.txt',
        'frames/lamp.txt'
    ]

    while True:

        # if len(GARBAGE_COROUTINES) < garbage_count:

        _, max_x = canvas.getmaxyx()

        random_speed = randint(30, 70) / 100
        frame = read_from_file(
            os.path.join(os.path.dirname(__file__), choice(garbage_frames))
        )

        _, frame_width = get_frame_size(frame)
        entrance_column = randint(1, max_x - frame_width)

        garbage_coroutine = fly_garbage(
            canvas,
            column=entrance_column,
            garbage_frame=frame,
            speed=random_speed
        )

        GARBAGE_COROUTINES.append(garbage_coroutine)

        await sleep(tics=15)
