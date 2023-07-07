#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/12/17 13:52
# @Author : gcnanmu
import os
import sys
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


class img_Feature:
    def get_contours(self, path, index=None):
        img = cv2.imread(path)
        # 灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 二值化
        retval, thre_imag = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        # 提取轮廓
        contours, hierarchy = cv2.findContours(thre_imag, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # # 查看提取的轮廓数量
        # print(f"轮廓的数量：{np.array(contours).shape}")

        if index is None:
            # 绘制轮廓
            draw_img1 = img.copy()

            # -1表示绘制所有轮廓
            # 0表示绘制第一条轮廓
            res1 = cv2.drawContours(draw_img1, contours, -1, (0, 0, 255), 10)

        # draw_img2 = img.copy()
        # res2 = cv2.drawContours(draw_img2, contours, 1, (255, 0, 0), 10)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/contours.png"), res1)
        return os.path.join(BASE_DIR, "./output/contours.png")

    def get_wjy(self, path, index=None):
        img = cv2.imread(path)
        # 灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 二值化
        retval, thre_imag = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        # 提取轮廓
        contours, hierarchy = cv2.findContours(thre_imag, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 绘制外接圆
        temp = img.copy()

        for i in range(len(contours)):
            (x, y), radius = cv2.minEnclosingCircle(contours[i])

            # 圆心
            center = (int(x), int(y))
            # 半径
            radius = int(radius)
            temp = cv2.circle(temp, center, radius, (0, 0, 255), 10)

        cv2.imwrite(os.path.join(BASE_DIR, "./output/wjy.png"), temp)
        return os.path.join(BASE_DIR, "./output/wjy.png")

    def get_wjjx(self, path, index=None):

        img = cv2.imread(path)
        # 灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 二值化
        retval, thre_imag = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        # 提取轮廓
        contours, hierarchy = cv2.findContours(thre_imag, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 绘制外接矩形
        temp = img.copy()

        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            temp = cv2.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 10)

        cv2.imwrite(os.path.join(BASE_DIR, "./output/wjjx.png"), temp)
        return os.path.join(BASE_DIR, "./output/wjjx.png")

    def get_min_wjjx(self, path, index=None):

        img = cv2.imread(path)
        # 灰度化
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 二值化
        retval, thre_imag = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        # 提取轮廓
        contours, hierarchy = cv2.findContours(thre_imag, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # 绘制最小外接矩形
        temp = img.copy()

        for cnt in contours:
            # 获得边界矩形（最小外接矩形）
            rbox = cv2.minAreaRect(cnt)
            # 获得矩形的四个点
            box = np.int0(cv2.boxPoints(rbox))
            temp = cv2.drawContours(temp, [box], 0, (0, 0, 255), 10)

        cv2.imwrite(os.path.join(BASE_DIR, "./output/min_wjjx.png"), temp)
        return os.path.join(BASE_DIR, "./output/min_wjjx.png")


class img_Match:
    def Hu_match(self, path1, path2):
        imag = cv2.imread(path1)
        match_image = cv2.imread(path2)
        # 灰度化
        gray = cv2.cvtColor(imag, cv2.COLOR_BGR2GRAY)
        A_image = cv2.cvtColor(match_image, cv2.COLOR_BGR2GRAY)

        # 二值化
        retval, thre_imag1 = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        retval, thre_imag2 = cv2.threshold(A_image, 100, 255, cv2.THRESH_BINARY)

        # 提取图像轮廓
        contours1, hierarchy1 = cv2.findContours(thre_imag1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # 提取模板轮廓
        contours2, hierarchy2 = cv2.findContours(thre_imag2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        print(f"原图轮廓数量：{len(contours1)}")
        print(f"模板轮廓数量：{len(contours2)}")

        temp_imag = imag.copy()
        temp_imag2 = match_image.copy()

        min_pos = -1
        min_value = 2
        for i in range(len(contours1)):
            # 参数3：匹配方法；参数4：opencv预留参数\
            value = cv2.matchShapes(contours2[0], contours1[i], 1, 0.0)
            if value < min_value:
                min_value = value
                min_pos = i

        result = cv2.drawContours(temp_imag, [contours1[min_pos]], 0, [0, 0, 255], 3)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/Hu_match.png"), result)
        return os.path.join(BASE_DIR, "./output/Hu_match.png")

    def ORB_match(self, path1, path2):
        # 读入图片
        image = cv2.imread(path1)
        match_image = cv2.imread(path2)

        # 初始化ORB
        orb = cv2.ORB_create()

        # 寻找关键点
        kp1 = orb.detect(image)
        kp2 = orb.detect(match_image)

        # 计算描述符
        # 计算哪张图片的用哪张图片的关键点。
        kp1, des1 = orb.compute(image, kp1)
        kp2, des2 = orb.compute(match_image, kp2)
        print(len(kp1), len(kp2))

        # 初始化 BFMatcher
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        # 对描述子进行匹配
        matches = bf.match(des1, des2)

        good_match = self.get_good_match(matches)

        outimage = cv2.drawMatches(image, kp1, match_image, kp2, good_match, outImg=None)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/ORB_match.png"), outimage)
        return os.path.join(BASE_DIR, "./output/ORB_match.png")

    def get_good_match(self, matches):
        # 计算最大距离和最小距离
        min_distance = matches[0].distance
        max_distance = matches[0].distance
        for x in matches:
            if x.distance < min_distance:
                min_distance = x.distance
            if x.distance > max_distance:
                max_distance = x.distance

        '''
            当描述子之间的距离大于两倍的最小距离时，认为匹配有误。
            但有时候最小距离会非常小，所以设置一个经验值30作为下限。
        '''
        good_match = []
        for x in matches:
            if x.distance <= max(2 * min_distance, 30):
                good_match.append(x)

        print(len(good_match))
        return good_match
