from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plot


class Plotter:
    def __init__(self, cameras):
        self.position = None
        self.cameras = cameras
        self.camera_positions = tuple(camera.position for camera in cameras)

        plot.ion()
        self.figure = plot.figure()
        self.axes = self.figure.add_subplot(111, projection='3d')

        self.drawn_items = {'left_line': None, 'right_line': None, 'left_xy_line': None, 'right_xy_line': None,
                            'object': None, 'intersection_line': None}

    def update(self):
        left, right = self.camera_positions
        if self.position is not None:
            if self.drawn_items['object'] is None:
                self.drawn_items['object'] = self.draw_point(self.position.xyz, 'red')
            else:
                # Quite hacky, no good solution
                self.drawn_items['object']._offsets3d = tuple([value] for value in self.position.xyz)

            if self.drawn_items['left_line'] is None:
                self.drawn_items['left_line'], = self.draw_line(left.xyz, self.position.xyz, 'blue')
            else:
                self.drawn_items['left_line'].set_data_3d(zip(left.xyz, self.position.xyz))

            if self.drawn_items['right_line'] is None:
                self.drawn_items['right_line'], = self.draw_line(right.xyz, self.position.xyz, 'blue')
            else:
                self.drawn_items['right_line'].set_data_3d(zip(right.xyz, self.position.xyz))

            if self.drawn_items['left_xy_line'] is None:
                self.drawn_items['left_xy_line'], = self.draw_line((*left.xy, 0), (*self.position.xy, 0), 'black',
                                                                   linestyle='--')
            else:
                self.drawn_items['left_xy_line'].set_data_3d(zip((*left.xy, 0), (*self.position.xy, 0)))

            if self.drawn_items['right_xy_line'] is None:
                self.drawn_items['right_xy_line'], = self.draw_line((*left.xy, 0), (*self.position.xy, 0), 'black',
                                                                    linestyle='--')
            else:
                self.drawn_items['right_xy_line'].set_data_3d(zip((*right.xy, 0), (*self.position.xy, 0)))

            if self.drawn_items['intersection_line'] is None:
                self.drawn_items['intersection_line'], = self.draw_line((*self.position.xy, 0), self.position.xyz,
                                                                        'black', linestyle='--')
            else:
                self.drawn_items['intersection_line'].set_data_3d(zip((*self.position.xy, 0), self.position.xyz))
        else:
            plot.cla()
            self.drawn_items = dict.fromkeys(self.drawn_items, None)
            self.start()

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

        self.axes.set_xlim3d(0, 6)
        self.axes.set_ylim3d(0, 6)
        self.axes.set_zlim3d(0, 5)

        for position in self.camera_positions:
            self.draw_point(position.xyz, 'red')

    def pause(self, milliseconds):
        plot.pause(milliseconds/1000)

    def show(self):
        plot.show()
