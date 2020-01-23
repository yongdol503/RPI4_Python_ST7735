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

import os.path #os에서 파일위치를 지정해주는 모듈
import ST7735 as TFT #ST7735드라이버를 사용하기위한 모듈
import Adafruit_GPIO as GPIO #Adafriuit의 SPI 통신을 이용하기 위한 모듈 
import Adafruit_GPIO.SPI as SPI #SPI통신 모듈
from PIL import Image #PIL(Python Image Library) 이미지 처리용 모듈

def main():
    #코드와 같은 경로에 images폴더에 pi_loge.png파일의 절대경로
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'pi_logo.png'))
    #logo에 pi_logo.png파일을 RGBA모드로 열어서 넣음
    logo = Image.open(img_path).convert("RGBA")
    #흰 배경화면을 RGBA모드, 디바이스 크기에 맞춰 생성후 로고를 붙여넣음
    background = Image.new("RGBA", device.size, "white")
    posn = ((device.width - logo.width) // 2, 0)
    background.paste(logo, posn)

    while True:
        #디바이스에 로고를 붙여넣은 배경화면을 디바이스 모드(흑백,컬러 등)에 맞춰 출력
        device.display(background.convert(device.mode))


if __name__ == "__main__":
    try:
        #디바이스 객체를 생성 <자세한 매개변수는 라이브러리 참조>
        #SpiDev(port:spi번호, device: cs번호, max~hz: 통신 클럭)
        #st7735(spi:통신 방법, (rst, dc): 각각 핀번호, rotate: 화면 회전)

        device=TFT.ST7735(rst=24, dc=25, rotate=180,      
            spi=SPI.SpiDev(port=0,device=0,max_speed_hz=64*1000000))
        device.begin()
        main()
    except KeyboardInterrupt:
        pass