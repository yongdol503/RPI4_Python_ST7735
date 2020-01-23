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

import os.path
import time
import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from PIL import Image, ImageSequence

def main():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'banana.gif'))
    banana = Image.open(img_path)
    #device 사이즈에 맞춰 이미지를 바꾸는 작업
    size = [min(*device.size)] * 2
    posn = ((device.width - size[0]) // 2, device.height - size[1])

    while True:
        for frame in ImageSequence.Iterator(banana): #바나나 반복자
            background = Image.new("RGB", device.size, "white")
            #resize(self,size,resample=NEAREST): LANCZOS필터가 효과적 
            background.paste(frame.resize(size, resample=Image.LANCZOS), posn)
            device.display(background.convert(device.mode))
            time.sleep(1/10) #LCD하드웨어 상 추가 delay가 발생하나 약 10fps라고 가정

if __name__ == "__main__":
    try:
        device=TFT.ST7735(rst=24, dc=25, rotate=180, 
             spi=SPI.SpiDev(port=0,device=0,max_speed_hz=64*1000000))
        device.begin()
        main()
    except KeyboardInterrupt:
        pass