import os

PERMA_DEATH = True

TIC_TIMEOUT = 0.1
YEAR_TICS = 15
GUN_APPEARANCE_YEAR = 2020
FIRE_ALARM_PHRASE = "Use Space. Shoot 'Em Up!"

BORDER_WIDTH = 1

STARS_FULLNESS = 0.05

GARBAGE_SPEED = 0.5

BASE_DIR = 'starship'

GAME_OVER_FRAMES_DIR = 'frames/game_over'
GARBAGE_FRAMES_DIR = 'frames/garbage'
SPACESHIP_FRAMES_DIR = 'frames/spaceship'

GAME_OVER_FRAME = 'game_over.txt'

SPACESHIP_FRAMES = (
    os.path.join(SPACESHIP_FRAMES_DIR, 'rocket_frame_1.txt'),
    os.path.join(SPACESHIP_FRAMES_DIR, 'rocket_frame_2.txt')
)

GARBAGE_FRAMES = (
    os.path.join(GARBAGE_FRAMES_DIR, 'duck.txt'),
    os.path.join(GARBAGE_FRAMES_DIR, 'hubble.txt'),
    os.path.join(GARBAGE_FRAMES_DIR, 'lamp.txt'),
    os.path.join(GARBAGE_FRAMES_DIR, 'trash_large.txt'),
    os.path.join(GARBAGE_FRAMES_DIR, 'trash_small.txt'),
    os.path.join(GARBAGE_FRAMES_DIR, 'trash_xl.txt'),
)
