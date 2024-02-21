import curses
import itertools
import asyncio
import os

from starship.explosion import explode
from starship.settings.game_state import OBSTACLES
from starship.tools.common_tools import read_from_file, sleep
from starship.tools.curses_tools import read_controls, get_frame_size, \
    draw_frame
from starship.settings import settings, game_state

GAME_OVER_DIR = os.path.join(settings.BASE_DIR, settings.GAME_OVER_FRAMES_DIR)


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
    max_row = rows - settings.BORDER_WIDTH
    max_column = columns - settings.BORDER_WIDTH

    curses.beep()

    while 1 < row < max_row and 0 < column < max_column:

        for obstacle in game_state.OBSTACLES:
            if obstacle.has_collision(row, column):
                game_state.OBSTACLES_IN_LAST_COLLISION.add(obstacle)
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
    """Creates fire shot and adds it to the fire shots coroutine"""

    fire_shot_column = spaceship.column + spaceship.width // 2
    fire_shot_row = spaceship.row - 1  # above the starship

    fire_shot_coroutine = fire(
        canvas,
        start_row=fire_shot_row + spaceship.row_speed,
        start_column=fire_shot_column + spaceship.column_speed,
        rows_speed=-0.9
    )

    game_state.coroutines.insert(0, fire_shot_coroutine)


async def show_fire_alarm(window):
    """Coroutine that will show fire alarm when GUN_APPEARANCE_YEAR comes"""
    while True:
        if game_state.YEAR >= settings.GUN_APPEARANCE_YEAR:
            coroutine = create_fire_alarm(window)
            game_state.coroutines.append(coroutine)
            return
        await asyncio.sleep(0)


async def create_fire_alarm(window):
    """Shows the alarm the fire gun is ready to shoot"""

    alarm_phrase = settings.FIRE_ALARM_PHRASE
    canvas = window.canvas

    row = window.rows // 2
    column = window.columns // 2 - len(alarm_phrase) // 2

    for _ in range(5):
        canvas.addstr(row, column, alarm_phrase, curses.A_DIM)
        await sleep(1)

        canvas.addstr(row, column, alarm_phrase)
        await sleep(1)

        canvas.addstr(row, column, alarm_phrase, curses.A_BOLD)
        await sleep(1)

        canvas.addstr(row, column, alarm_phrase)
        await sleep(1)

    canvas.addstr(row, column, alarm_phrase, curses.A_INVIS)


async def show_game_over(window):
    """Displays the Game Over banner"""
    game_over = read_from_file(
        os.path.join(GAME_OVER_DIR, settings.GAME_OVER_FRAME)
    )
    game_over_height, game_over_width = get_frame_size(game_over)

    game_over_row = window.rows // 2 - game_over_height // 2
    game_over_column = window.columns // 2 - game_over_width // 2

    canvas = window.canvas

    while True:
        draw_frame(canvas, game_over_row, game_over_column, game_over)
        await asyncio.sleep(0)
        draw_frame(canvas, game_over_row, game_over_column, game_over, True)


async def run_spaceship(window, spaceship, border_width=1, tics=2):
    """
    Async func that runs the spaceship, arranges fire shots
    and computes spaceship collisions.
    """

    canvas = window.canvas

    for frame in itertools.cycle(spaceship.frames):

        for _ in range(tics):
            canvas.addstr(3, 3, str(len(OBSTACLES)), curses.A_BOLD) ########
            canvas.nodelay(True)
            rows_change, columns_change, is_fire = read_controls(canvas)

            spaceship.update_spaceship_coords(
                window=window,
                rows_change=rows_change,
                columns_change=columns_change,
                border_width=border_width
            )

            for obstacle in game_state.OBSTACLES:
                if settings.PERMA_DEATH and obstacle.has_collision(
                        obj_corner_row=spaceship.row,
                        obj_corner_column=spaceship.column,
                        obj_size_rows=spaceship.height,
                        obj_size_columns=spaceship.width):
                    game_state.GAME_OVER = True
                    explosion_row = spaceship.row + spaceship.height // 2
                    explosion_column = spaceship.column + spaceship.width // 2
                    await explode(canvas, explosion_row, explosion_column)
                    game_state.coroutines.append(show_game_over(window))
                    return

            if is_fire and game_state.YEAR >= settings.GUN_APPEARANCE_YEAR:
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
