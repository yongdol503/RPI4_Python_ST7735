import os.path
import sys
import urllib.request
from PIL import Image
from luma.core.interface.serial import spi
from luma.lcd.device import st7735

def downImage(img_url, img_name):
    dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'images'))
    urllib.request.urlretrieve(img_url, dir+'/'+img_name)

def main():
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
            'images', 'qr_code.png'))

    logo = Image.open(img_path).convert("RGB")
    logo = logo.resize(device.size, resample = Image.LANCZOS)
    background = Image.new("RGB", device.size, "white")
    posn = ((device.width - logo.width) // 2, (device.height - logo.height) // 2)
    background.paste(logo, posn)

    while True:
        device.display(background)


if __name__ == "__main__":
    try:
        device = st7735(spi(port=0, device=0, gpio_RST=24, gpio_DC=25, bus_speed_hz=32000000), bgr=True, width=128, rotate=3, h_offset=1, v_offset=2)
        device.command(0x21)
        try:
            main()
        except:
            downImage(sys.argv[1],'qr_code.png')  #sample url : https://live.staticflickr.com/8236/8497781378_f33da2504f_z.jpg
            main()
    except KeyboardInterrupt:
        pass
