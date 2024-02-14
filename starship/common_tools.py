import asyncio
import os


def read_from_file(file_name):
    """Reads text from file"""

    with open(file_name, 'r') as text:
        text = text.read()
    return text


async def sleep(tics=1):
    for tic in range(tics):
        await asyncio.sleep(0)


def get_frames_list(*frames_paths):
    frames_list = []

    for frame_path in frames_paths:
        frame = read_from_file(
            os.path.join(os.path.dirname(__file__), frame_path)
        )
        frames_list.append(frame)

    return frames_list
