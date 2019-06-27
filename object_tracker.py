import cv2


class ObjectTracker:
    def __init__(self, identifier: int, size, lower_range, upper_range, capture=0):
        """
        Initializes a tracker that can keep track on a single object in a specified color range.
        Tracks the largest contour of specified color

        :param identifier: int
            A integer which specifies what window the image should be rendered on. Different trackers should have unique
            identifiers
        :param size: tuple (x, y)
            Specifies the size the captured frame should be scaled down to
        :param lower_range: numpy.array([hue - 10, 100, 100], dtype=numpy.uint8)
            Specifies the lower end of the hue value of the object being tracked
        :param upper_range: numpy.array([hue + 10, 255, 255], dtype=numpy.uint8)
            Specifies the upper end of the hue value of the object being tracked
        :param capture: int or string
            The capturing device being used by the tracker, be it video file or camera
        """
        self.identifier = identifier
        self.video_capture = cv2.VideoCapture(capture)

        self.size = size
        self.center = None

        self.lower_range = lower_range
        self.upper_range = upper_range

    def run(self):
        """
        Captures and modifies picture to mask out contours to be tracked. Renders bounding box and centroid
        """
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
        """
        Finds the largest contour of given color based on mask parameter. Renders bounding box and center of object,
        and sets the center value if contour is found, None otherwise
        :param frame: numpy.array
             The cv2 representation of the image
        :param mask:
            The mask derived from the modified image
        """
        contours = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        if len(contours) > 0:
            largest_contour = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(largest_contour)
            moments = cv2.moments(largest_contour)
            self.center = (int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00']))

            if w > 10 and h > 10:
                cv2.rectangle(frame, (int(x), int(y)), (int(x+w), int(y+h)), (0, 255, 255), 2)
                cv2.circle(frame, self.center, 5, (0, 0, 255), -1)
        else:
            self.center = None

    def get_converted_centroid(self):
        """
        Converts and returns the center position of the largest contour. The values are translated from image position
        to a range from 0 to 1 based on image size.
        :return: tuple (x, y)
            The position of the center translated from 0 to 1 of currently tracked object if such value exist.
            None otherwise
        """
        if self.center is not None:
            x, y = self.center
            width, height = self.size
            return 1 - x/width, 1 - y/height
        return None
