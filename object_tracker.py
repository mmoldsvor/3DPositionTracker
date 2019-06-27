import numpy
import cv2


class ObjectTracker:
    def __init__(self, identifier, size, lower_range, upper_range, capture=0):
        self.identifier = identifier
        self.video_capture = cv2.VideoCapture(capture)

        self.size = size
        self.center = None

        self.lower_range = lower_range
        self.upper_range = upper_range

    def run(self):
        current_frame = self.video_capture.read()[1]
        resized_frame = cv2.resize(current_frame, self.size)
        horizontal_frame = cv2.flip(resized_frame, 1)
        blurred = cv2.GaussianBlur(horizontal_frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, self.lower_range, self.upper_range)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        self.find_contours(horizontal_frame, mask)
        cv2.imshow('window{}'.format(self.identifier), horizontal_frame)

    def find_contours(self, frame, mask):
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(largest_contour)
            moments = cv2.moments(largest_contour)
            self.center = (int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00']))

            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, self.center, 5, (0, 0, 255), -1)
        else:
            self.center = None

    def get_converted_centroid(self):
        if self.center is not None:
            x, y = self.center
            width, height = self.size
            return 1 - x/width, 1 - y/height
        return None


if __name__ == '__main__':
    lower = numpy.array([90, 100, 100], dtype=numpy.uint8)
    upper = numpy.array([110, 255, 255], dtype=numpy.uint8)

    tracker = ObjectTracker((500, 500), lower, upper)

    tracker.video_capture.release()
    cv2.destroyAllWindows()
