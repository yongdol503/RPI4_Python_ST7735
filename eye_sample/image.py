import os.path
from PIL import Image
import ST7735 as TFT
import Adafruit_GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

def main():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images', 'pi_logo.png'))
    logo = Image.open(img_path).convert("RGBA")

    background = Image.new("RGBA", device.size, "white")
    posn = ((device.width - logo.width) // 2, 0)
    background.paste(logo, posn)

    while True:
        device.display(background.convert(device.mode))


if __name__ == "__main__":
    try:
        device=TFT.ST7735(rst=24, dc=25, rotate=180, spi=SPI.SpiDev(port=0,device=0,max_speed_hz=64*1000000))
        device.begin()
        main()
    except KeyboardInterrupt:
        pass
