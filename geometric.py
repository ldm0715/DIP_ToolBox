import os
import sys
from math import sin, cos, pi, fabs, radians, tan
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


class Geometric:
    def Size_Change(self, path, size):
        image = cv2.imread(path)
        h, w, c = image.shape
        result = cv2.resize(image, (0, 0), fx=size, fy=size, interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/resize.png"), result)
        return os.path.join(BASE_DIR, "./output/resize.png"), size

    # 镜像变换
    def Mirror_Transform(self, path, type):
        image = cv2.imread(path)
        h, w, c = image.shape
        if type == 1:
            # 水平镜像
            result = cv2.flip(image, 1)
        elif type == 2:
            # 垂直镜像
            result = cv2.flip(image, 0)
        elif type == 3:
            # 水平垂直反转
            result = cv2.flip(image, -1)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/mirror_transform.png"), result)
        return os.path.join(BASE_DIR, "./output/mirror_transform.png")

    # 旋转变换
    def Rotation_Transformation(self, path, rotation):
        image = cv2.imread(path)
        w, h, c = image.shape
        rotation_numpy = cv2.getRotationMatrix2D((w // 2, h // 2), rotation, 4 / 5)
        # # 计算新的中心点
        # heightNew = int(w * fabs(sin(radians(rotation))) + h * fabs(cos(radians(rotation))))
        # widthNew = int(h * fabs(sin(radians(rotation))) + w * fabs(cos(radians(rotation))))

        # rotation_numpy[0, 2] += (widthNew - w) / 2
        # rotation_numpy[1, 2] += (heightNew - h) / 2

        result = cv2.warpAffine(image, rotation_numpy, (w, w), borderValue=(255, 255, 255))
        cv2.imwrite(os.path.join(BASE_DIR, "./output/rotation_transform.png"), result)
        return os.path.join(BASE_DIR, "./output/rotation_transform.png"), rotation

    # 三角形形变
    def TRIANGLE(self, path):
        image = cv2.imread(path)
        image_list = self.get_RBG(image)
        # print(f"外凹{len(image_list)}")
        result_list = list()
        for q in range(len(image_list)):
            gray = image_list[q]
            height, width = gray.shape
            k = width / height
            resize_gray = np.zeros([height, width], np.uint8)
            for i in range(height):
                temp = int(k * i)
                for j in range(temp):
                    # 每行非黑色区域的长度
                    distance = temp
                    # 缩小的倍率
                    ratio = distance / width
                    # 取点的步长
                    stepsize = 1.0 / ratio
                    # 将同意行缩小相同倍率
                    resize_gray[i][j] = gray[i][int((j - temp) * stepsize)]
            result_list.append(resize_gray)
        result = cv2.merge(result_list)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/triangle_transform.png"), result)
        return os.path.join(BASE_DIR, "./output/triangle_transform.png")

    # S形变
    def SSHAPE(self, path):
        image = cv2.imread(path)
        image_list = self.get_RBG(image)
        # print(f"外凹{len(image_list)}")
        result_list = list()
        for k in range(len(image_list)):
            gray = image_list[k]
            height, width = gray.shape[0], gray.shape[1]
            RANGE = int(width * 0.8)
            resize_gray = np.zeros([height, width], np.uint8)
            for i in range(height):
                # 得到正弦波的波形，即j对应的起点
                temp = float((width - RANGE) / 2 + (width - RANGE) * sin((2 * pi * i) / height + pi) / 2)
                for j in range(int(temp + 0.5), int(RANGE + temp)):
                    # 映射关系
                    m = int(((j - temp) * width / RANGE))
                    if m >= width:
                        m = width - 1
                    if m < 0:
                        m = 0
                    resize_gray[i, j] = gray[i, m]
            result_list.append(resize_gray)
        result = cv2.merge(result_list)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/sshape_transform.png"), result)
        return os.path.join(BASE_DIR, "./output/sshape_transform.png")

    # 水平外凸
    def CONVEX(self, path):
        image = cv2.imread(path)
        image_list = self.get_RBG(image)
        # print(f"外凹{len(image_list)}")
        result_list = list()
        for k in range(len(image_list)):
            gray = image_list[k]
            # print(gray)
            height, width = gray.shape
            RANGE = width * (width / height)
            resize_gray = np.zeros([height, width], np.uint8)
            for i in range(height):
                # 得到正弦波的波形，即j对应的起点
                temp = float((width - RANGE) * sin(((2 * pi * i) / height) / 2))
                temp = 200 - temp
                for j in range(int(temp + 0.5), int(width - temp)):
                    # 每行非黑色区域的长度
                    distance = int(width - temp) - int(temp + 0.5)
                    # 缩小的倍率
                    ratio = distance / width
                    # 取点的步长
                    stepsize = 1.0 / ratio
                    # 将同意行缩小相同倍率
                    resize_gray[i][j] = gray[i][int((j - temp) * stepsize)]
            result_list.append(resize_gray)
        result = cv2.merge(result_list)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/convex_transform.png"), result)
        return os.path.join(BASE_DIR, "./output/convex_transform.png")

    # 水平内凹
    def CONCAVE(self, path):
        image = cv2.imread(path)
        image_list = self.get_RBG(image)
        result_list = list()
        for k in range(len(image_list)):
            gray = image_list[k]
            height, width = gray.shape
            RANGE = int(width * 0.8)
            resize_gray = np.zeros([height, width], np.uint8)
            for i in range(height):
                # 得到正弦波的波形，即j对应的起点
                temp = float((width - RANGE) * sin(((2 * pi * i) / height) / 2))
                for j in range(int(temp + 0.5), int(width - temp)):
                    # 每行非黑色区域的长度
                    distance = int(width - temp) - int(temp + 0.5)
                    # 缩小的倍率
                    ratio = distance / width
                    # 取点的步长
                    stepsize = 1.0 / ratio
                    # 将同意行缩小相同倍率
                    resize_gray[i][j] = gray[i][int((j - temp) * stepsize)]
            result_list.append(resize_gray)
        result = cv2.merge(result_list)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/concave_transform.png"), result)
        return os.path.join(BASE_DIR, "./output/concave_transform.png")

    # 分离图像通道
    def get_RBG(self, image):
        image_list = list()
        if len(image.shape) > 2:
            w, h, d = cv2.split(image)
            image_list.append(w)
            image_list.append(h)
            image_list.append(d)
        else:
            image_list.append(image)
        return image_list

    # 错切
    def Stagger_Cut(self, path, rotation, type):
        if rotation > 45:
            rotation = 45
        if rotation < 0:
            rotation = 0
        image = cv2.imread(path)
        height, width = image.shape[:2]
        a = tan(rotation * pi / 180.0)
        height_add = int(height + width * a)
        width_add = int(width + height * a)
        if type == 1:
            zero1 = np.zeros((height_add - height, width, 3), np.uint8)
            temp_image1 = np.vstack((image, zero1))
            MAS_1 = np.float32([[1, a, 0], [0, 1, 0]])
            result = cv2.warpAffine(temp_image1, MAS_1, (width_add, height))
        elif type == 2:
            zero2 = np.zeros((height, width_add - width, 3), np.uint8)
            temp_image2 = np.hstack((image, zero2))
            MAS_2 = np.float32([[1, 0, 0], [a, 1, 0]])
            result = cv2.warpAffine(temp_image2, MAS_2, (width, height_add))
        cv2.imwrite(os.path.join(BASE_DIR, "./output/stagger_cut.png"), result)
        return os.path.join(BASE_DIR, "./output/stagger_cut.png"), rotation

    def toushi(self, path, spotlist):
        test_image = cv2.imread(path)
        width, height = 250, 350
        # 找到目标位置
        # 所需图像部分四个顶点的像素点坐标
        pts1 = np.float32(spotlist)
        # 定义对应的像素点坐标
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        # 使用getPerspectiveTransform()得到转换矩阵
        pad_rotation = cv2.getPerspectiveTransform(pts1, pts2)
        # 使用warpPerspective()进行透视变换
        result = cv2.warpPerspective(test_image, pad_rotation, (width, height))
        cv2.imwrite(os.path.join(BASE_DIR, "./output/toushi.png"), result)
        return os.path.join(BASE_DIR, "./output/toushi.png")


class Rectification:
    def Perspective(self, path, spot_list):
        test_image = cv2.imread(path)
        width, height = 250, 350  # 所需图像大小
        # 找到目标位置
        # 所需图像部分四个顶点的像素点坐标
        pts1 = np.float32([[500, 1800], [1400, 1480], [2200, 2600], [2700, 1900]])
        # 定义对应的像素点坐标
        pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
        # 使用getPerspectiveTransform()得到转换矩阵
        pad_rotation = cv2.getPerspectiveTransform(pts1, pts2)
        # 使用warpPerspective()进行透视变换
        result = cv2.warpPerspective(test_image, pad_rotation, (width, height))
        cv2.imwrite(os.path.join(BASE_DIR, "./output/perspective_transform.png"), result)
        return os.path.join(BASE_DIR, "./output/perspective_transform.png")
