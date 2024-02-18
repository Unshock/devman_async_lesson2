import os
import curses
import itertools
import asyncio
import random

from common_tools import read_from_file, sleep, get_frames_list
from curses_tools import read_controls, get_frame_size, draw_frame
from settings import FIRE_SHOTS_COROUTINES, ROCKET_COROUTINES, OBSTACLES, \
    OBSTACLES_IN_LAST_COLLISION


async def fire(canvas, start_row, start_column, rows_speed=-0.3,
               columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 1 < row < max_row and 0 < column < max_column:

        for obstacle in OBSTACLES:
            if obstacle.has_collision(row, column):
                OBSTACLES_IN_LAST_COLLISION.append(obstacle)
                return


        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas, row, column, symbol='*', delay=0):
    """Display animation of blinking star"""

    canvas.addstr(row, column, symbol, curses.A_DIM)
    await sleep(delay)

    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(20)

        canvas.addstr(row, column, symbol)
        await sleep(3)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(5)

        canvas.addstr(row, column, symbol)
        await sleep(3)


async def create_fire_shot(canvas, spaceship):

    fire_shot_column = spaceship.column + spaceship.width // 2
    fire_shot_row = spaceship.row - 1  # above the starship

    fire_shot_coroutine = fire(
        canvas,
        start_row=fire_shot_row + spaceship.row_speed,
        start_column=fire_shot_column + spaceship.column_speed,
        rows_speed=-0.9
    )

    FIRE_SHOTS_COROUTINES.append(fire_shot_coroutine)


async def run_spaceship(window, spaceship, border_width=1, tics=2):

    canvas = window.canvas
    #tics1 = 0

    for frame in itertools.cycle(spaceship.frames):

        # canvas.addstr(16, 5, 'WOW2c' + str(tics1), curses.A_DIM)
        # canvas.addstr(17, 5, 'WOW3c' + str(len(ROCKET_COROUTINES)),
        #              curses.A_DIM)

        canvas.addstr(16, 5, 'WOW2c' + str(len(OBSTACLES)), curses.A_DIM)
        canvas.addstr(17, 5, 'WOW2c' + str(random.choice(OBSTACLES).uid), curses.A_DIM)
        canvas.addstr(18, 5, 'WOW2c' + str(len(OBSTACLES_IN_LAST_COLLISION)),
                      curses.A_DIM)

        for _ in range(tics):
            canvas.nodelay(True)
            rows_change, columns_change, is_fire = read_controls(canvas)

            spaceship.update_spaceship_coords(
                window=window,
                rows_change=rows_change,
                columns_change=columns_change,
                border_width=border_width
            )

            #tics1 += 1
            if is_fire:
                await create_fire_shot(canvas, spaceship)

            draw_frame(
                canvas=canvas,
                start_row=spaceship.row,
                start_column=spaceship.column,
                text=frame
            )
            await asyncio.sleep(0)
            draw_frame(
                canvas=canvas,
                start_row=spaceship.row,
                start_column=spaceship.column,
                text=frame,
                negative=True
            )
