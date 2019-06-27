from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plot


class PositionPlot:
    def __init__(self, cameras, bounds=((0, 5), (0, 5), (0, 5))):
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
            self.draw_point(camera.position.xyz, 'red')
            for fov in camera.get_fov_xy_vectors():
                self.draw_line(camera.position.xyz, (camera.position + (fov*7)).xyz, 'green')

    def update(self):
        left, right = tuple(camera.position for camera in self.cameras)
        if self.position is not None:
            self.points['object'] = (self.position.xyz, 'red')
            self.points['object_xy'] = ((*self.position.xy, 0), 'grey')

            self.lines['left_line'] = (left.xyz, self.position.xyz, 'blue', '-')
            self.lines['right_line'] = (right.xyz, self.position.xyz, 'blue', '-')
            self.lines['left_xy_line'] = ((*left.xy, 0), (*self.position.xy, 0), 'grey', '--')
            self.lines['right_xy_line'] = ((*right.xy, 0), (*self.position.xy, 0), 'grey', '--')
            self.lines['intersection_line'] = ((*self.position.xy, 0), self.position.xyz, 'grey', '--')

    def update_draw(self):
        if self.position is not None:
            for key in self.points.keys():
                if self.points[key] is not None:
                    point, color = self.points[key]
                    if self.drawn_points[key] is None:
                        self.drawn_points[key] = self.draw_point(point, color)
                    else:
                        print(tuple([value] for value in point))
                        self.drawn_points[key]._offsets3d = tuple([value] for value in point)

            for key in self.lines.keys():
                if self.lines[key] is not None:
                    start, end, color, linestyle = self.lines[key]
                    if self.drawn_lines[key] is None:
                        self.drawn_lines[key], = self.draw_line(start, end, color, linestyle)
                    else:
                        self.drawn_lines[key].set_data_3d(list(zip(start, end)))
        else:
            if None not in self.drawn_lines and None not in self.drawn_points:
                plot.cla()
                self.drawn_lines = dict.fromkeys(self.drawn_lines, None)
                self.drawn_points = dict.fromkeys(self.drawn_points, None)
                self.start()
                self.draw_static_objects()

    def draw_line(self, start, end, color='black', linestyle='-'):
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

    @staticmethod
    def pause(milliseconds):
        plot.pause(milliseconds/1000)

    @staticmethod
    def show():
        plot.show()
