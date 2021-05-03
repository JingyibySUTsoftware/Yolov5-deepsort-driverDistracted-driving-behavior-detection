import cv2
import mydetect
import myfatigue
import time

cap = cv2.VideoCapture(0)

def frametest(frame):
    ret = []
    labellist = []
    tstart = time.time()
    action = mydetect.predict(frame)
    for label, prob, xyxy in action:
        labellist.append(label)
        text = label + str(prob)
        left = int(xyxy[0])
        top = int(xyxy[1])
        right = int(xyxy[2])
        bottom = int(xyxy[3])
        cv2.putText(frame,text,(left, top-5),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
    ret.append(labellist)
    frame,eye,mouth = myfatigue.detfatigue(frame)
    ret.append(round(eye,3))
    ret.append(round(mouth,3))
    #print(eye,mouth)
    tend = time.time()
    fps=1/(tend-tstart)
    fps = "%.2f fps" % fps
    cv2.putText(frame,fps,(10, 20),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 1)
    return ret,frame