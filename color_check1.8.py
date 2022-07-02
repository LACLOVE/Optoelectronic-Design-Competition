#!/usr/bin/python
# -*- coding: UTF-8 -*-

''' 利用加了偏正片的摄像头识别检测蓝色（红色）灯'''
''' 将目标标记出来 '''
''' 自动识别串口 '''
''' 增加辅助测试十字架和最小范围圆形区域 '''
''' 用减法除去了白光（R通道二值图减去B通道二值图）'''
''' by 卢宁 2018.5.31 '''

''' 多线程 ''' 
import thread
import time

#串口通信配置串口号和波特率 
import serial
import serial.tools.list_ports

''' 已知串口号 '''
#port = "COM5"
#baudrate = 115200
#arduino = serial.Serial(port,baudrate)

''' 自动识别串口号 '''
port_list = list(serial.tools.list_ports.comports())
 
if len(port_list) <= 0:
    print "The Serial port can't find!"
     
else:
    port_list_0 =list(port_list[0])
 
    port_serial = port_list_0[0]
 
    arduino = serial.Serial(port_serial,9600,timeout = 0.0001)
 
    print "check which port was really used >",arduino.name

''' 添加opencv库 '''
import numpy as np
import cv2

X=0
Y=0

# 为线程定义一个函数
def image_processing():
    cap = cv2.VideoCapture(0)
    cap.set(cv2.cv.CV_CAP_PROP_FPS, 30) #设定帧率

    global X #全局变量X坐标
    global Y #全局变量Y坐标

    
    while True:
        X=0
        Y=0
        ret, img = cap.read()
        #cv2.imshow("原图", img)
        #定义结构元素
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))  #开运算，闭运算程度设置


                     
        #使用 OpenCV 的 Split 函数，对它进行分离通道的操作，把它分别变成三张单通道的图片
        B, G, R = cv2.split(img)

        #cv2.imshow("R", R)  #红色目标通道
        #cv2.imshow("G", G)
        #cv2.imshow("B", B)  #蓝色目标通道

        th, dst = cv2.threshold(R, 200, 255, cv2.THRESH_BINARY);#二值图_未能解决滤掉白色灯光部分
        th, dst1 = cv2.threshold(B, 200, 255, cv2.THRESH_BINARY);

        dst2=cv2.subtract(dst,dst1) 
        
        blur = cv2.GaussianBlur(dst2,(5,5),0)

        cv2.imshow("lalala", blur)

        # 闭运算，远距离目标也检测到，不能除去小的噪点
        closed = cv2.morphologyEx(blur,cv2.MORPH_CLOSE,kernel)
        #cv2.imshow("Close",closed)

        # 开运算，能除去小的噪点，但是远距离目标就检测不到了，还不知道怎么使用开操作
        opened = cv2.morphologyEx(closed,cv2.MORPH_OPEN,kernel)
        #cv2.imshow("Open",opened)

               
        global contours
        edges = cv2.Canny(opened,400,800) #对开操作进行轮廓检测
        drawing = np.zeros(img.shape,np.uint8)     # Image to draw the contours
        contours,hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            rect = cv2.minAreaRect(cnt)             # 得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
            points = cv2.cv.BoxPoints(rect)         # Find four vertices of rectangle from above rect
            points = np.int0(np.around(points))     # Round the values and make it integers
                         
            color = np.random.randint(0,255,(3)).tolist()  # Select a random color
            #cv2.drawContours(img,[cnt],0,color,1)#轮廓
            #cv2.polylines(img,[points],True,(0,255,0),10)# 矩形拟合


            #十字架&最小圆形区域
            cv2.line(img,(320,0),(320,480),(255,255,0),2)
            cv2.line(img,(0,240),(640,240),(255,255,0),2)
            cv2.circle(img,(320,240), 40, (0,0,255), 1)

            x0,y0,w0,h0 = cv2.boundingRect(contours[0])
            X=x0+w0/2
            Y=y0+h0/2
            #print(X,Y)

            cv2.rectangle(img,(x0,y0),(x0+w0,y0+h0),(255,120,0),3)
            white = (0,0,0)#设置白色变量
            cv2.circle(img,(X,Y),5,white)#circle(图像，圆心，半径，颜色)


        #cv2.imshow("lalala", drawing)
        cv2.imshow('input',img)
        #cv2.imwrite('contours.png', img)
     
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

#为线程定义一个函数,发送目标X,Y坐标
def serial():
     while True:
        #arduino.write("255")
        x = str(X)
        #print(x)
        #arduino.write(b)          # 数据开始传送的标识字节
        arduino.write(x)          # 通过串行连接发送X坐标
        time.sleep(0.02)               # 等待响应
        while arduino.inWaiting()>0 : # 如果有响应等待...
            print arduino.readline()  # 然后打印它
# 创建两个线程
try:
   thread.start_new_thread( image_processing,() )
   thread.start_new_thread( serial,() )
except:
   print "Error: unable to start thread"
 
while 1:
   pass
