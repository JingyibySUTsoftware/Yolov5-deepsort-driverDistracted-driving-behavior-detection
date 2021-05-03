import sys
import os
from glob import glob
from PySide2 import QtWidgets,QtCore,QtGui
from PySide2.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PySide2.QtCore import QDir, QTimer,Slot
from PySide2.QtGui import QPixmap,QImage
from ui_mainwindow import Ui_MainWindow
import cv2
import myframe

# 定义变量
# 眼睛长宽比
# 闪烁阈值
EYE_AR_THRESH = 0.15
EYE_AR_CONSEC_FRAMES = 2
# 打哈欠长宽比
# 闪烁阈值
MAR_THRESH = 0.65
MOUTH_AR_CONSEC_FRAMES = 3
# 初始化帧计数器和眨眼总数
COUNTER = 0
TOTAL = 0
# 初始化帧计数器和打哈欠总数
mCOUNTER = 0
mTOTAL = 0
# 行为帧数变量
ActionCOUNTER = 0
# 周期变量
Roll = 0
Rolleye = 0
Rollmouth = 0

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        # 打开文件类型，用于类的定义
        self.f_type = 0

    def window_init(self):
        # 设置控件属性
        self.label.setText("请打开摄像头")
        self.label_2.setText("疲劳检测：")
        self.label_3.setText("眨眼次数：0")
        self.label_4.setText("哈欠次数：0")
        self.label_5.setText("行为检测：")
        self.label_6.setText("手机")
        self.label_7.setText("抽烟")
        self.label_8.setText("喝水")
        self.label_9.setText("是否存在分心行为")
        self.label_10.setText("是否为疲劳状态")
        self.menu.setTitle("打开")
        self.actionOpen_camera.setText("打开摄像头")
        # 菜单按钮 槽连接 到函数
        self.actionOpen_camera.triggered.connect(CamConfig_init)
        # 自适应窗口缩放
        self.label.setScaledContents(True)
    # def printf(self, mes):
    #     self.textBrowser.append(mes)  # 在指定的区域显示提示信息
    #     self.cursot = self.textBrowser.textCursor()
    #     self.textBrowser.moveCursor(self.cursot.End)

# 定义摄像头类
class CamConfig:
    def __init__(self):
        Ui_MainWindow.printf(window,"正在打开摄像头请稍后...")
        # 设置时钟
        self.v_timer = QTimer()
        # 打开摄像头
        self.cap = cv2.VideoCapture(0)
        if not self.cap:
            Ui_MainWindow.printf(window,"打开摄像头失败")
            return
        # 设置定时器周期，单位毫秒
        self.v_timer.start(20)
        # 连接定时器周期溢出的槽函数，用于显示一帧视频
        self.v_timer.timeout.connect(self.show_pic)
        Ui_MainWindow.printf(window,"载入成功，开始运行程序")
        Ui_MainWindow.printf(window,"")
        Ui_MainWindow.printf(window,"开始执行疲劳检测...")
        window.statusbar.showMessage("正在使用摄像头...")
    def show_pic(self):
        # 全局变量
        global EYE_AR_THRESH,EYE_AR_CONSEC_FRAMES,MAR_THRESH,MOUTH_AR_CONSEC_FRAMES,COUNTER,TOTAL,mCOUNTER,mTOTAL,ActionCOUNTER,Roll,Rolleye,Rollmouth
        # 读取一帧
        success, frame = self.cap.read()
        if success:
            # Mat格式图像转Qt中图像的方法
            #检测
            ret,frame = myframe.frametest(frame)
            lab,eye,mouth = ret
            #行为判断
            ActionCOUNTER += 1
            for i in lab:
                if(i == "phone"):
                    window.label_6.setText("<font color=red>正在用手机</font>")
                    window.label_9.setText("<font color=red>请不要分心</font>")
                    if ActionCOUNTER > 0:
                        ActionCOUNTER -= 1
                elif(i == "smoke"):
                    window.label_7.setText("<font color=red>正在抽烟</font>")
                    window.label_9.setText("<font color=red>请不要分心</font>")
                    if ActionCOUNTER > 0:
                        ActionCOUNTER -= 1
                elif(i == "drink"):
                    window.label_7.setText("<font color=red>正在用喝水</font>")
                    window.label_9.setText("<font color=red>请不要分心</font>")
                    if ActionCOUNTER > 0:
                        ActionCOUNTER -= 1
            #疲劳判断
            if eye < EYE_AR_THRESH:  # 眼睛长宽比：0.2
                COUNTER += 1
                Rolleye += 1
            else:
                # 如果连续3次都小于阈值，则表示进行了一次眨眼活动
                if COUNTER >= EYE_AR_CONSEC_FRAMES:  # 阈值：3
                    TOTAL += 1
                    window.label_3.setText("眨眼次数：" + str(TOTAL))
                    # 重置眼帧计数器
                    COUNTER = 0
            if mouth > MAR_THRESH:  # 张嘴阈值0.5
                mCOUNTER += 1
                Rollmouth += 1
            else:
                # 如果连续3次都小于阈值，则表示打了一次哈欠
                if mCOUNTER >= MOUTH_AR_CONSEC_FRAMES:  # 阈值：3
                    mTOTAL += 1
                    window.label_4.setText("哈欠次数：" + str(mTOTAL))
                    # 重置嘴帧计数器
                    mCOUNTER = 0
            if ActionCOUNTER == 15:
                window.label_6.setText("手机")
                window.label_7.setText("抽烟")
                window.label_8.setText("喝水")
                window.label_9.setText("")
                ActionCOUNTER = 0
            show = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            showImage = QImage(show.data, show.shape[1], show.shape[0], QImage.Format_RGB888)
            window.label.setPixmap(QPixmap.fromImage(showImage))
            Roll += 1
            if Roll == 150:
                perclos = (Rolleye/Roll) + (Rollmouth/Roll)*0.2
                Ui_MainWindow.printf(window,"过去150帧中，Perclos得分为"+str(round(perclos,3)))
                if perclos > 0.38:
                    Ui_MainWindow.printf(window,"当前处于疲劳状态")
                    window.label_10.setText("<font color=red>疲劳！！！</font>")
                    Ui_MainWindow.printf(window,"")
                else:
                    Ui_MainWindow.printf(window,"当前处于清醒状态")
                    window.label_10.setText("清醒")
                    Ui_MainWindow.printf(window,"")
                #归零
                Roll = 0
                Rolleye = 0
                Rollmouth = 0
                Ui_MainWindow.printf(window,"重新开始执行疲劳检测...")
def CamConfig_init():
    window.f_type = CamConfig()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.window_init()
    window.show()
    sys.exit(app.exec_())