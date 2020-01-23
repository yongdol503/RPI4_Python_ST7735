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
import multiprocessing as mp #multiprocessing을 위한 모듈
import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from PIL import Image, ImageSequence
#gif를 img로 쪼개는 함수, 추후 메서드로 추가할 예정 
def img_prepare(img='eyes_v2.gif', lcd_size=[128,128]):
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'images',img))
    eye = Image.open(img_path)
    eye_list=[]
    for frame in ImageSequence.Iterator(eye):
            background = Image.new("RGB", lcd_size, "white")
            background.paste(frame.resize(lcd_size, resample=Image.LANCZOS), [0,0])
            eye_list.append(background)
    return eye_list,len(eye_list)

def start(eye):
    eye.begin()
    eye_img, l=img_prepare(lcd_size=eye.size)
    while True:
        for i in range(0,l):
            barrier.wait() #process간 synchronize를 위해 사용
            time.sleep(1/45)
            eye.display(eye_img[i])
        
if __name__ == "__main__":
    try:
        L_eye=TFT.ST7735(rst=24,dc=25,x_offset=2, y_offset=3, rotate=180, 
            spi=SPI.SpiDev(port=0,device=0,max_speed_hz=64*1000000))
        R_eye=TFT.ST7735(rst=6 ,dc=12,x_offset=2, y_offset=3, rotate=180, 
            spi=SPI.SpiDev(port=0,device=1,max_speed_hz=64*1000000))
        barrier = mp.Barrier(2, timeout=2) #synchronize를 위한 barrier
        left=mp.Process(target=start, args=(L_eye,)) #process 생성
        right=mp.Process(target=start, args=(R_eye,))
        left.start() #process 시작
        right.start()
        
    except KeyboardInterrupt:
        pass