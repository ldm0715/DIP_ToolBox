# pyuic5 -o main_ui.py test.ui
# pyuic5 -o gamma_ui.py gamma.ui

import sys
import os
import cv2
from PyQt5 import QtCore
from PyQt5.QtWidgets import QFrame, QMainWindow, QApplication, QFileDialog, QWidget
from PyQt5.QtGui import QPixmap, QIcon
from gamma_ui import Ui_Frame
from blur_ui import Ui_Frame
from resize_ui import Ui_Form_1
from xz_rotation import Ui_Form
from ttlb_ui import Ui_frame_2
from enhancement import *
from geometric import *
from main_ui import Ui_MainWindow
from segmentation import Segmentation
# 设置任务栏图标
import ctypes
from regional_extraction import Barcode
from kmeans_ui import Ui_widget
from feature import img_Feature, img_Match
from match_ui import Ui_Form2
from about_me import Ui_Form

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

# 项目基础路径
BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
# 图标路径
ICO_PATH = os.path.join(BASE_DIR, "./icon/favicon.ico")


class MyWindow(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__()
        self.setUi()
        self.input_path = None
        self.output_path = None
        self.state_str = None
        self.operation_str = None
        self.match_image_path = None
        self.location = None

        # 获取ui文件最顶层的对象

        # 最顶层对象的所有属性
        # print(self.ui.__dict__)
        # 获取最顶层下actionopen与actionsave对象

    def setUi(self):

        self.setupUi(self)
        openfile_action = self.actionopen
        savefile_action = self.actionsave
        gray_action = self.actionhdh_2
        binarization_action = self.actionerzhihua
        gamma_action = self.actiongamma
        equalizeHist_action = self.actionjhh
        sobel_action = self.actionsobel
        lals_action = self.actionlpls
        guass_noisy_action = self.actiongs_2
        pepper_salt_action = self.actionps
        uniform_noise_action = self.actionun
        s_change_action = self.actions
        traggle_change_action = self.actionsjx
        nei_change_action = self.actionneia
        wai_change_action = self.actionwaia
        Stagger_Cut_1_action = self.actionspcq
        Stagger_Cut_2_action = self.actionczcq
        spjx_action = self.actionspjx_2
        czjx_action = self.actionczjx_2
        spjx_czjx_action = self.actionspczfz
        guassblur_action = self.actiongs
        uniformblur_action = self.actionjz
        medianblur_action = self.actionzh
        toushi_action = self.actiontsbh
        resize_action = self.actionresize
        rotation_ation = self.actionrotate
        ttlb_action = self.actionttlb
        clear_input_button = self.pushButton
        clear_output_button = self.pushButton_2
        copy_image_button = self.pushButton_3
        regional_extraction_action = self.actiontxmtq
        actionewm_action = self.actionewm
        actioncp_action = self.actioncp
        action_kmeans = self.actionkm
        action_cdx = self.actioncdx
        actionabout_me = self.actionabout_me

        # 图像特征提取
        action_lktq = self.actionlktq_2
        action_wjy = self.actionwjy
        action_wjjz = self.actionwjjz
        action_zxwj = self.actionzxwj
        action_Hu = self.actionHu
        action_ORB = self.action_ORB

        # 给打开文件绑定槽函数
        openfile_action.triggered.connect(self.openfile)
        savefile_action.triggered.connect(self.savefile)
        gray_action.triggered.connect(self.gray_change)
        binarization_action.triggered.connect(self.binarization)
        equalizeHist_action.triggered.connect(self.equalizeHist)
        sobel_action.triggered.connect(self.sobel)
        lals_action.triggered.connect(self.laplacian)
        guass_noisy_action.triggered.connect(self.guass_noisy)
        pepper_salt_action.triggered.connect(self.pepper_salt)
        uniform_noise_action.triggered.connect(self.uniform_noise)
        s_change_action.triggered.connect(self.s_change)
        traggle_change_action.triggered.connect(self.traggle_change)
        nei_change_action.triggered.connect(self.nei_change)
        wai_change_action.triggered.connect(self.wai_change)
        Stagger_Cut_1_action.triggered.connect(self.Stagger_Cut_1)
        Stagger_Cut_2_action.triggered.connect(self.Stagger_Cut_2)
        spjx_action.triggered.connect(self.sp_mirror)
        czjx_action.triggered.connect(self.cz_mirror)
        spjx_czjx_action.triggered.connect(self.sp_cz_mirror)
        guassblur_action.triggered.connect(self.get_gaussianblur_ui)
        uniformblur_action.triggered.connect(self.get_uniformblur_ui)
        medianblur_action.triggered.connect(self.get_medianBlur_ui)
        toushi_action.triggered.connect(self.toushi_change)

        gamma_action.triggered.connect(self.gamma_ui)
        resize_action.triggered.connect(self.resize_ui)
        rotation_ation.triggered.connect(self.rotation_ui)
        ttlb_action.triggered.connect(self.ttlb_ui)

        clear_input_button.clicked.connect(self.clear_input)
        clear_output_button.clicked.connect(self.clear_output)
        copy_image_button.clicked.connect(self.copy_image)
        regional_extraction_action.triggered.connect(self.regional_extraction)

        actionewm_action.triggered.connect(self.get_qr)
        actioncp_action.triggered.connect(self.get_chepai)

        action_kmeans.triggered.connect(self.kmeans_ui)
        action_cdx.triggered.connect(self.cdx)

        # 图像特征匹配
        action_lktq.triggered.connect(self.get_contours)
        action_wjy.triggered.connect(self.get_wjy)
        action_wjjz.triggered.connect(self.get_wjjx)
        action_zxwj.triggered.connect(self.get_min_wjjx)
        action_Hu.triggered.connect(self.Hu_match_ui)
        action_ORB.triggered.connect(self.ORB_match_ui)
        actionabout_me.triggered.connect(self.about_me)

    def about_me(self):
        self.about_me_ui()

    def about_me_ui(self):
        self.window11 = about_me()
        self.window11.setWindowIcon(QIcon(ICO_PATH))
        self.window11.show()

    # 实现粘贴图像的操作
    def copy_image(self):
        self.clear_input()
        self.clear_output()
        print("目录为: %s" % os.listdir(os.path.join(BASE_DIR, "./input")))
        if len(os.listdir(os.path.join(BASE_DIR, "./input"))) > 0:
            # 移除
            os.remove(os.path.join(BASE_DIR, "./input/zhantie.png"))
            # 移除后列出目录
            print("移除后 : %s" % os.listdir(os.path.join(BASE_DIR, "./input")))
        try:
            # 创建剪切板对象
            clipboard = QApplication.clipboard()
            # 用于从剪切板读出图片
            path = clipboard.pixmap()
            out_jpg = QPixmap(path)
            fname = os.path.join(BASE_DIR, "./input/zhantie.png")
            out_jpg.save(fname)
            if len(os.listdir(os.path.join(BASE_DIR, "./input"))) > 0:
                self.input_path = fname
            if self.input_path is not None:
                self.state_str = "复制图像成功"
        except:
            self.state_str = "复制失败,剪切板为空"
        finally:
            self.show_state()
            self.show_input_image()

    # 实现打开文件操作
    def openfile(self):
        self.clear_output()
        self.clear_input()
        # 选取文件
        try:
            imgName, imgType = QFileDialog.getOpenFileName(None, "请选择要添加的文件")
            if imgName == "":
                return
            self.state_str = f"打开文件成功，文件所在路径为：{str(imgName)}"
            self.input_path = imgName
        except:
            self.state_str = "打开文件失败，检查路径是否有中文"
        finally:
            self.show_state()
            self.show_input_image()
            print(self.state_str)

    # 保存文件逻辑
    def savefile(self):
        if self.output_path != None:
            out_jpg = QPixmap(self.output_path)
            fname, ftype = QFileDialog.getSaveFileName(None, "请选择要保存的路径", "PNG files(*.png)")
            out_jpg.save(fname)
            self.state_str = "保存文件成功"
        else:
            self.state_str = "当前没有要输出图片"
        self.show_state()
        print(self.state_str)

    # 清空输入
    def clear_input(self):
        self.label.setPixmap(QPixmap(""))
        self.textBrowser.setText("")
        self.input_path = None
        self.state_str = "清空输入成功"
        self.show_state()
        print(self.state_str)

    # 清空输出
    def clear_output(self):
        self.label_2.setPixmap(QPixmap(""))
        self.textBrowser.setText("")
        self.output_path = None
        self.state_str = "清空输出成功"
        self.show_state()
        print(self.state_str)

    # 展示状态
    def show_state(self, ):
        self.textBrowser_2.setText(self.state_str)
        # 刷新
        self.textBrowser_2.repaint()

    # 展示选择的操作名称
    def show_operation(self):
        self.textBrowser.setText(self.operation_str)
        # 刷新
        self.textBrowser_2.repaint()

    # 展示处理后图片
    def show_output_image(self):
        # 加载图片文件
        jpg = QPixmap(self.output_path)
        # 显示图片
        self.label_2.setPixmap(jpg)
        # 图片自适应label
        self.label_2.setScaledContents(True)

    # 处理完成后的操作
    def finall_things(self):
        self.show_state()
        self.show_operation()
        self.show_output_image()
        print(self.state_str)

    # 展示输入图片
    def show_input_image(self):
        # 加载图片文件
        jpg = QPixmap(self.input_path)
        # 显示图片
        self.label.setPixmap(jpg)
        # 图片自适应label
        self.label.setScaledContents(True)

    # 灰度变换
    def gray_change(self):
        s = Spatial_Domain()
        try:
            self.output_path = s.Graying(self.input_path)
            self.operation_str = "灰度化"
            self.state_str = "灰度化成功"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 二值化操作
    def binarization(self):
        s = Spatial_Domain()
        try:
            self.output_path = s.Binarization(self.input_path)
            self.state_str = "二值化成功"
            self.operation_str = "二值化"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 直方图均衡化
    def equalizeHist(self):
        s = Spatial_Domain()
        try:
            self.output_path = s.EqualizeHist(self.input_path)
            self.state_str = "均衡化成功"
            self.operation_str = "均衡化"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # Sobel锐化
    def sobel(self):
        s = Spatial_Domain()
        try:
            self.output_path = s.Sobel(self.input_path)
            self.state_str = "Sobel锐化成功"
            self.operation_str = "Sobel锐化"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 拉普拉斯锐化
    def laplacian(self):
        s = Spatial_Domain()
        try:
            self.output_path = s.Laplacian(self.input_path)
            self.state_str = "Laplacian锐化成功"
            self.operation_str = "Laplacian锐化"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 高斯噪声
    def guass_noisy(self):
        s = Add_Noise()
        try:
            self.output_path = s.Guass_Noisy(self.input_path)
            self.state_str = "添加高斯噪声成功"
            self.operation_str = "添加高斯噪声"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 椒盐噪声
    def pepper_salt(self):
        s = Add_Noise()
        try:
            self.output_path = s.Pepper_Salt(self.input_path)
            self.state_str = "添加椒盐噪声成功"
            self.operation_str = "添加椒盐噪声"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 均匀噪声
    def uniform_noise(self):
        s = Add_Noise()
        try:
            self.output_path = s.Uniform_Noise(self.input_path)
            self.state_str = "添加均匀噪声成功"
            self.operation_str = "添加均匀噪声"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # s形变换
    def s_change(self):
        c = Geometric()
        try:
            self.output_path = c.SSHAPE(self.input_path)
            self.state_str = "s形变成功"
            self.operation_str = "s形变"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 三角形变
    def traggle_change(self):
        c = Geometric()
        try:
            self.output_path = c.TRIANGLE(self.input_path)
            self.state_str = "三角形变成功"
            self.operation_str = "三角形变"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 内凹
    def nei_change(self):
        c = Geometric()
        try:
            self.output_path = c.CONCAVE(self.input_path)
            self.state_str = "内凹变化成功"
            self.operation_str = "内凹"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 外凹
    def wai_change(self):
        c = Geometric()
        try:
            self.output_path = c.CONVEX(self.input_path)
            self.state_str = "外凹变化成功"
            self.operation_str = "外凹"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 水平错切
    def Stagger_Cut_1(self):
        c = Geometric()
        try:
            self.output_path, rotation = c.Stagger_Cut(self.input_path, 30, 1)
            self.state_str = "水平错切成功"
            self.operation_str = f"水平错切{rotation}"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 垂直错切
    def Stagger_Cut_2(self):
        c = Geometric()
        try:
            self.output_path, rotation = c.Stagger_Cut(self.input_path, 30, 2)
            self.state_str = "垂直错切成功"
            self.operation_str = f"垂直错切{rotation}"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 水平错切
    def sp_mirror(self):
        c = Geometric()
        try:
            self.output_path = c.Mirror_Transform(self.input_path, 1)
            self.state_str = "水平镜像变换成功"
            self.operation_str = "水平镜像"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 垂直错切
    def cz_mirror(self):
        c = Geometric()
        try:
            self.output_path = c.Mirror_Transform(self.input_path, 2)
            self.state_str = "垂直镜像变换成功"
            self.operation_str = "垂直镜像"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 水平垂直错切
    def sp_cz_mirror(self):
        c = Geometric()
        try:
            self.output_path = c.Mirror_Transform(self.input_path, 3)
            self.state_str = "水平垂直镜像变换成功"
            self.operation_str = "水平垂直镜像"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    # 透视变换
    def toushi_change(self):
        c = Geometric()
        try:
            self.get_location()
            self.output_path = c.toushi(self.input_path, self.location)
            if len(self.location) < 4:
                self.output_path = None
                self.state_str = "透视变换失败"
            else:
                self.state_str = "透视变换成功"
            self.operation_str = "透视变换"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def gamma_ui(self):
        self.window2 = Gamma_Ui()
        self.window2.setWindowIcon(QIcon(ICO_PATH))
        self.window2.show()
        self.window2.mySignal.connect(self.gamma)

    # 伽马变换
    def gamma(self, value):
        s = Spatial_Domain()
        try:
            self.output_path, gamma = s.Gamma(self.input_path, int(value))
            self.state_str = "伽马变换成功"
            self.operation_str = f"伽马变换{gamma}"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def get_gaussianblur_ui(self):
        self.window3 = Blur_UI()
        self.window3.setWindowIcon(QIcon(ICO_PATH))
        self.window3.show()
        self.window3.mySignal2.connect(self.gaussianBlur)

    # 高斯滤波
    def gaussianBlur(self, value2):
        s = Spatial_Domain()
        try:
            input = int(value2)
            size = tuple((input, input))
            self.output_path, size = s.GaussianBlur(self.input_path, size)
            self.state_str = "高斯滤波成功"
            self.operation_str = f"高斯滤波(size:{size})"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def get_uniformblur_ui(self):
        self.window4 = Blur_UI()
        self.window4.setWindowIcon(QIcon(ICO_PATH))
        self.window4.show()
        self.window4.mySignal2.connect(self.blur)

    def blur(self, value3):
        s = Spatial_Domain()
        try:
            input = int(value3)
            size = tuple((input, input))
            self.output_path, size = s.Blur(self.input_path, size)
            self.state_str = "均值滤波成功"
            self.operation_str = f"均值滤波(size:{size})"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def get_medianBlur_ui(self):
        self.window = Blur_UI()
        self.window.setWindowIcon(QIcon(ICO_PATH))
        self.window.show()
        self.window.mySignal2.connect(self.medianblur)

    def medianblur(self, value4):
        s = Spatial_Domain()
        try:
            size = int(value4)
            self.output_path, size = s.MedianBlur(self.input_path, size)
            self.state_str = "中值滤波成功"
            self.operation_str = f"中值滤波(size:{size})"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def resize_ui(self):
        # 显示界面
        self.window5 = Resize_UI()
        self.window5.setWindowIcon(QIcon(ICO_PATH))
        self.window5.show()
        # 定义接收信号后需要执行的操作
        self.window5.mySignal3.connect(self.resize_change)

    # 进行尺寸变换
    def resize_change(self, value5):
        s = Geometric()
        try:
            size = float(value5)
            self.output_path, size = s.Size_Change(self.input_path, size)
            self.state_str = "更改大小成功"
            self.operation_str = f"大小变更为原来的{size}"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def rotation_ui(self):
        self.window6 = XZ_Rotation()
        self.window6.setWindowIcon(QIcon(ICO_PATH))
        self.window6.show()
        self.window6.mySignal4.connect(self.rotation_transformation)

    def rotation_transformation(self, value6):
        s = Geometric()
        try:
            rotation = int(value6)
            self.output_path, size = s.Rotation_Transformation(self.input_path, rotation)
            self.state_str = "旋转变换成功"
            self.operation_str = f"逆时针旋转角度{rotation}°"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def ttlb_ui(self):
        self.window7 = TTLB_UI()
        self.window7.setWindowIcon(QIcon(ICO_PATH))
        self.window7.show()
        self.window7.mySignal5.connect(self.homomorphic_filter)

    def homomorphic_filter(self, rh, rl, c, d0):
        s = Frequency_Domain()
        try:
            rh = float(rh)
            rl = float(rl)
            c = float(c)
            d0 = float(d0)
            self.output_path, rl, rh, c, d0 = s.Homomorphic_Filter(self.input_path, rl, rh, c, d0)
            self.state_str = "同态滤波成功"
            self.operation_str = f"同态滤波(rl={rl},rh={rh},c={c},d0={d0})"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def get_location(self):
        # 定义输入点的列表
        self.location = list()
        # 如果当前没有输入，直接结束
        # 如果当前有输入，那么读入图像
        if self.input_path is None:
            return
        else:
            img = cv2.imread(self.input_path)

        def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
            if event == cv2.EVENT_LBUTTONDOWN:
                xy = "%d,%d" % (x, y)
                # 在界面中画出鼠标点击后的点
                cv2.circle(img, (x, y), 5, (255, 0, 0), thickness=-1)
                cv2.putText(img, xy, (x, y), cv2.FONT_HERSHEY_COMPLEX,
                            1, (0, 0, 0), thickness=1)
                # 储存点的数据
                self.location.append((x, y))
                cv2.imshow("image", img)

        cv2.namedWindow("image", 0)
        cv2.resizeWindow("image", 500, 500)
        cv2.setMouseCallback("image", on_EVENT_LBUTTONDOWN)
        cv2.imshow("image", img)
        cv2.waitKey(0)
        print(self.location)

    def regional_extraction(self):
        b = Barcode()
        try:
            self.output_path = b.get_barcode(self.input_path)
            self.state_str = "条形码定位成功"
            self.operation_str = f"条形码定位"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def get_qr(self):
        b = Barcode()
        try:
            self.output_path = b.get_qr(self.input_path)
            self.state_str = "二维码定位成功"
            self.operation_str = f"二维码定位"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def get_chepai(self):
        b = Barcode()
        try:
            self.output_path = b.chepai(self.input_path)
            self.state_str = "车牌定位成功"
            self.operation_str = f"车牌定位"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def kmeans_ui(self):
        self.window8 = KMeans_UI()
        self.window8.setWindowIcon(QIcon(ICO_PATH))
        self.window8.show()
        self.window8.mySignal6.connect(self.kmeans)

    def kmeans(self, k_input):
        s = Segmentation()
        try:
            k_input = int(k_input)
            self.output_path, k = s.kmeans(self.input_path, k_input)
            self.state_str = "KMeans图像分割成功"
            self.operation_str = f"KMeans图像分割(k={k})"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def cdx(self):
        b = Segmentation()
        try:
            # 使用界面手动获取车前范围的四个点
            self.get_location()
            self.output_path = b.get_cdx(self.input_path, self.location)
            self.state_str = "绘制车道线与车前范围成功"
            self.operation_str = f"绘制车道线与车前范围"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径，或者选取范围时出错，导致Hough变换的结果为空"
        finally:
            self.finall_things()

    def get_contours(self):
        b = img_Feature()
        try:
            self.output_path = b.get_contours(self.input_path)
            self.state_str = "绘制轮廓成功"
            self.operation_str = f"绘制轮廓"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def get_wjy(self):
        b = img_Feature()
        try:
            self.output_path = b.get_wjy(self.input_path)
            self.state_str = "绘制外接圆成功"
            self.operation_str = f"绘制外接圆"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def get_wjjx(self):
        b = img_Feature()
        try:
            self.output_path = b.get_wjjx(self.input_path)
            self.state_str = "绘制外接矩形成功"
            self.operation_str = f"绘制外接矩形"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def get_min_wjjx(self):
        b = img_Feature()
        try:
            self.output_path = b.get_min_wjjx(self.input_path)
            self.state_str = "绘制最小外接矩形成功"
            self.operation_str = f"绘制最小外接矩形"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def Hu_match_ui(self):
        self.window9 = Match_UI()
        self.window9.setWindowIcon(QIcon(ICO_PATH))
        self.window9.show()
        self.window9.mySignal7.connect(self.Hu_match)

    def Hu_match(self, path):
        b = img_Match()
        try:
            self.match_image_path = path
            self.output_path = b.Hu_match(self.input_path, self.match_image_path)
            self.state_str = "Hu矩图像匹配成功"
            self.operation_str = f"Hu矩图像匹配"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()

    def ORB_match_ui(self):
        self.window10 = Match_UI()
        self.window10.setWindowIcon(QIcon(ICO_PATH))
        self.window10.show()
        self.window10.mySignal7.connect(self.OBR_match)

    def OBR_match(self, path):
        b = img_Match()
        try:
            self.match_image_path = path
            self.output_path = b.ORB_match(self.input_path, self.match_image_path)
            self.state_str = "Hu矩图像匹配成功"
            self.operation_str = f"Hu矩图像匹配"
        except:
            if self.input_path is None:
                self.state_str = "您当前没有输入"
            else:
                self.state_str = "您当前输入有中文路径"
        finally:
            self.finall_things()


class Gamma_Ui(QFrame, Ui_Frame):
    mySignal = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Gamma_Ui, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_gamma)

    def get_gamma(self):
        gamma = self.lineEdit.text()
        self.mySignal.emit(gamma)
        self.close()


