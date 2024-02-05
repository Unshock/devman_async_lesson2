import os
import curses
import itertools
import asyncio

from common_tools import read_from_file
from curses_tools import read_controls, get_frame_size, draw_frame


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
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed


async def blink(canvas, row, column, symbol='*', delay=0):
    """Display animation of blinking star"""

    for tic in range(delay):
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await asyncio.sleep(0)

    while True:

        for tic in range(20):
            canvas.addstr(row, column, symbol, curses.A_DIM)
            await asyncio.sleep(0)

        for tic in range(3):
            canvas.addstr(row, column, symbol)
            await asyncio.sleep(0)

        for tic in range(5):
            canvas.addstr(row, column, symbol, curses.A_BOLD)
            await asyncio.sleep(0)

        for tic in range(3):
            canvas.addstr(row, column, symbol)
            await asyncio.sleep(0)


async def animate_spaceship(canvas, border_width=1, tics=2, speed=1):
    """Display animation of flying starship"""

    rocket_frame_1 = read_from_file(
        os.path.join(os.path.dirname(__file__), 'frames/rocket_frame_1.txt'))
    rocket_frame_2 = read_from_file(
        os.path.join(os.path.dirname(__file__), 'frames/rocket_frame_2.txt'))

    rocket_height, rocket_width = get_frame_size(rocket_frame_1)

    max_y, max_x = canvas.getmaxyx()
    row = max_y // 2 - rocket_height // 2
    column = max_x // 2 - rocket_width // 2

    for frame in itertools.cycle((rocket_frame_1, rocket_frame_2)):
        frame_height, frame_width = get_frame_size(frame)

        for tic in range(tics):
            canvas.nodelay(True)
            rows_change, columns_change, _ = read_controls(canvas)

            if rows_change:
                rows_change *= speed
                max_frame_y = max_y - frame_height - border_width
                row = max(
                    border_width,
                    min(max_frame_y, row + rows_change)
                )

            elif columns_change:
                columns_change *= speed
                max_frame_x = max_x - frame_width - border_width
                column = max(
                    border_width,
                    min(max_frame_x, column + columns_change)
                )

            draw_frame(canvas, row, column, frame)
            await asyncio.sleep(0)
            draw_frame(canvas, row, column, frame, negative=True)
