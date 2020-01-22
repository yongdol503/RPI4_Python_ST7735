import os.path
import time
import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
from PIL import Image, ImageDraw, ImageFont, ImageColor

def main():
    color = ImageColor.getrgb('hsl(192, 100%, 84%)')
    base = Image.new('RGBA', device.size, color)
    txt = Image.new('RGBA', base.size, (255,255,255,0))
    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'fonts', 'NanumSquareRoundEB.ttf'))
    fnt = ImageFont.truetype(font_path, device.height-70)
    d = ImageDraw.Draw(txt)
    d.text((10,30), "안녕", font=fnt, fill=(0,0,0,255))
    out = Image.alpha_composite(base, txt)
    device.display(out.convert(device.mode))

if __name__ == '__main__':
    try:
        device=TFT.ST7735(rst=24, dc=25, rotate=180, spi=SPI.SpiDev(port=0,device=0,max_speed_hz=64*1000000))
        device.begin()
        main()
    except KeyboardInterrupt:
        pass