class Blur_UI(QFrame, Ui_Frame):
    mySignal2 = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Blur_UI, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_value)

    def get_value(self):
        size = self.lineEdit.text()
        self.mySignal2.emit(size)
        self.close()


class Resize_UI(QWidget, Ui_Form_1):
    mySignal3 = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Resize_UI, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_value)

    def get_value(self):
        resize = self.lineEdit.text()
        self.mySignal3.emit(resize)
        self.close()


class XZ_Rotation(QWidget, Ui_Form):
    mySignal4 = QtCore.pyqtSignal(str)

    def __init__(self):
        super(XZ_Rotation, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_value)

    def get_value(self):
        rotation = self.lineEdit.text()
        self.mySignal4.emit(rotation)
        self.close()


class TTLB_UI(QWidget, Ui_frame_2):
    mySignal5 = QtCore.pyqtSignal(str, str, str, str)

    def __init__(self):
        super(TTLB_UI, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_value)

    def get_value(self):
        rl = self.lineEdit.text()
        rh = self.lineEdit_2.text()
        c = self.lineEdit_3.text()
        d0 = self.lineEdit_4.text()
        self.mySignal5.emit(rl, rh, c, d0)
        self.close()


class KMeans_UI(QWidget, Ui_widget):
    mySignal6 = QtCore.pyqtSignal(str)

    def __init__(self):
        super(KMeans_UI, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.get_value)

    def get_value(self):
        k = self.lineEdit.text()
        self.mySignal6.emit(k)
        self.close()


