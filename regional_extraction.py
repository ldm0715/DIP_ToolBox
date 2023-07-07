#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/11/27 14:08
# @Author : gcnanmu
import cv2
import os
import sys
import imutils
import numpy as np

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


class Barcode:

    # 条形码
    def get_barcode(self, path):
        image = cv2.imread(path)
        # 转化为灰度图像
        gray_imag = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # 高斯滤波
        gaussian_imag = cv2.GaussianBlur(gray_imag, (5, 5), 0)

        # 计算图片x和y方向的Scharr梯度大小
        ddepth = cv2.cv.CV_32F if imutils.is_cv2() else cv2.CV_32F
        gradX = cv2.Sobel(gaussian_imag, ddepth=ddepth, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gaussian_imag, ddepth=ddepth, dx=0, dy=1, ksize=-1)

        # 用x方向的梯度减去y方向的梯度
        sobel_imag = cv2.subtract(gradX, gradY)
        sobel_imag = cv2.convertScaleAbs(sobel_imag)

        # 均值滤波
        blur_image = cv2.blur(sobel_imag, (12, 12))

        # 二值化
        ret, re_img = cv2.threshold(blur_image, 200, 255, cv2.THRESH_BINARY)

        # 闭运算
        k = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
        morph_imag = cv2.morphologyEx(re_img, cv2.MORPH_CLOSE, kernel=k)

        #  执行一系列的腐蚀和膨胀操作
        closed = cv2.erode(morph_imag, None, iterations=6)
        closed = cv2.dilate(closed, None, iterations=6)

        # 找到阈值化后图片中的轮廓，然后进行根据区域进行排序，仅保留最大区域
        cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

        # 计算最大轮廓的旋转边界框
        rect = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(rect) if imutils.is_cv2() else cv2.boxPoints(rect)
        box = np.int0(box)

        # 在检测到的条形码周围绘制边界框并显示图片
        result = cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/get_barcode.png"), result)
        return os.path.join(BASE_DIR, "./output/get_barcode.png")

    # 二维码
    def get_qr(self, path):
        src_image = cv2.imread(path)
        # 实例化
        qrcoder = cv2.QRCodeDetector()
        # qr检测并解码
        codeinfo, points, straight_qrcode = qrcoder.detectAndDecode(src_image)
        # 绘制qr的检测结果
        cv2.drawContours(src_image, [np.int32(points)], 0, (0, 0, 255), 2)
        # print(points)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/get_qr.png"), src_image)
        return os.path.join(BASE_DIR, "./output/get_qr.png")

    def chepai(self, path):
        image = cv2.imread(path)
        # 转化为灰度图
        gray_imag = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # 0为不计算y方向
        gaussian_imag = cv2.GaussianBlur(gray_imag, (3, 3), 0)
        # 获得x方向的sobel锐化
        sobel_imag = cv2.Sobel(gaussian_imag, -1, 1, 0, ksize=3)
        # 二值化
        ret, binary_imag = cv2.threshold(sobel_imag, 127, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 16), np.uint8)
        # 闭运算连接车牌数字
        closed_imag = cv2.morphologyEx(binary_imag, cv2.MORPH_CLOSE, kernel=kernel)
        # 开运算去除其他部分
        opened_imag = cv2.morphologyEx(closed_imag, cv2.MORPH_OPEN, kernel=kernel)

        # 获得结构
        element = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # 对图像进行膨胀操作
        dilation_imag = cv2.dilate(opened_imag, element, iterations=3)

        # 获得举行轮廓
        contours, hierarchy = cv2.findContours(dilation_imag, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # for item in contours:
        #     rect = cv2.boundingRect(item)
        #     x = rect[0]
        #     y = rect[1]
        #     weight = rect[2]
        #     height = rect[3]
        #     if weight > (height * 2):
        #         chepai = image[y:y + height, x:x + weight]

        # image = cv2.drawContours(image, contours, -1, (0, 0, 255), 3)

        # 将轮廓规整为长方形
        rectangles = []
        for c in contours:
            x = []
            y = []
            for point in c:
                y.append(point[0][0])
                x.append(point[0][1])
            r = [min(y), min(x), max(y), max(x)]
            rectangles.append(r)

        # 用颜色识别出车牌区域
        # 需要注意的是这里设置颜色识别下限low时，可根据识别结果自行调整
        dist_r = []
        max_mean = 0
        for r in rectangles:
            block = image[r[1]:r[3], r[0]:r[2]]
            hsv = cv2.cvtColor(block, cv2.COLOR_BGR2HSV)
            low = np.array([100, 60, 60])
            up = np.array([140, 255, 255])
            result = cv2.inRange(hsv, low, up)
            # 用计算均值的方式找蓝色最多的区块
            mean = cv2.mean(result)
            if mean[0] > max_mean:
                max_mean = mean[0]
                dist_r = r

        # 画出识别结果，由于之前多做了一次膨胀操作，导致矩形框稍大了一些，因此这里对于框架+3-3可以使框架更贴合车牌
        cv2.rectangle(image, (dist_r[0] + 3, dist_r[1]), (dist_r[2] - 3, dist_r[3]), (0, 255, 0), 2)
        cv2.imwrite(os.path.join(BASE_DIR,"./output/chepai.png"),image)
        return os.path.join(BASE_DIR,"./output/chepai.png")