#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2022/12/7 19:48
# @Author : gcnanmu

import cv2
import os
import sys
import numpy as np

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


class Segmentation:
    def kmeans(self, path, k: int):
        image = cv2.imread(path)
        # 构建图像数据
        data = image.reshape((-1, 3))
        input_data = np.float32(data)

        # 图像分割
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        num_clusters = k
        ret, label, center = cv2.kmeans(input_data, num_clusters, None, criteria, num_clusters,
                                        cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]  # 使用flatten降维，赋予就近的中心label作为颜色值，进行分割分类

        result = res.reshape((image.shape))
        cv2.imwrite(os.path.join(BASE_DIR, "./output/kmeans_result.png"), result)
        return os.path.join(BASE_DIR, "./output/kmeans_result.png"), k

    def get_cdx(self, path, spot_list):
        # 高斯滤波
        raw = cv2.imread(path)
        guass_image = cv2.GaussianBlur(raw, (5, 5), 0)

        # 灰度化
        gray_image = cv2.cvtColor(guass_image, cv2.COLOR_BGR2GRAY)

        # Canny算子提取边缘
        canny_image = cv2.Canny(gray_image, 50, 100, (3, 3))

        # 获得掩模图像
        mask_image = self.getROI(canny_image, spot_list)
        # print(mask_image)

        # # 对图像进行腐蚀操作，去掉不需要的小白点
        # # 创建核函数
        # kernel = np.ones((1, 1), np.uint8)
        # # 腐蚀操作
        # erode_image = cv2.erode(mask_image, kernel)
        # # 膨胀操作
        # dilate_image = cv2.dilate(erode_image, kernel)

        # 获得车前范围
        mask_temp = self.getROI(gray_image, spot_list)
        trapezoid_result = cv2.HoughLinesP(mask_temp, rho=1, theta=1 * np.pi / 180, threshold=15, minLineLength=40,
                                           maxLineGap=20)

        # 初步获得车道线
        hough_result = cv2.HoughLinesP(mask_image, rho=1, theta=1 * np.pi / 180, threshold=15, minLineLength=40,
                                       maxLineGap=20)
        # print(f"Hough_result:{hough_result}")
        result_ = raw.copy()

        for spot in trapezoid_result:
            for x1, y1, x2, y2 in spot:
                cv2.line(result_, (x1, y1), (x2, y2), (176, 224, 230), 2)

        result_ = self.draw_lines(img=result_, lines=hough_result)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/cdx.png"), result_)
        return os.path.join(BASE_DIR, "./output/cdx.png")


    def draw_lines(self, img, lines, color=[255, 0, 0], thickness=2):
        left_lines_x = []
        left_lines_y = []
        right_lines_x = []
        right_lines_y = []
        line_y_max = 0
        line_y_min = 999
        for line in lines:
            for x1, y1, x2, y2 in line:
                if y1 > line_y_max:
                    line_y_max = y1
                if y2 > line_y_max:
                    line_y_max = y2
                if y1 < line_y_min:
                    line_y_min = y1
                if y2 < line_y_min:
                    line_y_min = y2
                k = (y2 - y1) / (x2 - x1)
                if k < -0.3:
                    left_lines_x.append(x1)
                    left_lines_y.append(y1)
                    left_lines_x.append(x2)
                    left_lines_y.append(y2)
                elif k > 0.3:
                    right_lines_x.append(x1)
                    right_lines_y.append(y1)
                    right_lines_x.append(x2)
                    right_lines_y.append(y2)
        # 最小二乘直线拟合
        left_line_k, left_line_b = np.polyfit(left_lines_x, left_lines_y, 1)
        right_line_k, right_line_b = np.polyfit(right_lines_x, right_lines_y, 1)
        # 根据直线方程和最大、最小的y值反算对应的x
        cv2.line(img,
                 (int((line_y_max - left_line_b) / left_line_k), line_y_max),
                 (int((line_y_min - left_line_b) / left_line_k), line_y_min),
                 color, thickness)
        cv2.line(img,
                 (int((line_y_max - right_line_b) / right_line_k), line_y_max),
                 (int((line_y_min - right_line_b) / right_line_k), line_y_min),
                 color, thickness)
        return img

    def getROI(self, image, location):
        height = image.shape[0]
        width = image.shape[1]
        # 自定义矩形范围
        triangle = np.array([location])
        print(triangle)
        # print(triangle)
        # 将范围之外的设置为黑色
        black_image = np.zeros_like(image)
        # 创建一个mask
        mask = cv2.fillPoly(black_image, triangle, 255)
        # 在原始图像上应用蒙版
        masked_image = cv2.bitwise_and(image, mask)
        # print(masked_image)
        return masked_image
