import cv2
import os
import sys
import numpy as np

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))


class Spatial_Domain:

    def Binarization(self, path):
        image = cv2.imread(path)
        gray_imag = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, re_img = cv2.threshold(gray_imag, 200, 255, cv2.THRESH_BINARY)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/binarization.png"), re_img)
        return os.path.join(BASE_DIR, "./output/binarization.png")

    def Gamma(self, path, gamma=2.0):
        image = cv2.imread(path)
        result = np.array(255 * (image / 255) ** gamma, dtype=np.uint8)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/gamma.png"), result)
        return os.path.join(BASE_DIR, "./output/gamma.png"), gamma

    def EqualizeHist(self, path):
        image = cv2.imread(path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        result = cv2.equalizeHist(image)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/equalizeHist.png"), result)
        return os.path.join(BASE_DIR, "./output/equalizeHist.png")

    def Graying(self, path):
        image = cv2.imread(path)
        result = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/graying.png"), result)
        return os.path.join(BASE_DIR, "./output/graying.png")

    def GaussianBlur(self, path, size:tuple):
        image = cv2.imread(path)
        result = cv2.GaussianBlur(image, size, 0)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/gaussianBlur.png"), result)
        return os.path.join(BASE_DIR, "./output/gaussianBlur.png"), size

    def Blur(self, path, size: tuple):
        image = cv2.imread(path)
        result = cv2.blur(image, size, 0)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/blur.png"), result)
        return os.path.join(BASE_DIR, "./output/blur.png"), size

    def MedianBlur(self, path, size: int):
        image = cv2.imread(path)
        result = cv2.medianBlur(image, size)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/medianBlur.png"), result)
        return os.path.join(BASE_DIR, "./output/medianBlur.png"), size

    def Laplacian(self, path):
        image = cv2.imread(path)
        laplacian = cv2.Laplacian(image, cv2.CV_8UC3)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/laplacian.png"), laplacian)
        return os.path.join(BASE_DIR, "./output/laplacian.png")

    def Sobel(self, path):
        image = cv2.imread(path)
        sobelx = cv2.Sobel(image, cv2.CV_8U, 1, 0, ksize=5)
        sobely = cv2.Sobel(image, cv2.CV_8U, 0, 1, ksize=5)

        dst = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 1)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/sobel.png"), dst)
        return os.path.join(BASE_DIR, "./output/sobel.png")

    def GaussianBlur(self, path, size=(3, 3)):
        image = cv2.imread(path)
        GaussianBlur_image = cv2.GaussianBlur(image, size, 0)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/gaussianblur.png"), GaussianBlur_image)
        return os.path.join(BASE_DIR, "./output/gaussianblur.png"), size

    def Blur(self, path, size=(3, 3)):
        image = cv2.imread(path)
        Blur_image = cv2.blur(image, size)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/blur_image.png"), Blur_image)
        return os.path.join(BASE_DIR, "./output/blur_image.png"), size

    def MedianBlur(self, path, size=3):
        image = cv2.imread(path)
        medianBlur_image = cv2.medianBlur(image, size)
        cv2.imwrite(os.path.join(BASE_DIR, "./output/medianBlur_image.png"), medianBlur_image)
        return os.path.join(BASE_DIR, "./output/medianBlur_image.png"), size


class Frequency_Domain:
    # 自定义同态滤波函数
    def Homomorphic_Filter(self, path, rl, rh, c, d0):
        image = cv2.imread(path)
        # 转化为灰度图像
        gray = np.double(cv2.cvtColor(image, cv2.COLOR_RGB2GRAY))
        m, n = gray.shape

        # 获取中心点坐标
        n1 = np.floor(m / 2)
        n2 = np.floor(n / 2)

        # step1:取对数
        gray_ln = np.log(gray + 1)

        # step2：傅里叶变化
        gray_fft = np.fft.fft2(gray_ln)
        # 中心化
        gray_fftshift = np.fft.fftshift(gray_fft)

        # step3：求得H（n，v）
        # 创建与原来图像相同大小的矩阵
        # 用来存储计算后的数值
        D = np.zeros((m, n))
        H = np.zeros((m, n))
        for i in range(m):
            for j in range(n):
                D[i, j] = ((i - n1) ** 2 + (j - n2) ** 2)
                H[i, j] = (rh - rl) * (1 - (np.exp(-c * (D[i, j] / (d0 ** 2))))) + rl

        temp = H * gray_fftshift

        # step4：傅里叶反变化
        gray_ifftshift = np.fft.ifftshift(temp)
        # 反中心化
        gray_ifft = np.fft.ifft2(gray_ifftshift)

        # step5：指数操作，产生增强后的图像
        gray_exp = np.exp(gray_ifft) - 1

        # 转化为uint8，范围为[0,255]
        result = np.uint8(np.clip(gray_exp, 0, 255))
        cv2.imwrite(os.path.join(BASE_DIR, "./output/homomorphic_filter.png"), result)
        return os.path.join(BASE_DIR, "./output/homomorphic_filter.png"), rl, rh, c, d0


class Add_Noise:
    def Guass_Noisy(self, path):
        image = cv2.imread(path)
        image.astype("float")
        # 高斯噪声是满足服从正太分布，且是可加性噪声
        guass_noise = np.random.normal(0, 50, image.shape)
        guass = image + guass_noise
        # 归一化操作，将范围设置为[0,255]
        guass = np.where(guass < 0, 0, np.where(guass > 255, 255, guass))
        # 将图像进行保存
        cv2.imwrite(os.path.join(BASE_DIR, "./output/guass_noise.png"), guass)
        return os.path.join(BASE_DIR, "./output/guass_noise.png")

    def Pepper_Salt(self, path):
        image = cv2.imread(path)
        # 设置添加椒盐噪声的数目比例
        s_vs_p = 0.5
        # 设置添加噪声图像像素的数目
        amount = 0.04
        noisy_img = np.copy(image)
        # 添加salt噪声
        num_salt = np.ceil(amount * image.size * s_vs_p)
        # 设置添加噪声的坐标位置
        coords = [np.random.randint(0, i - 1, int(num_salt)) for i in image.shape]
        noisy_img[coords[0], coords[1], :] = [255, 255, 255]
        # 添加pepper噪声
        num_pepper = np.ceil(amount * image.size * (1. - s_vs_p))
        # 设置添加噪声的坐标位置
        coords = [np.random.randint(0, i - 1, int(num_pepper)) for i in image.shape]
        noisy_img[coords[0], coords[1], :] = [0, 0, 0]
        # 保存图片
        cv2.imwrite(os.path.join(BASE_DIR, "./output/pepper_salt_noisy.png"), noisy_img)
        return os.path.join(BASE_DIR, "./output/pepper_salt_noisy.png")

    def Uniform_Noise(self, path):
        image = cv2.imread(path)
        noiseUniform = np.random.uniform(0, 100, image.shape)
        imgUniformNoise = image + noiseUniform
        # 转为unit8的格式（图片格式）
        # normalize的作用是归一化，范围是[0,255]
        imgUniformNoise = np.uint8(cv2.normalize(src=imgUniformNoise, dst=None,
                                                 alpha=0, beta=255, norm_type=cv2.NORM_MINMAX))

        # 保存图片
        cv2.imwrite(os.path.join(BASE_DIR, "./output/uniform_noise.png"), imgUniformNoise)
        return os.path.join(BASE_DIR, "./output/uniform_noise.png")
