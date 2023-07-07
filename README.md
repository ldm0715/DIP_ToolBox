<p align="center">
  <img width="15%" align="center" src="https://z4a.net/images/2023/07/07/DIP_ToolBox_logo1.png" alt="logo">
</p>
  <h1 align="center">
  DIP ToolBox
</h1>
<p align="center">
<img src="https://img.shields.io/badge/Version-v1.0-green?style=flat&logo">
<img src="https://img.shields.io/badge/Platform-Win|macOS-blue?color=#4ec820" alt="Platform Win|macOS"/>
<img src="https://img.shields.io/badge/Python-3.7%20-blue?color=#4ec820" alt="Python 3.7"/>
</p>
<p align="center">
  图像处理小工具
</p>

<p align="center">
  <img width="40%" align="center" src="https://z4a.net/images/2023/07/07/DIP_ToolBox_ui.png" alt="ui">
</p>

## 运行与使用说明

本界面使用`PyQt5`编写，相关代码可以在项目文件中查看，其中保留了`.ui`文件 ，有需要可以自取更改。

本程序实现了以下经典的数字图像处理功能：

- [x] 图像打开、保存、粘贴
- [x] 空间域处理
  1. 点运算
  2. 平滑
  3. 锐化
- [x] 频域处理：同态滤波
- [x] 添加噪声：高斯、椒盐、均匀噪声
- [x] 几何变换
  1. 常规
  2. 哈哈镜效果
- [x] 图像矫正：透视变换（鼠标手动定位）
- [x] 区域定位
  1. 条形码区域识别
  2. 二维码区域识别
  3. 车牌区域识别
- [x] 图像分割
  1. KMeans图像分割
  2. 车道线检测
- [x] 图像特征提取
  1. 几何形状特征
  2. 图像匹配

## 使用方法

项目文件结构：

```Dir Tree
DIP_ToolBox
├─ DIP_ToolBox.exe
├─ background
│    └─ background.png
├─ icon
│    ├─ favicon.ico
│    ├─ logo1.png
│    └─ logo2.png
├─ input
│    └─ zhantie.png
└─ output
       ├─ binarization.png
       └─ graying.png
```

本工具为傻瓜式操作，但是**需要知道相应文件夹的作用，否则会出现无法使用的情况。**

|   文件夹   |             作用             |
| :--------: | :--------------------------: |
|    ico     |      储存执行程序的图标      |
| background |      储存执行程序的背景      |
|   input    | 储存粘贴图像（没有就会报错） |
|   output   |       处理后的输出图像       |

## 注意事项

这是早期的课设作品，由于本人水平有限，测试时在大部分场景应该是没问题的，但肯定也有其他问题。由于精力有限，无法继续更新，仅供大家参考。最后**祝大家使用愉快**。

Copyright © 2023 by gcnanmu.
