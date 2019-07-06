import numpy
import cv2
import matplotlib.pyplot as plot

from object_tracker import ObjectTracker
from camera import Camera
from vector import Vector
from position_plot import PositionPlot


if __name__ == '__main__':
    done = False

    lower = [160, 100, 100]
    upper = [190, 255, 255]

    tracker1 = ObjectTracker('Left', (711, 400), lower, upper, 2)
    tracker2 = ObjectTracker('Right', (711, 400), lower, upper, 1)
    camera1 = Camera(Vector(0, 0, 1), ((80 * numpy.pi) / 180, 0), ((60 * numpy.pi) / 180, (47 * numpy.pi) / 180),
                     tracker1)
    camera2 = Camera(Vector(1, 0, 1), ((100 * numpy.pi) / 180, 0), ((60 * numpy.pi) / 180, (47 * numpy.pi) / 180),
                     tracker2)

    plotter = PositionPlot((camera1, camera2), ((-1, 2), (-1, 2), (1, 2)))
    plotter.start()
    plot.show()

    while not done:
        tracker1.run()
        tracker2.run()
        key = cv2.waitKey(1)

        if key == ord('q'):
            done = True

        for camera in (camera1, camera2):
            camera.update_camera()

        triangulated_position = Camera.triangulate((camera1, camera2))
        plotter.position = Vector(*triangulated_position) if triangulated_position is not None else None

        plotter.update_values()
        plotter.update_draw()
        plot.pause(0.001)

    tracker1.video_capture.release()
    tracker2.video_capture.release()
    cv2.destroyAllWindows()

