# self implementing paint application
import cv2
import numpy as np

color = [0, 0, 0]
size = 3
radius = 5
filling = False
brushing = True
erasing = False
pressed = False
prev_x, prev_y = None, None
# paint brush icon
brush = cv2.imread('images/brush.png', 3)
brush = cv2.resize(brush, (40, 40))
eraser = cv2.imread('images/eraser.png', 3)  # eraser icon
eraser = cv2.resize(eraser, (40, 40))
fill = cv2.imread('images/fill.png', 3)  # fill icon
fill = cv2.resize(fill, (40, 40))
# to reduce the brush or eraser size
plus = cv2.imread('images/plus.png', 3)
plus = cv2.resize(plus, (40, 40))
# to increase the brush or eraser size
minus = cv2.imread('images/minus.png', 3)
minus = cv2.resize(minus, (40, 40))
red = np.full((40, 40, 3), (0, 0, 255))
magenta = np.full((40, 40, 3), (255, 0, 255))
yellow = np.full((40, 40, 3), (0, 255, 255))
green = np.full((40, 40, 3), (0, 255, 0))
cyan = np.full((40, 40, 3), (255, 255, 0))
blue = np.full((40, 40, 3), (255, 0, 0))
black = np.full((40, 40, 3), (0, 0, 0))

tools = np.hstack((brush, eraser, red, magenta,
                  yellow, green, cyan, black, blue, fill, plus, minus))
tool_bar = np.zeros((40, 1920, 3))
tool_bar[0:tools.shape[0], 0:tools.shape[1]] = tools

size_text = f'Size: {size}'


canvas = np.ones([1040, 1920, 3], 'uint8')*255  # white colored canvas


def click(event, x, y, flags, param):
    global color, size, radius, erasing, brushing, pressed, prev_x, prev_y, filling

    if event == cv2.EVENT_LBUTTONDOWN:
        if y in range(0, 40) and x in range(0, 40):  # to select brush
            brushing = True
            erasing = False
            filling = False

        if y in range(0, 40) and x in range(40, 80):  # to select eraser
            erasing = True
            brushing = False
            filling = False

        if y in range(0, 40) and x in range(80, 80+40*1):  # red
            color = (0, 0, 255)
        if y in range(0, 40) and x in range(80+40*1, 80+40*2):  # magenta
            color = (255, 0, 255)
        if y in range(0, 40) and x in range(80+40*2, 80+40*3):  # yellow
            color = (0, 255, 255)
        if y in range(0, 40) and x in range(80+40*3, 80+40*4):  # green
            color = (0, 255, 0)
        if y in range(0, 40) and x in range(80+40*4, 80+40*5):  # cyan
            color = (255, 255, 0)
        if y in range(0, 40) and x in range(80+40*5, 80+40*6):  # black
            color = (0, 0, 0)
        if y in range(0, 40) and x in range(80+40*6, 80+40*7):  # blue
            color = (255, 0, 0)
        if y in range(0, 40) and x in range(80+40*7, 80+40*8):  # blue
            filling = True
            erasing = False
            brushing = False
        if y in range(0, 40) and x in range(80+40*8, 80+40*9):  # increase the size of brush
            if size <= 66:
                size += 3
        if y in range(0, 40) and x in range(80+40*9, 80+40*10):  # decrese the size of brush
            if size >= 3:
                size -= 3
    y -= 40
    if brushing == True:
        if event == cv2.EVENT_LBUTTONDOWN:
            pressed = True
            # cv2.circle(canvas, (x, y), radius + size, color, -1)
            cv2.line(canvas, (x, y), (x, y), color, radius + size)
            prev_x, prev_y = x, y

        if event == cv2.EVENT_MOUSEMOVE and pressed:
            if prev_x is not None and prev_y is not None:
                cv2.line(canvas, (prev_x, prev_y),
                         (x, y), color, radius + size)
            prev_x, prev_y = x, y

        if event == cv2.EVENT_LBUTTONUP:
            pressed = False
            prev_x, prev_y = None, None

    if erasing == True:
        white = (255, 255, 255)
        if event == cv2.EVENT_LBUTTONDOWN:
            pressed = True
            cv2.line(canvas, (x, y), (x, y), white, radius + size)
            prev_x, prev_y = x, y

        elif event == cv2.EVENT_MOUSEMOVE and pressed == True:
            if prev_x is not None and prev_y is not None:
                cv2.line(canvas, (prev_x, prev_y),
                         (x, y), white, radius + size)
            prev_x, prev_y = x, y

        elif event == cv2.EVENT_LBUTTONUP:
            pressed = False
            prev_x, prev_y = None, None

    if filling == True:
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.floodFill(canvas, None, (x, y), color)


cv2.namedWindow('frame')
cv2.setMouseCallback('frame', click)  # this will respond to mouse clicks

while (True):
    output = np.vstack((tool_bar, canvas))
    cv2.imshow("frame", output)
    ch = cv2.waitKey(1)
    if ch & 0xFF == ord('q'):  # press q to quit the screen
        break

cv2.destroyAllWindows()
