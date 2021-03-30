from AIDetector_pytorch import Detector
from PIL import Image
from threading import Thread
import playsound
import cv2
import time

def main():
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
    #累计违规数目
    
    phone_num=0
    smoke_num=0
    drink_num=0

    func_status = {}
    func_status['headpose'] = None
    det = Detector()
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == True:
            cv2.putText(frame, "Press 'q': Quit", (10, 470),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (84, 255, 159), 2)
            b,g,r = cv2.split(frame)
            img_rgb = cv2.merge([b,g,r])
            #img_rgb =cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            start=time.time()
            result = det.feedCap(img_rgb, func_status)
            end=time.time()
            fps=1/(end-start)
            fps = "%.2f fps" % fps
            lbl=str(result['track_cls'])
            
            if lbl in ['phone','smoke','drink']:
                if not Alarm_ON:
                    Alarm_ON=True
                    if lbl=='phone':
                        phone_num
                        phone_num+=1
                        if phone_num>=3:
                            playsoundThread(sound_alarm_path_1)
                            phone_num=0
                    elif lbl=='smoke':
                        smoke_num
                        smoke_num+=1
                        if smoke_num>=3:
                            playsoundThread(sound_alarm_path_2)
                            smoke_num=0
                    elif lbl=='drink':
                        
                        drink_num
                        drink_num+=1
                        if drink_num>=3:
                            playsoundThread(sound_alarm_path_3)
                            drink_num=0
            else:
                Alarm_ON=False
            
            result = result['frame']
            cv2.putText(result, fps, (10, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            cv2.imshow('Frame of dangerous',result)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    #关闭窗口
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':

    main()
