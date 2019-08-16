import cv2
import numpy as np

image_hsv = None  # global ;(
pixel = (20, 60, 80)  # some stupid default


def clamp(value, min=0, max=255):
    if value > 255:
        return 255
    elif value < 0:
        return 0
    return value


# mouse callback function
def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y, x]

        # you might want to adjust the ranges(+-10, etc):
        upper = np.array([pixel[0] + 10, clamp(pixel[1] + 10), clamp(pixel[2] + 40)])
        lower = np.array([pixel[0] - 10, clamp(pixel[1] - 10), clamp(pixel[2] - 40)])
        print(pixel, lower, upper)

        image_mask = cv2.inRange(image_hsv, lower, upper)
        cv2.imshow("mask", image_mask)


def main():
    global image_hsv, pixel  # so we can use it in mouse callback

    video_capture = cv2.VideoCapture(1)
    _, image = video_capture.read()
    cv2.imshow("bgr", image)

    cv2.namedWindow('hsv')
    cv2.setMouseCallback('hsv', pick_color)

    # now click into the hsv img , and look at values:
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imshow("hsv", image_hsv)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
