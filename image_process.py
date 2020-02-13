import cv2 as cv
import numpy as np


class image_process( ):

    def show(self, name):
        cv.imshow('Show', name)
        cv.waitKey(0)
        cv.destroyAllWindows( )

    def process(self):
        bg = cv.imread('./error/error_sc1.png', 1)
        front = cv.imread('./error/error_nc1.png', 1)
        print(bg.shape)
        print(front.shape)
        for i in range(bg.shape[0]):
            for j in range(bg.shape[1]):
                if bg[i][j][0] >= 157 and bg[i][j][1] >= 157 and bg[i][j][2] >= 157:
                    bg[i][j] = (0, 0, 0)
        bg = cv.GaussianBlur(bg, (1, 1), -10)
        front = cv.cvtColor(front, cv.COLOR_BGR2GRAY)
        bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
        # ret, bg = cv.threshold(bg, 127, 255, cv.THRESH_TOZERO)
        # ret, front = cv.threshold(front, 127, 255, cv.THRESH_TOZERO)


        result = cv.matchTemplate(bg, front, cv.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(np.argmax(result), result.shape)
        print(x, y)

        w, h = front.shape
        cv.rectangle(bg, (y, x), (y + w, x + h), (7, 249, 151), 2)
        cv.imwrite("gray.jpg", bg)
        self.show(bg)

        return x, y






ip = image_process( )
ip.process( )