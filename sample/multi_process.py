import time
import random
import sys
import os.path
import multiprocessing as mp
from glob import glob

import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from PIL import Image, ImageSequence, GifImagePlugin

def img_prepare(img='eyes_v2.gif', lcd_size=[128,128]):

    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images',img))
    eye = Image.open(img_path)
    eye_list=[]
    for frame in ImageSequence.Iterator(eye):
            background = Image.new("RGB", lcd_size, "white")
            background.paste(frame.resize(lcd_size, resample=Image.LANCZOS), [0,0])
            eye_list.append(background)
    return eye_list,len(eye_list)

def start(device):
    device.begin()
    eye,l=img_prepare(lcd_size=device.size)
    while True:
        for i in range(0,l):
            barrier.wait()
            time.sleep(1/45)
            device.display(eye[i])
        
if __name__ == "__main__":
    try:
        L_eye=TFT.ST7735(rst=24,dc=25,x_offset=2, y_offset=3, rotate=180, spi=SPI.SpiDev(port=0,device=0,max_speed_hz=64*1000000))
        R_eye=TFT.ST7735(rst=6 ,dc=12,x_offset=2, y_offset=3, rotate=180, spi=SPI.SpiDev(port=0,device=1,max_speed_hz=64*1000000))

        barrier = mp.Barrier(2, timeout=2)

        left=mp.Process(target=start, args=(L_eye,))
        right=mp.Process(target=start, args=(R_eye,))
        left.start()
        right.start()
        
    except KeyboardInterrupt:
        pass
