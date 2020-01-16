import os.path
import time
from PIL import Image, ImageSequence
import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

def main():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'banana.gif'))
    banana = Image.open(img_path)
    size = [min(*device.size)] * 2
    posn = ((device.width - size[0]) // 2, device.height - size[1])

    while True:
        for frame in ImageSequence.Iterator(banana):
            background = Image.new("RGB", device.size, "white")
            background.paste(frame.resize(size, resample=Image.LANCZOS), posn)
            device.display(background.convert(device.mode))
            time.sleep(1/10)

if __name__ == "__main__":
    try:
        device=TFT.ST7735(rst=24, dc=25, rotate=180, spi=SPI.SpiDev(port=0,device=0,max_speed_hz=64*1000000))
        device.begin()
        main()
    except KeyboardInterrupt:
        pass
