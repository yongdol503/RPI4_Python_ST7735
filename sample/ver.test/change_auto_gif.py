import time
import random
import sys
import os.path
import multiprocessing as mp

import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from PIL import Image, ImageSequence

def img_prepare(lcd_size=[128,128]):
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

def center(Lpup,Rpup):
    print("center on")
    i=0
    time.sleep(3)
    while 1:
        i+=1
        Lpup.send(i%7)
        Rpup.send(i%7)
        time.sleep(1)
        barrier2.wait()

def start(device,sup):
    data=img_prepare()
    device.begin()
    time.sleep(1)
    print(data[0][0],data[0][1],data[0][2][0])
    while True:
        n=sup.recv()
        barrier2.wait()
        for i in range(0,data[n][1]):
            barrier1.wait()
            time.sleep(1/45)
            device.display(data[n][2][i])
        time.sleep(0.2)

if __name__ == "__main__":
    try:
        imgl=['eyes_v2_skyblue.gif','eyes_v2_light_brown.gif', 'eyes_v2_brown.gif', 'eyes_v2_indigo.gif', 'eyes_v2.gif', 'eyes_v2_love.gif', 'eyes_v2_blue.gif']

        L_eye=TFT.ST7735(rst=24,dc=25,x_offset=2, y_offset=3, rotate=180, spi=SPI.SpiDev(port=0,device=0,max_speed_hz=64*1000000))
        R_eye=TFT.ST7735(rst=6 ,dc=12,x_offset=2, y_offset=3, rotate=180, spi=SPI.SpiDev(port=0,device=1,max_speed_hz=64*1000000))

        Lpup,Lsup=mp.Pipe()
        Rpup,Rsup=mp.Pipe()

        barrier1=mp.Barrier(2, timeout=2)
        barrier2=mp.Barrier(3, timeout=5)

        left=mp.Process(target=start, args=(L_eye,Lsup))
        right=mp.Process(target=start, args=(R_eye,Rsup))
        #img_prep=mp.Process(target=center, args=(Lpup,Rpup))

        left.start()
        right.start()
        #img_prep.start()

        print("change on")
        while 1:
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
