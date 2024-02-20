from tools.common_tools import get_frames_list
from tools.curses_tools import get_frame_size, Window
from physics import update_speed


class Spaceship:
    def __init__(self, window, *frame_paths):
        frames = get_frames_list(*frame_paths)
        if self._validate_frames(frames):
            self.frames = frames
            self._row_speed = 0
            self._column_speed = 0
            self._row, self._column = self._get_init_starship_coords(window)
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

    @property
    def row(self):
        return self._row

    @row.setter
    def row(self, row):
        self._row = row

    @property
    def column(self):
        return self._column

    @column.setter
    def column(self, column):
        self._column = column

    @property
    def row_speed(self):
        return self._row_speed

    @row_speed.setter
    def row_speed(self, row_speed):
        self._row_speed = row_speed

    @property
    def column_speed(self):
        return self._column_speed

    @column_speed.setter
    def column_speed(self, column_speed):
        self._column_speed = column_speed

    def update_spaceship_coords(
            self, window, rows_change=0, columns_change=0, border_width=1):

        if rows_change or columns_change:

            self._row_speed, self._column_speed = update_speed(
                self._row_speed,
                self._column_speed,
                rows_direction=rows_change,
                columns_direction=columns_change,
                fading=0.8,
            )

        else:

            self._row_speed, self._column_speed = update_speed(
                self._row_speed,
                self._column_speed,
                rows_direction=0,
                columns_direction=0,
                fading=0.8
            )

        if self._row_speed:
            max_frame_y = window.rows - self.height - border_width
            self.row = max(
                border_width,
                min(max_frame_y, self.row + self._row_speed)
            )

        if self._column_speed:
            max_frame_x = window.columns - self.width - border_width
            self.column = max(
                border_width,
                min(max_frame_x, self.column + self._column_speed)
            )

    def _get_init_starship_coords(self, window):
        if isinstance(window, Window):
            row = window.rows // 2 - self.height // 2
            column = window.columns // 2 - self.width // 2
            return row, column
        else:
            raise ValueError(f'Invalid window obj {window}')

    @staticmethod
    def _validate_frames(frames):
        heights, widths = set(), set()
        for frame in frames:
            height, width = get_frame_size(frame)
            heights.add(height)
            widths.add(width)
        return len(heights) == len(widths) == 1
