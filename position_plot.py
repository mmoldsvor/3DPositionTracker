from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plot
from camera import Camera

from typing import Tuple


class PositionPlot:
    def __init__(self,
                 cameras: Tuple[Camera, Camera],
                 bounds: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]] = ((0, 5), (0, 5), (0, 5))):
        """
        Plots tracked object's position in 3D space

        :param cameras: tuple (Camera, Camera)
        :param bounds: tuple ((x_0, x), (y_0, y), (z_0, z))
            The bounds of the 3D plot
        """

        self.position = None
        self.cameras = cameras

        self.bounds = bounds

        plot.ion()
        self.figure = plot.figure()
        self.axes = self.figure.add_subplot(111, projection='3d')

        # tuple (start, end, color, linestyle)
        self.lines = {'left_line': None, 'right_line': None, 'left_xy_line': None, 'right_xy_line': None,
                      'intersection_line': None}
        # tuple (x, y, z, color)
        self.points = {'object': None, 'object_xy': None}

        self.drawn_lines = {'left_line': None, 'right_line': None, 'left_xy_line': None, 'right_xy_line': None,
                            'intersection_line': None}
        self.drawn_points = {'object': None, 'object_xy': None}

    def draw_static_objects(self):
        for camera in self.cameras:
            self.draw_point(camera.position, 'red')
            for fov in camera.get_fov_xy_vectors():
                self.draw_line(camera.position, (camera.position + (fov * 7)), 'green')

    def update(self):
        left, right = tuple(camera.position for camera in self.cameras)
        average_z = (left.z + right.z) / 2
        if self.position is not None:
            self.points['object'] = (self.position, 'red')
            self.points['object_xy'] = ((*self.position.xy, average_z), 'grey')

            self.lines['left_line'] = (left, self.position, 'blue', '-')
            self.lines['right_line'] = (right, self.position, 'blue', '-')
            self.lines['left_xy_line'] = ((*left.xy, average_z), (*self.position.xy, average_z), 'grey', '--')
            self.lines['right_xy_line'] = ((*right.xy, average_z), (*self.position.xy, average_z), 'grey', '--')
            self.lines['intersection_line'] = ((*self.position.xy, average_z), self.position, 'grey', '--')
        else:
            left_vector, right_vector = tuple(camera.vector for camera in self.cameras)
            self.lines['left_line'] = (left, left + left_vector * 4, 'red', '--') if left_vector is not None else None
            self.lines['right_line'] = (
            right, right + right_vector * 4, 'red', '--') if right_vector is not None else None

    def update_draw(self):
        if self.position is not None:
            for key in self.points.keys():
                if self.points[key] is not None:
                    self.display_point(key)

            for key in self.lines.keys():
                if self.lines[key] is not None:
                    self.display_line(key)
        else:
            if None not in self.drawn_lines and None not in self.drawn_points:
                plot.cla()
                self.drawn_lines = dict.fromkeys(self.drawn_lines, None)
                self.drawn_points = dict.fromkeys(self.drawn_points, None)
                self.start()

            for key in ('left_line', 'right_line'):
                if self.lines[key] is not None:
                    self.display_line(key)

    def display_point(self, key):
        """
        Creates line or moves line if already existing
        :param key: The key of the line to display
        """
        point, color = self.points[key]
        if self.drawn_points[key] is None:
            self.drawn_points[key] = self.draw_point(point, color)
        else:
            self.drawn_points[key]._offsets3d = tuple([value] for value in point)

    def display_line(self, key):
        """
        Creates point or moves point if already existing
        :param key: The key of the line to display
        """
        start, end, color, linestyle = self.lines[key]
        if self.drawn_lines[key] is None:
            self.drawn_lines[key], = self.draw_line(start, end, color, linestyle)
        else:
            self.drawn_lines[key].set_data_3d(list(zip(start, end)))
            self.drawn_lines[key].set_linestyle(linestyle)
            self.drawn_lines[key].set_color(color)

    def draw_line(self, start: Tuple[float, float, float], end: Tuple[float, float, float], color: str = 'black',
                  linestyle: str = '-'):
        x1, y1, z1 = start
        x2, y2, z2 = end

        return self.axes.plot((x1, x2), (y1, y2), (z1, z2), color=color, linestyle=linestyle)

    def draw_point(self, point, color='black'):
        return self.axes.scatter(*point, color=color)

    def start(self):
        self.axes.set_xlabel('X Axis')
        self.axes.set_ylabel('Y Axis')
        self.axes.set_zlabel('Z Axis')

        x_bound, y_bound, z_bound = self.bounds
        self.axes.set_xlim3d(*x_bound)
        self.axes.set_ylim3d(*y_bound)
        self.axes.set_zlim3d(*z_bound)

        self.draw_static_objects()

    @staticmethod
    def pause(milliseconds):
        plot.pause(milliseconds / 1000)

    @staticmethod
    def show():
        plot.show()
