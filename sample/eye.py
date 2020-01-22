import sys
import time
import os.path
from PIL import Image, ImageSequence
from luma.core.sprite_system import framerate_regulator
from luma.core.interface.serial import spi
from luma.lcd.device import st7735

def main():
    regulator = framerate_regulator(fps=10)
    img_path = os.path.abspath(os.path.join(os.path.dirname(__file__),
        'images','eye_wink_ffast.gif'))
    eye_w = Image.open(img_path)

    size = [min(*L_eye.size)] * 2
    posn = ((L_eye.width - size[0]) // 2, L_eye.height - size[1])

    leye=[]
    reye=[]

    start=time.time()
    for frame in ImageSequence.Iterator(eye_w):
        with regulator:
            l_eye = Image.new("RGB", L_eye.size, "white")
            l_eye.paste(frame.resize(size, resample=Image.LANCZOS), posn)
	    leye.append(l_eye)
            r_eye = Image.new("RGB", R_eye.size, "white")
            r_eye.paste(frame.resize(size, resample=Image.LANCZOS), posn)
	    reye.append(r_eye)
    l=len(leye)
    print time.time()-start

    while True:
        start=time.time()
        print "wink"
        for i in range(l):
	    L_eye.display(leye[i])
	    R_eye.display(reye[i])
	    print i
	    time.sleep(0.045)
        print time.time()-start
        time.sleep(1)

if __name__ == "__main__":
    try:
        L_eye = st7735(spi(port=0, device=0, gpio_RST=24, gpio_DC=25, bus_speed_hz=32000000), bgr=True, width=128, rotate=3, h_offset=1, v_offset=2)
        L_eye.command(0x21)
        R_eye = st7735(spi(port=0, device=1, gpio_RST=6, gpio_DC=12, bus_speed_hz=32000000), bgr=True, width=128, rotate=3, h_offset=1, v_offset=2)
        R_eye.command(0x21)
	main()
    except KeyboardInterrupt:
        pass