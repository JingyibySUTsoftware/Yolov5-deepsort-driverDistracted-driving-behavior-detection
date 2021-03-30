#coding:utf-8
from AIDetector_pytorch import Detector
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import cv2
import time

class MainUi(QtWidgets.QMainWindow):
    returnSignal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.timer_camera = QTimer()  # 初始化定时器
        self.cap = cv2.VideoCapture() #初始化摄像头
        self.CAM_NUM = 0
        self.slot_init()
        self.init_ui()
    def slot_init(self):
        self.timer_camera.timeout.connect(self.show_camera)
        self.left_bt1.clicked.connect(self.slotCameraButton)
        self.left_bt2.clicked.connect(self.returnSignal)

    def show_camera(self):
        func_status = {}
        func_status['headpose'] = None
        det = Detector()
        ret, self.frame = self.cap.read()
        show = cv2.resize(self.frame,(480,320))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        cv2.putText(show, "Press 'q': Quit", (10, 470),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (84, 255, 159), 2)
        start = time.time()
        result = det.feedCap(show, func_status)
        end = time.time()
        fps = 1/(end-start)
        fps = "%.2f fps" % fps
        result = result['frame']
        cv2.putText(result, fps, (10, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        showImage = QImage(result.data, result.shape[1], result.shape[0], QImage.Format_RGB888)
        self.right_label_1.setPixmap(QPixmap.fromImage(showImage))
    #打开关闭摄像头控制
    def slotCameraButton(self):
        if self.timer_camera.isActive() == False:
    #打开摄像头并显示图像信息
            self.openCamera()
        else:
    #关闭摄像头并清空显示信息
            self.closeCamera()
    #打开摄像头
    def openCamera(self):
        flag = self.cap.open(self.CAM_NUM)
        if flag == False:
            self.left_textbrowser.append("请检测相机与电脑是否连接正确")
        else:
            self.left_textbrowser.append("打开摄像头")
            self.timer_camera.start(30)
            self.left_bt1.setText('关闭摄像头')
    def closeCamera(self):
        self.timer_camera.stop()
        self.cap.release()
        self.right_label_1.clear()
        self.left_bt1.setText('打开摄像头')
    def init_ui(self):
        self.setFixedSize(1800, 800)         
        self.main_widget = QtWidgets.QWidget()  # 创建窗口主部件         
        self.main_layout = QtWidgets.QGridLayout()  # 创建主部件的网格布局         
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局           
        
        self.left_widget = QtWidgets.QWidget()  # 创建左侧部件         
        self.left_widget.setObjectName('left_widget')         
        self.left_layout = QtWidgets.QGridLayout()  # 创建左侧部件的网格布局层         
        self.left_widget.setLayout(self.left_layout) # 设置左侧部件布局为网格           
        
        self.right_widget = QtWidgets.QWidget() # 创建右侧部件         
        self.right_widget.setObjectName('right_widget')         
        self.right_layout = QtWidgets.QGridLayout()         
        self.right_widget.setLayout(self.right_layout) # 设置右侧部件布局为网格           
        
        self.main_layout.addWidget(self.left_widget,0,0,30,8) # 左侧部件在第0行第0列，占8行3列         
        self.main_layout.addWidget(self.right_widget,0,9,30,61) # 右侧部件在第0行第3列，占8行9列         
        self.setCentralWidget(self.main_widget) # 设置窗口主部件

        
        
        self.left_close = QtWidgets.QPushButton("")  # 关闭按钮
        self.left_mini = QtWidgets.QPushButton("")  # 空白按钮
        self.left_visit = QtWidgets.QPushButton("")  # 最小化按钮

        self.left_bt1=QtWidgets.QPushButton("打开摄像头")
        self.left_bt1.setObjectName('left_button')
        self.left_bt2 = QtWidgets.QPushButton("返回")
        self.left_bt2.setObjectName('left_button')

        self.left_label_1 = QtWidgets.QLabel("疲劳检测") 
        self.left_label_1.setObjectName('left_label') 
        self.left_label_2 = QtWidgets.QLabel("疲劳时间设置(秒)")
        self.left_label_2.setObjectName('left_label_time') 
        self.left_label_3 = QtWidgets.QLabel("危险行为检测")
        self.left_label_3.setObjectName('left_label')
        self.left_label_4 = QtWidgets.QLabel("状态输出")
        self.left_label_4.setObjectName('left_label')
        self.right_label_1=QtWidgets.QLabel("用于输出异常行为的窗口")
        self.right_label_1.setObjectName('right_label_cv1')
        self.right_label_2 = QtWidgets.QLabel("用于输出疲劳驾驶部分的窗口")
        self.right_label_2.setObjectName('right_label_cv2')

        self.left_checkbox_1 = QtWidgets.QCheckBox("哈欠检测") 
        self.left_checkbox_1.setObjectName('left_checkbox')
        self.left_checkbox_2 = QtWidgets.QCheckBox("眨眼检测")
        self.left_checkbox_2.setObjectName('left_checkbox')
        self.left_checkbox_3 = QtWidgets.QCheckBox("点头检测") 
        self.left_checkbox_3.setObjectName('left_checkbox')
        self.left_checkbox_4 = QtWidgets.QCheckBox("目视前方")
        self.left_checkbox_4.setObjectName('left_checkbox')

        self.left_spinbox=QtWidgets.QSpinBox(self.left_widget)
        self.left_spinbox.setObjectName('spinbox')
        self.left_spinbox.setWrapping(False)
        self.left_spinbox.setFrame(True)

        self.left_radiobutton_1=QtWidgets.QRadioButton("喝水检测")
        self.left_radiobutton_1.setObjectName('left_radiobutton')
        self.left_radiobutton_1.setChecked(True)
        self.left_radiobutton_1.setAutoExclusive(False)
        self.left_radiobutton_2 = QtWidgets.QRadioButton("吸烟检测")
        self.left_radiobutton_2.setObjectName('left_radiobutton')
        self.left_radiobutton_2.setChecked(True)
        self.left_radiobutton_2.setAutoExclusive(False)
        self.left_radiobutton_3 = QtWidgets.QRadioButton("手机检测")
        self.left_radiobutton_3.setObjectName('left_radiobutton')
        self.left_radiobutton_3.setChecked(True)
        self.left_radiobutton_3.setAutoExclusive(False)
        self.left_radiobutton_4 = QtWidgets.QRadioButton("人脸检测")
        self.left_radiobutton_4.setObjectName('left_radiobutton')
        self.left_radiobutton_4.setChecked(True)
        self.left_radiobutton_4.setAutoExclusive(False)

        self.left_textbrowser=QtWidgets.QTextBrowser(self.left_widget)
        self.left_textbrowser.setObjectName('left_textbrowser')
        self.left_textbrowser.setReadOnly(True)




        self.left_layout.addWidget(self.left_mini, 0, 0, 1, 2) 
        self.left_layout.addWidget(self.left_close, 0, 4, 1, 2) 
        self.left_layout.addWidget(self.left_visit, 0, 2, 1, 2)
        self.left_layout.addWidget(self.left_bt1,1,0,1,4)
        self.left_layout.addWidget(self.left_bt2, 2,0,1,4)
        self.left_layout.addWidget(self.left_label_1, 3, 0, 1, 3)
        self.left_layout.addWidget(self.left_checkbox_1, 4, 0, 1, 3)
        self.left_layout.addWidget(self.left_label_2, 4, 3, 1, 3)
        self.left_layout.addWidget(self.left_spinbox, 4, 6, 1, 3)
        self.left_layout.addWidget(self.left_checkbox_2, 5, 0, 1, 3)
        self.left_layout.addWidget(self.left_checkbox_3, 5, 3, 1, 3)
        self.left_layout.addWidget(self.left_checkbox_4, 5, 6, 1, 3)
        self.left_layout.addWidget(self.left_label_3, 6, 0, 1, 3)
        self.left_layout.addWidget(self.left_radiobutton_1, 7, 0, 1, 3)
        self.left_layout.addWidget(self.left_radiobutton_2, 7, 3, 1, 3)
        self.left_layout.addWidget(self.left_radiobutton_3, 8, 0, 1, 3)
        self.left_layout.addWidget(self.left_radiobutton_4, 8, 3, 1, 3)
        self.left_layout.addWidget(self.left_label_4, 9, 0, 1, 3)
        self.left_layout.addWidget(self.left_textbrowser, 10, 0, 10, 6)
        self.right_layout.addWidget(self.right_label_1, 0, 0, 30, 30)
        self.right_layout.addWidget(self.right_label_2, 0, 30, 30, 30)


        self.left_close.setFixedSize(20, 20)  # 设置关闭按钮的大小 
        self.left_visit.setFixedSize(20, 20)  # 设置按钮大小 
        self.left_mini.setFixedSize(20, 20) # 设置最小化按钮大小

        #美化代码
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowOpacity(0.85)  # 设置窗口透明度
        self.main_layout.setSpacing(0)
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.left_close.setStyleSheet('''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''') 
        self.left_visit.setStyleSheet('''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''') 
        self.left_mini.setStyleSheet('''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')
        #self.main_widget.setStyleSheet('''background:black;''')
        self.left_widget.setStyleSheet('''
            QWidget#left_widget{     
                background:black;     
                border-top:1px solid white;     
                border-bottom:1px solid white;     
                border-left:1px solid white;     
                border-top-left-radius:10px;     
                border-bottom-left-radius:10px; 
            }
            #left_label{
            color:white;
                font-size:20px;
                font-weight:700;
                font-family:"Microsoft YaHei";
            }
            #left_button{
                color: white;
                font:bold 14px;
                background-color:#1E9FFF;
            }
            #left_checkbox{font-size:16px;font-family:"Microsoft YaHei";color:white;}
            #left_label_time{font-size:16px;font-family:"Microsoft YaHei";color:white;}
            #left_radiobutton{font-size:16px;font-family:"Microsoft YaHei";color:white;}
            QSpinBox{font-size:16px;font-family:"Microsoft YaHei";background:white;}
            #left_textbrowser{font-size:16px;font-family:"Microsoft YaHei";background-color:white;}
            
''')
        self.right_widget.setStyleSheet('''
            QWidget#right_widget{        
                color:#232C51;         
                background:white;         
                border-top:1px solid darkGray;         
                border-bottom:1px solid darkGray;         
                border-right:1px solid darkGray;         
                border-top-right-radius:10px;         
                border-bottom-right-radius:10px;     
            }
''')






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    gui = MainUi()
    gui.show()
    sys.exit(app.exec_())


