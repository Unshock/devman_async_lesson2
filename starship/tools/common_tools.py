import asyncio
import os

from settings import settings


def read_from_file(file_name):
    """Reads text from file"""

    with open(file_name, 'r') as text:
        text = text.read()
    return text


async def sleep(tics=1):
    """Custom async sleep"""
    for tic in range(tics):
        await asyncio.sleep(0)


def get_frames_list(*frames_paths):
    """Returns frames from frames_paths"""
    frames_list = []

    for frame_path in frames_paths:
        frame = read_from_file(
            os.path.join(settings.BASE_DIR, frame_path)
        )
        frames_list.append(frame)

    return frames_list
