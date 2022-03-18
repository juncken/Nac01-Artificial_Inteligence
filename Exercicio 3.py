
import cv2
from matplotlib import pyplot as plt
import numpy as np
import math


def calculo(mask, frame):
    gray = frame.copy()
    gray = cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
    calc_cont, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    centers = []
    for i in range(len(calc_cont)):
        moments = cv2.moments(calc_cont[i])
        centers.append((int(moments['m10']/moments['m00']), int(moments['m01']/moments['m00'])))
        


    frame_img = frame.copy()


    if len(centers) == 2:

        cx1=centers[0][0]
        cx2=centers[1][0]
        cy1=centers[0][1]
        cy2=centers[1][1]

        cv2.line(frame_img,(cx1,cy1),(cx2, cy2),(93, 18, 199),2)

        if (cx1 - cx2) == 0:
            m1 = (cy1 - cy2)
            m2 = (cy2 - cy2)
        else:
            m1 = (cy1 - cy2)/(cx1 - cx2)
            m2 = (cy2 - cy2)/(cx1 - cx2)
        
        angulo = math.atan((m2-m1)/(1-(m2*m1)))
        angulo_graus = round(math.degrees(angulo))


        font = cv2.FONT_HERSHEY_SIMPLEX
        text = f'Angulo da reta: {angulo_graus}'
        textsize = cv2.getTextSize(text, font, 1, 1)[0]

        textX = int((frame_img.shape[1] - textsize[0]) / 2)
        textY = int((frame_img.shape[0] + textsize[1]) / 2)
        cv2.putText(frame_img, text, (textX, textY), font, 1, (100, 255, 255), 1)
        return frame_img
    
    return frame

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)


if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False
    
while rval:
    frame = cv2.flip(frame, 1)
    cframe = frame.copy()
    cframe = cv2.cvtColor(cframe,cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(cframe,cv2.HOUGH_GRADIENT,dp=5,minDist=200,param1=300,param2=200,minRadius=50,maxRadius=70)

    mask = cframe.copy()
    mask = np.zeros(cframe.shape[:2],dtype="uint8")

    if circles is not None:
        raio = []
        circles = np.uint16(np.around(circles))
        for i in circles[0,:2]:
            cv2.circle(mask,(i[0],i[1]),i[2],(255,255,255),-1)
            cv2.circle(frame,(i[0],i[1]),i[2],(20, 176, 18),5)
        frame = calculo(mask, frame).copy()

    cv2.imshow("preview", frame)
    
    
    rval, frame = vc.read()
    key = cv2.waitKey(32)
    if key == 32:
        break

vc.release()
cv2.destroyWindow("preview")