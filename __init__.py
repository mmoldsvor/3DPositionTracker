import numpy
import cv2
from object_tracker import ObjectTracker
from camera import Camera
from vector import Vector
from position_plot import PositionPlot

if __name__ == '__main__':
    done = False

    lower1 = numpy.array([90, 100, 100], dtype=numpy.uint8)
    upper1 = numpy.array([110, 255, 255], dtype=numpy.uint8)
    lower2 = numpy.array([90, 60, 60], dtype=numpy.uint8)
    upper2 = numpy.array([110, 255, 255], dtype=numpy.uint8)

    tracker1 = ObjectTracker(1, (711, 400), lower1, upper1, 0)
    tracker2 = ObjectTracker(2, (711, 400), lower2, upper2, 1)
    camera1 = Camera(Vector(0, 0, 1), ((80 * numpy.pi) / 180, 0), ((60 * numpy.pi) / 180, (47 * numpy.pi) / 180),
                     tracker1)
    camera2 = Camera(Vector(1, 0, 1), ((100 * numpy.pi) / 180, 0), ((60 * numpy.pi) / 180, (47 * numpy.pi) / 180))

    plotter = PositionPlot((camera1, camera2), ((-1, 2), (-1, 2), (1, 2)))
    plotter.start()
    PositionPlot.show()

    while not done:
        tracker1.run()
        tracker2.run()
        key = cv2.waitKey(1)

        if key == ord('q'):
            done = True

        for camera in (camera1, camera2):
            camera.update_camera()

        triangulated_position = Camera.triangulate((camera1, camera2))
        if triangulated_position is not None:
            plotter.position = Vector(*triangulated_position)
        else:
            plotter.position = None

        plotter.update()
        plotter.update_draw()
        PositionPlot.pause(1)

    tracker1.video_capture.release()
    tracker2.video_capture.release()
    cv2.destroyAllWindows()

