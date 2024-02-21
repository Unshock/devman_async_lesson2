from random import randint, choice

import asyncio

from starship.tools.curses_tools import draw_frame, get_frame_size
from starship.tools.common_tools import sleep, get_frames_list
from starship.settings.game_state import OBSTACLES, \
    OBSTACLES_IN_LAST_COLLISION
from starship.settings import game_state, settings
from starship.obstacles import Obstacle
from starship.explosion import explode
from starship.game_scenario import get_garbage_delay_tics


async def fly_garbage(canvas, column, garbage_frame, garbage_id=0, speed=0.5):
    """
    Animate garbage, flying from top to bottom.
    Column position will stay same, as specified on start.
    """
    rows_number, columns_number = canvas.getmaxyx()
    garbage_height, garbage_width = get_frame_size(garbage_frame)

    row = -garbage_height

    obstacle = Obstacle(row, column, garbage_height, garbage_width, garbage_id)
    OBSTACLES.add(obstacle)

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

    OBSTACLES.remove(obstacle)


async def fill_orbit_with_garbage(window):
    """Coroutine that fills canvas with garbage according game scenario rate"""

    garbage_frames = get_frames_list(*settings.GARBAGE_FRAMES)
    canvas = window.canvas

    while True:
        garbage_delay = get_garbage_delay_tics(game_state.YEAR)

        if not garbage_delay:
            await sleep(settings.YEAR_TICS)

        else:
            speed = settings.GARBAGE_SPEED
            frame = choice(garbage_frames)

            _, frame_width = get_frame_size(frame)
            entrance_column = randint(1, window.columns - frame_width)

            garbage_coroutine = fly_garbage(
                canvas,
                column=entrance_column,
                garbage_frame=frame,
                speed=speed
            )

            game_state.coroutines.insert(0, garbage_coroutine)
            await sleep(garbage_delay)
