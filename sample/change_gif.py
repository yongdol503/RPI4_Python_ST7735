# MIT License

# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
# Improved by the yongdol503

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import random
import sys
import os.path
import threading
import multiprocessing as mp
from queue import Queue #쓰레드간 통신에 사용할 큐, 프로세스간 큐는 mp에 구현되어 있음
import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from PIL import Image, ImageSequence

def img_prepare(lcd_size=[128,128]):  #이미지처리 함수, 빠른 전환을 위해 미리 처리 권장
    global imgl
    data=[]
    for img in imgl:
        img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images',img))
        eye = Image.open(img_path)
        eye_list=[]
        for frame in ImageSequence.Iterator(eye):
            background = Image.new("RGB", lcd_size, "white")
            background.paste(frame.resize(lcd_size, resample=Image.LANCZOS), [0,0])
            eye_list.append(background)
        data.append([img,len(eye_list),eye_list])
    return data

def recive(sup,q):  #메인 프로세스에서 보낸 데이터를 수신하는 쓰레드 함수
    while True:
        n=sup.recv()
        q.put(n)
        print('recive')
        barrier2.wait()

def lcd(device,sup):  #각각 lcd를 제어할 프로세스
    data=img_prepare()
    device.begin()
    q=Queue()
    observer=threading.Thread(target=recive,args=(sup,q))
    observer.start()   #메인에서 전송될 데이터를 관찰하고 전달할 쓰레드, 실시간을 위해 사용
    n=0
    while True:
        if not q.empty():
            print('changing img!')
            n=q.get()
        print("displayed <%s>"%data[n][0])
        for i in range(0,data[n][1],2): #gif 전환속도를 올리고자 2step씩 건너뜀
            barrier1.wait()
            time.sleep(1/45)
            device.display(data[n][2][i])
        time.sleep(2)

if __name__ == "__main__":
    try:
        imgl=['eyes_v2_skyblue.gif','eyes_v2_light_brown.gif', 'eyes_v2_brown.gif', 'eyes_v2_indigo.gif', 'eyes_v2.gif', 'eyes_v2_love.gif', 'eyes_v2_blue.gif']

        L_eye=TFT.ST7735(rst=24,dc=25,x_offset=2, y_offset=3, rotate=180,
            spi=SPI.SpiDev(port=0,device=0,max_speed_hz=64*1000000))
        R_eye=TFT.ST7735(rst=6 ,dc=12,x_offset=2, y_offset=3, rotate=180,
            spi=SPI.SpiDev(port=0,device=1,max_speed_hz=64*1000000))
        #process간 통신을 위한 파이프
        Lpup,Lsup=mp.Pipe()
        Rpup,Rsup=mp.Pipe()

        barrier1=mp.Barrier(2, timeout=2)
        barrier2=mp.Barrier(3, timeout=2)

        left=mp.Process(target=lcd, args=(L_eye,Lsup))
        right=mp.Process(target=lcd, args=(R_eye,Rsup))

        left.start()
        right.start()
        #입력받아 정보를 전달할 메인 프로세스
        print("change fucntion on")
        while True:
            for n,name in enumerate(imgl):
                print(n,name)
            try:
                i=int(input())
            except:
                i=0
            Lpup.send(i%7)
            Rpup.send(i%7)
            barrier2.wait()

    except KeyboardInterrupt:
        pass