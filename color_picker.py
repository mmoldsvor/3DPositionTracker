import cv2
import numpy


class ColorPicker:
    def __init__(self, capture):
        self.video_capture = cv2.VideoCapture(capture)
        self.image_hsv = None
        self.image_mask = None

        self.upper = None
        self.lower = None

    @staticmethod
    def clamp(value, min_value=0, max_value=255):
        if value > max_value:
            value = max_value
        elif value < min_value:
            value = min_value
        return value

    def pick_color(self, event, x, y, flags, parameters):
        if event == cv2.EVENT_LBUTTONDOWN and self.image_hsv is not None:
            hue, saturation, value = self.image_hsv[x, y]
            if self.upper is None and self.lower is None:
                self.upper = [hue + 10, ColorPicker.clamp(saturation + 10), ColorPicker.clamp(value + 40)]
                self.lower = [hue - 10, ColorPicker.clamp(saturation - 10), ColorPicker.clamp(value - 40)]
            else:
                self.upper = [max(hue + 10, self.upper[0]), max(ColorPicker.clamp(saturation + 10), self.upper[1]),
                              max(ColorPicker.clamp(value + 40), self.upper[2])]
                self.lower = [min(hue - 10, self.lower[0]), min(ColorPicker.clamp(saturation - 10), self.lower[1]),
                              min(ColorPicker.clamp(value - 40), self.lower[2])]
            print(self.lower, self.upper)

    def run(self):
        _, image = self.video_capture.read()

        cv2.namedWindow('ColorPicker')
        cv2.setMouseCallback('ColorPicker', self.pick_color)

        self.image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        cv2.imshow('ColorPicker', image)

        if self.lower is not None and self.upper is not None:
            self.image_mask = cv2.inRange(self.image_hsv, numpy.array(self.lower), numpy.array(self.upper))
            cv2.imshow('mask', self.image_mask)


if __name__ == '__main__':
    done = False

    color_picker = ColorPicker(1)

    while not done:
        key = cv2.waitKey(1)
        color_picker.run()

        if key == ord('q'):
            done = True

    color_picker.video_capture.release()
    cv2.destroyAllWindows()
