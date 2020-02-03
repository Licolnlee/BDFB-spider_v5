import cv2 as cv
import numpy as np

bg = cv.imread('./download/sc.png')
front = cv.imread('./download/nc.png')

bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
front = cv.cvtColor(front, cv.COLOR_BGR2GRAY)

result = cv.matchTemplate(bg, front, cv.TM_CCOEFF_NORMED)
np.argmax(result)
x, y = np.unravel_index(np.argmax(result), result.shape)

print(x, y)

w, h = front.shape
cv.rectangle(bg, (y, x), (y+w, x+h), (38,38,38), 2)



cv.imshow("gray", bg)
cv.imshow("gray2", front)
cv.waitKey(0)
cv.destroyAllWindows()