class Match_UI(QWidget, Ui_Form2):
    mySignal7 = QtCore.pyqtSignal(str)

    def __init__(self):
        super(Match_UI, self).__init__()
        self.setup_ui()
        self.input_path = None

    def setup_ui(self):
        self.setupUi(self)
        input_button = self.pushButton
        clear_button = self.pushButton_2
        confirm_button = self.pushButton_3

        input_button.clicked.connect(self.openfile)
        clear_button.clicked.connect(self.clear_input)
        confirm_button.clicked.connect(self.get_value)

    # 实现打开文件操作
    def openfile(self):
        self.clear_input()
        # 选取文件
        try:
            imgName, imgType = QFileDialog.getOpenFileName(None, "请选择要添加的文件")
            if imgName == "":
                return
            print(f"打开文件成功，文件所在路径为：{str(imgName)}")
            self.input_path = imgName
        except:
            print("打开文件失败，检查路径是否有中文")
        finally:
            self.show_input_image()

    # 展示处理后图片
    def show_input_image(self):
        # 加载图片文件
        jpg = QPixmap(self.input_path)
        # 显示图片
        self.label.setPixmap(jpg)
        # 图片自适应label
        self.label.setScaledContents(True)

    # 清空输入
    def clear_input(self):
        self.label.setPixmap(QPixmap(""))
        self.input_path = None
        print("清空输入成功")

    def get_value(self):
        if self.input_path is None:
            print("当前输入为空")
        else:
            path = self.input_path
            self.mySignal7.emit(path)
            self.close()


class about_me(QFrame, Ui_Form):

    def __init__(self):
        super(about_me, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MyWindow()
    # 设置图标
    w.setWindowIcon(QIcon(ICO_PATH))
    w.setStyleSheet("#MainWindow{border-image:url(./background/background.png)}")
    w.show()
    app.exec()
