import numpy
import cv2
from object_tracker import ObjectTracker
from camera import Camera
from vector import Vector
from position_plot import PositionPlot

if __name__ == '__main__':
    lower = numpy.array([90, 100, 100], dtype=numpy.uint8)
    upper = numpy.array([110, 255, 255], dtype=numpy.uint8)

    tracker1 = ObjectTracker(1, (711, 400), lower, upper)
    #tracker2 = Tracker(2, (711, 400), lower, upper)
    camera1 = Camera(Vector(1, 0, 0), ((90*numpy.pi)/180, 0), ((60*numpy.pi)/180, (47*numpy.pi)/180), tracker1)
    camera2 = Camera(Vector(5, 0, 0), ((90 * numpy.pi)/180, 0), ((60*numpy.pi)/180, (47*numpy.pi)/180), tracker1)

    plotter = PositionPlot((camera1, camera2), ((0, 6), (0, 6), (0, 5)))
    plotter.start()
    PositionPlot.show()

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
        PositionPlot.pause(10)

    tracker1.video_capture.release()
    #tracker2.video_capture.release()
    cv2.destroyAllWindows()

