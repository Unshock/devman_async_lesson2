import asyncio

from tools.common_tools import sleep
from settings import game_state
from tools.curses_tools import draw_frame

PHRASES = {
    1957: "First Sputnik",
    1961: "Gagarin flew!",
    1969: "Armstrong got on the moon!",
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS start building',
    2011: 'Messenger launch to Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}


def get_garbage_delay_tics(year):
    if year < 1961:
        return None
    elif year < 1969:
        return 20
    elif year < 1981:
        return 14
    elif year < 1995:
        return 10
    elif year < 2010:
        return 8
    elif year < 2020:
        return 6
    else:
        return 2


async def year_timer(tics_for_year=15):
    while True:
        await sleep(tics_for_year)
        game_state.YEAR += 1


async def show_year(window):
    canvas = window.canvas
    left_border_indent = 20

    row = 1
    column = window.columns - left_border_indent

    while True:
        if game_state.GAME_OVER:
            return

        year = game_state.YEAR

        draw_frame(canvas, row, column, f'Year: {year}')
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, f'Year: {year}', negative=True)


async def show_phrase(window, tics_for_year=15):
    canvas = window.canvas
    left_border_indent = 20
    year_indent = 3

    row = 1
    column = window.columns - left_border_indent - year_indent

    while True:
        if game_state.GAME_OVER:
            return

        phrase = PHRASES.get(game_state.YEAR, '')
        draw_frame(canvas, row, column - len(phrase), phrase)
        await sleep(tics_for_year)
        draw_frame(canvas, row, column - len(phrase), phrase, negative=True)
