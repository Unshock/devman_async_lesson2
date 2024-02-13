import os
import curses
import itertools
import asyncio

from common_tools import read_from_file, sleep
from curses_tools import read_controls, get_frame_size, draw_frame
from physics import update_speed


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

    row_speed = column_speed = 0

    for frame in itertools.cycle((rocket_frame_1, rocket_frame_2)):
        frame_height, frame_width = get_frame_size(frame)

        canvas.nodelay(True)
        rows_change, columns_change, _ = read_controls(canvas)

        canvas.addstr(1, 5, 'rc'+str(round(rows_change, 3)), curses.A_DIM)
        canvas.addstr(3, 5, 'cc'+str(round(columns_change, 3)), curses.A_DIM)

        canvas.addstr(5, 5, 'rs'+str(round(row_speed, 2)), curses.A_DIM)
        canvas.addstr(7, 5, 'cs'+str(round(column_speed, 2)), curses.A_DIM)

        canvas.addstr(9, 5, 'r'+str(row), curses.A_DIM)
        canvas.addstr(11, 5, 'c'+str(column), curses.A_DIM)

        if rows_change or columns_change:

            row_speed, column_speed = update_speed(
                row_speed,
                column_speed,
                rows_direction=rows_change,
                columns_direction=columns_change,
                fading=0.8,
                #column_speed_limit=6,
                #row_speed_limit=6
            )

        else:

            row_speed, column_speed = update_speed(
                row_speed,
                column_speed,
                rows_direction=0,
                columns_direction=0,
                fading=0.8
            )

        # if abs(row_speed) < 1:
        #     row_speed = 0
        #row += row_speed
        #column += column_speed

        if row_speed:
            max_frame_y = max_y - frame_height - border_width
            row = max(
                border_width,
                min(max_frame_y, row + row_speed)
            )

        if column_speed:
            max_frame_x = max_x - frame_width - border_width
            column = max(
                border_width,
                min(max_frame_x, column + column_speed)
            )

        # if rows_change:
        #     rows_change *= speed
        #     max_frame_y = max_y - frame_height - border_width
        #     row = max(
        #         border_width,
        #         min(max_frame_y, row + rows_change)
        #     )

        # elif columns_change:
        #     columns_change *= speed
        #     max_frame_x = max_x - frame_width - border_width
        #     column = max(
        #         border_width,
        #         min(max_frame_x, column + columns_change)
        #     )

        draw_frame(canvas, row, column, frame)
        await sleep(tics=tics)
        draw_frame(canvas, row, column, frame, negative=True)
