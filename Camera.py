from Vector import Vector
import math
import numpy
import cv2
from PositionPlot import Plotter
from ObjectTracker import Tracker


class Camera:
    def __init__(self, position: Vector, angle: tuple, field_of_view: tuple, tracker: Tracker=None):
        """
        Initialization of the camera instance.

        :param position: Vector (x, y, z)
            The relative position of the camera
        :param angle: tuple (x_angle, y_angle)
            The relative angle (radians) of the camera where 0 is right
        :param field_of_view: tuple (fov_x, fov_y)
            The field of view of the camera in radians
        :param ratio:
            TEMPORARY
        """

        self.position = position
        self.angle = angle
        self.field_of_view = field_of_view

        self.tracker = tracker
        self.ratio = None

    def update_ratio(self):
        if self.tracker is not None:
            self.ratio = self.tracker.get_converted_centroid()

    @staticmethod
    def triangulate(cameras: tuple):
        """
        Derives the intersection point of the object by triangulating the position in which the object is displayed
        by the two cameras
        :param cameras: tuple (Camera, Camera)
            The cameras used for triangulating the position
        :return: tuple (x, y, z)
            The position of the intersection if successful, None otherwise
        """

        if None in cameras or None in [camera.ratio for camera in cameras]:
            return None

        left, right = cameras
        vector_left, vector_right = left.calculate_vector(), right.calculate_vector()
        intersection = Camera.intersection(left.position, Vector(*vector_left.xy), right.position, Vector(*vector_right.xy))

        if intersection is not None:
            height = Camera.calculate_average_height(cameras, vector_left, vector_right, intersection)
            x, y = intersection
            return x, y, height

    @staticmethod
    def intersection(point1: Vector, vector1: Vector, point2: Vector, vector2: Vector):
        """
        Calculates the intersection point between two lines, where each line has two known points

        :param point1: Vector
            Starting point of the first line
        :param vector1: Vector
            Second point of the first line
        :param point2: Vector
            Starting point of the second line
        :param vector2:
            Second point of the second line
        :return:
            x and y value from the point of intersection between the two lines if successful, None if not
        """
        x1, y1 = point1.xy
        x2, y2 = (point1 + vector1).xy
        x3, y3 = point2.xy
        x4, y4 = (point2 + vector2).xy

        divisor = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)

        if divisor != 0:
            x = (((x1 * y2) - (y1 * x2)) * (x3 - x4) - (x1 - x2) * ((x3 * y4) - (y3 * x4))) / divisor
            y = (((x1 * y2) - (y1 * x2)) * (y3 - y4) - (y1 - y2) * ((x3 * y4) - (y3 * x4))) / divisor
            return x, y
        return None

    @staticmethod
    def calculate_average_height(cameras: tuple, left_vector: Vector, right_vector: Vector, intersection: tuple):
        """
        Calculates the average height of the object being tracked from the two cameras

        :param cameras: tuple (Camera, Camera)
        :param left_vector: Vector
            The vector pointing towards the tracked object from the left camera's point of view
        :param right_vector: Vector
            The Vector pointing towards the tracked object from the right camera's point of view
        :param intersection: tuple (x, y)
            Intersection on the xy plane between the displayed image of the two cameras
        :return: float
            The average height of the tracked object
        """
        left, right = cameras
        left_x, left_z = left_vector.xz
        right_x, right_z = right_vector.xz
        intersection_x, _ = intersection

        height_left = left_z * ((intersection_x - left.position.x)/left_x)
        height_right = right_z * ((intersection_x - right.position.x)/right_x)

        return (height_left + height_right)/2

    def calculate_vector(self):
        """
        Calculates a vector based on the camera field of view, angle and the ratio of which the object being tracked
        was detected

        :return: Vector
            The Vector directed towards the center of the tracked object
        """
        ratio_horizontal, ratio_vertical = self.ratio
        fov_horizontal, fov_vertical = self.field_of_view
        angle_horizontal, angle_vertical = self.angle

        theta_x = (ratio_horizontal*fov_horizontal - fov_horizontal/2) + angle_horizontal
        theta_y = (ratio_vertical*fov_vertical - fov_vertical/2) + angle_vertical

        return Vector(math.cos(theta_x)*math.cos(theta_y), math.sin(theta_x)*math.cos(theta_y), math.sin(theta_y))

    def get_fov_xy_vectors(self):
        """
        Generates a Vector for each direction of the field of view in the xy plane
        :return: Vector, Vector
            The Vectors describing the edge of the field of view sector
        """
        field_of_view, _ = self.field_of_view
        angle, _ = self.angle

        theta1 = field_of_view + angle - (field_of_view/2)
        theta2 = angle - (field_of_view/2)

        return Vector(math.cos(theta1), math.sin(theta1)), Vector(math.cos(theta2), math.sin(theta2))


if __name__ == '__main__':
    lower = numpy.array([90, 100, 100], dtype=numpy.uint8)
    upper = numpy.array([110, 255, 255], dtype=numpy.uint8)

    tracker1 = Tracker(1, (711, 400), lower, upper)
    #tracker2 = Tracker(2, (711, 400), lower, upper)
    camera1 = Camera(Vector(1, 0, 0), ((90*math.pi)/180, 0), ((60*math.pi)/180, (47*math.pi)/180), tracker1)
    camera2 = Camera(Vector(5, 0, 0), ((90 * math.pi)/180, 0), ((60*math.pi)/180, (47*math.pi)/180), tracker1)

    plotter = Plotter((camera1, camera2), ((0, 6), (0, 6), (0, 5)))
    plotter.start()
    Plotter.show()

    while True:
        tracker1.run()
        #tracker2.run()
        key = cv2.waitKey(1)

        if key == ord('q'):
            tracker1.video_capture.release()
            #tracker2.video_capture.release()
            cv2.destroyAllWindows()

        for camera in (camera1, camera2):
            camera.update_ratio()

        triangulated_position = Camera.triangulate((camera1, camera2))
        if triangulated_position is not None:
            plotter.position = Vector(*triangulated_position)
        else:
            plotter.position = None

        plotter.update()
        plotter.update_draw()
        Plotter.pause(10)

    tracker1.video_capture.release()
    #tracker2.video_capture.release()
    cv2.destroyAllWindows()

