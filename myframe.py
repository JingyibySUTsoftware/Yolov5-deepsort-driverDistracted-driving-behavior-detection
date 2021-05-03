# 检测的接口函数

import cv2
import mydetect     #yolo检测
import myfatigue    #疲劳检测
import time

cap = cv2.VideoCapture(0)

def frametest(frame):
    # frame为帧输入

    # 定义返回变量
    ret = []
    labellist = []

    # 计时开始，用于计算fps
    tstart = time.time()

    # Dlib疲劳检测
    # eye 眼睛开合程度
    # mouth 嘴巴开合程度
    frame,eye,mouth = myfatigue.detfatigue(frame)
    

    # yolo检测
    action = mydetect.predict(frame)
    for label, prob, xyxy in action:
        # 在labellist加入当前label
        labellist.append(label)

        # 将标签和置信度何在一起
        text = label + str(prob)

        # 画出识别框
        left = int(xyxy[0])
        top = int(xyxy[1])
        right = int(xyxy[2])
        bottom = int(xyxy[3])
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)

        # 在框的左上角画出标签和置信度
        cv2.putText(frame,text,(left, top-5),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)

    # 将信息加入到ret中
    ret.append(labellist)
    ret.append(round(eye,3))
    ret.append(round(mouth,3))

    # 计时结束
    tend = time.time()
    # 计算fps
    fps=1/(tend-tstart)
    fps = "%.2f fps" % fps
    # 在图片的左上角标出Fps
    cv2.putText(frame,fps,(10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)

    # 返回ret 和 frame
    return ret,frame