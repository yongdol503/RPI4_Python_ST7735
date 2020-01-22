import time
import random
import sys
import os.path
import multiprocessing as mp

import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from PIL import Image, ImageSequence

def img_prepare(img='eyes_v2_skyblue.gif', lcd_size=[128,128]):

    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images',img))
    eye = Image.open(img_path)
    eye_list=[]
    for frame in ImageSequence.Iterator(eye):
            background = Image.new("RGB", lcd_size, "white")
            background.paste(frame.resize(lcd_size, resample=Image.LANCZOS), [0,0])
            eye_list.append(background)
    return eye_list,len(eye_list)

def center(Lpup,Rpup):
    print("center")
    i=0
    while 1:
        i+=1
        if i%60<20:
            Lpup.send('eyes_v2_skyblue.gif')
            Rpup.send('eyes_v2_skyblue.gif')
        elif i%60<40:
            Lpup.send('eyes_v2_blue.gif')
            Rpup.send('eyes_v2_blue.gif')
        else:
            Lpup.send('eyes_v2_love.gif')
            Rpup.send('eyes_v2_love.gif')
        time.sleep(0.5)
        barrier2.wait()

def start(device,sup):
    device.begin()
    last=""
    while True:
            data=sup.recv()
            if data is not last:
                eye, l=img_prepare(img=data,lcd_size=device.size)
                last=data
            barrier2.wait()

            for i in range(0,l):
                barrier1.wait()
                time.sleep(1/45)
                device.display(eye[i])

if __name__ == "__main__":
    try:
        L_eye=TFT.ST7735(rst=24,dc=25,x_offset=2, y_offset=3, rotate=180, spi=SPI.SpiDev(port=0,device=0,max_speed_hz=64*1000000))
        R_eye=TFT.ST7735(rst=6 ,dc=12,x_offset=2, y_offset=3, rotate=180, spi=SPI.SpiDev(port=0,device=1,max_speed_hz=64*1000000))

        Lpup,Lsup=mp.Pipe()
        Rpup,Rsup=mp.Pipe()

        barrier1=mp.Barrier(2, timeout=2)
        barrier2=mp.Barrier(3, timeout=5)

        left=mp.Process(target=start, args=(L_eye,Lsup))
        right=mp.Process(target=start, args=(R_eye,Rsup))
        img_prep=mp.Process(target=center, args=(Lpup,Rpup))
        left.start()
        right.start()
        img_prep.start()

    except KeyboardInterrupt:
        pass
