# Yolov5-deepsort-driverDistracted-driving-behavior-detection
基于深度学习的驾驶员分心驾驶行为预警系统

## 项目预览
![](https://github.com/JingyibySUTsoftware/Yolov5-deepsort-driverDistracted-driving-behavior-detection/raw/master/images/gif.gif"分心预警")



![](https://github.com/JingyibySUTsoftware/Yolov5-deepsort-driverDistracted-driving-behavior-detection/raw/master/images/SharedScreenshot.jpg"疲劳预警")

## 项目快速使用

在运行项目之前请安装好各种依赖

```shell
pip install -r requirements.txt
```



```powershell
python test.py
```

运行此文件即可使用笔记本自带摄像头进行检测

如果想使用usb外接摄像头请更改下面代码中的‘0’为您的设备号（一般为1）

```python
 cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
```

```powershell
python demo.py
```

运行此文件是检测文件中的视频，并输出检测结果

如果想检测自己的视频文件请更改下面代码中的文件路径

```python
cap = cv2.VideoCapture('testvideo/1.mp4')
```



## 文件结构说明

demo.py  视频文件检测

test.py      摄像头视频流检测

tired.py     疲劳检测代码

aieye.py    UI界面设计部分

## 警报声音

这些声音都放在了sound文件夹下，如果不喜欢这些可以换成自己的。

```python
#声音文件路径
    sound_alarm_path_1='sound\phone.mp3'
    sound_alarm_path_2='sound\smoke.mp3'
    sound_alarm_path_3='sound\drink.mp3'

    #播放声音
    def sound_alarm(alarm_path):
        playsound.playsound(alarm_path)
    #播放声音线程
    def playsoundThread(sound_alarm_path):
        t= Thread(target=sound_alarm, args=(sound_alarm_path,))
        t.daemon = True
        t.start()

    #声音播放标志
    Alarm_ON = False
```

这里为了达到实时检测的目的，没有用多线程，有时候可能会出现声音鬼畜现象。

## 实时帧率显示

```python
start=time.time()
            result = det.feedCap(img_rgb, func_status)
            end=time.time()
            fps=1/(end-start)
            fps = "%.2f fps" % fps
```



## 使用自己的模型

参考以下大佬的链接

[1]【小白CV】手把手教你用YOLOv5训练自己的数据集（从Windows环境配置到模型部署）:https://blog.csdn.net/weixin_44936889/article/details/110661862

训练好后放到 weights 文件夹下

## 项目参考

>https://github.com/Sharpiless/Yolov5-deepsort-inference
>
>遵循 GNU General Public License v3.0 协议，标明目标检测部分来源：<https://github.com/ultralytics/yolov5/>







