from common_tools import get_frames_list
from curses_tools import get_frame_size


class Spaceship:
    def __init__(self, *frame_paths):
        frames = get_frames_list(*frame_paths)
        if self._validate_frames(frames):
            self.frames = frames
        else:
            raise ValueError('Frames are not valid for spaceship')

    @property
    def height(self):
        height, _ = get_frame_size(self.frames[0])
        return height

    @property
    def width(self):
        _, width = get_frame_size(self.frames[0])
        return width

    @staticmethod
    def _validate_frames(frames):
        heights, widths = set(), set()
        for frame in frames:
            height, width = get_frame_size(frame)
            heights.add(height)
            widths.add(width)
        return len(heights) == len(widths) == 1
