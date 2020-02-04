import cv2 as cv
import numpy as np


class image_process( ):

    def show(self, name):
        cv.imshow('Show', name)
        cv.waitKey(0)
        cv.destroyAllWindows( )

    def process(self):
        bg = cv.imread('./download/sc5.png')
        front = cv.imread('./download/nc5.png')

        bg = cv.GaussianBlur(bg, (1, 1), -10)
        front = cv.cvtColor(front, cv.COLOR_BGR2GRAY)
        bg = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
        # bg = cv.Canny(bg, 100, 100)
        result = cv.matchTemplate(bg, front, cv.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(np.argmax(result), result.shape)
        print(x, y)

        w, h = front.shape
        cv.rectangle(bg, (y, x), (y + w, x + h), (7, 249, 151), 2)
        cv.imwrite("gray.jpg", bg)
        self.show(bg)

        return x, y
        # temp = 'temp.png'
        # targ = 'targ.png'
        # cv.imwrite(temp, oblk)
        # cv.imwrite(targ, otemp)
        # target = cv.imread(targ)
        # target = cv.cvtColor(target, cv.COLOR_BGR2GRAY)
        # target = abs(255 - target)
        # cv.imwrite(targ, target)
        # target = cv.imread(targ)
        # template = cv.imread(temp)
        # result = cv.matchTemplate(target, template, cv.TM_CCOEFF_NORMED)
        # x, y = np.unravel_index(np.argmax(result), result.shape)

        # target = cv.cvtColor(bg, cv.COLOR_BGR2GRAY)
        # # target = abs(255 - target)
        # template = cv.cvtColor(front, cv.COLOR_BGR2GRAY)
        # template = abs(255 - template)
        #
        # result = cv.matchTemplate(target, template, cv.TM_CCOEFF_NORMED)
        # np.argmax(result)
        # x, y = np.unravel_index(np.argmax(result), result.shape)
        # # return x, y
        # #
        # print(x, y)
        #
        # w, h = template.shape
        # cv.rectangle(target, (y, x), (y + w, x + h), (7, 249, 151), 2)
        # cv.imwrite("gray.jpg", target)
        # self.show(target)
        # return x, y


ip = image_process( )
ip.process( )

# # 对滑块进行二值化处理
# def handle_img1(image):
#     kernel = np.ones((8, 8), np.uint8)  # 去滑块的前景噪声内核
#     gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
#     width, heigth = gray.shape
#     for h in range(heigth):
#         for w in range(width):
#             if gray[w, h] == 0:
#                 gray[w, h] = 96
#     # cv.imshow('gray', gray)
#     binary = cv.inRange(gray, 96, 96)
#     res = cv.morphologyEx(binary, cv.MORPH_OPEN, kernel)  # 开运算去除白色噪点
#     # cv.imshow('res', res)
#     return res
#
#
# # 模板匹配(用于寻找缺口有点误差)
# def template_match(img_target, img_template):
#     tpl = handle_img1(img_template)  # 误差来源就在于滑块的背景图为白色
#     blurred = cv.GaussianBlur(img_target, (3, 3), 0)  # 目标图高斯滤波
#     gray = cv.cvtColor(blurred, cv.COLOR_BGR2GRAY)
#     ret, target = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)  # 目标图二值化
#     # cv.imshow("template", tpl)
#     # cv.imshow("target", target)
#     method = cv.TM_CCOEFF_NORMED
#     width, height = tpl.shape[:2]
#     result = cv.matchTemplate(target, tpl, method)
#     min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
#     left_up = max_loc
#     right_down = (left_up[0] + height, left_up[1] + width)
#     cv.rectangle(img_target, left_up, right_down, (0, 0, 255), 2)
#     cv.imshow('res', img_target)
#
#
# if __name__ == '__main__':
#     img0 = cv.imread('./download/sc.png')
#     img1 = cv.imread('./download/nc.png')
#     template_match(img0, img1)
#     cv.waitKey(0)
#     cv.destroyAllWindows()
