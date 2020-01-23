import time
import random
import sys
import os.path
import threading
from glob import glob
from PIL import Image, ImageSequence, GifImagePlugin
from luma.core.sprite_system import framerate_regulator
from luma.core.interface.serial import spi
from luma.lcd.device import st7735

def img_prepare(img, lcd_size=[128,128]):
    regulator = framerate_regulator(fps=1000)
    
    img_path = os.path.abspath(os.path.join(os.path.dirname('two_spi.py'),'images',img))
   
    eye = Image.open(img_path)
    eye_list=[]
    for frame in ImageSequence.Iterator(eye):
        with regulator:
            background = Image.new("RGB", lcd_size, "white")
            background.paste(frame.resize(lcd_size, resample=Image.LANCZOS), [0,0])
            eye_list.append(background)
    return eye_list,len(eye_list)

def start_l(img='eye_wink.gif'):
    leye,l=img_prepare(img, L_eye.size)
    while True:
        #start=time.time()
        for i in range(0,l):
            #barrier.wait()
            time.sleep(1/45)
            L_eye.display(leye[i])
        #print(rate,". L time:",time.time()-start)
        time.sleep(random.uniform(0,1))

def start_r(img='eye_wink.gif'):
    reye,l=img_prepare(img, R_eye.size)
    while True:
        #start=time.time()
        for i in range(0,l):
            #barrier.wait()
            time.sleep(1/45)
            R_eye.display(reye[i])
        #print(rate,". R time:",time.time()-start)
        time.sleep(random.uniform(0,1))


if __name__ == "__main__":
    try:
        dir=sys.argv[1]
        if dir=='l':
            L_eye = st7735(spi(port=0, device=0, gpio_RST=24, gpio_DC=25, bus_speed_hz=32000000,transfer_size=4096), bgr=True, width=128, rotate=3, h_offset=2, v_offset=2)
            start_l('eyes_v2.gif')
        else:
            R_eye = st7735(spi(port=1, device=2, gpio_RST= 6, gpio_DC=12, bus_speed_hz=32000000,transfer_size=4096), bgr=True, width=128, rotate=3, h_offset=2, v_offset=2)
            start_r('eyes_v2.gif')

        """
        barrier = threading.Barrier(2, timeout=3)
        try:
            left=threading.Thread(target=start_l,args=(sys.argv[1],))
            right=threading.Thread(target=start_r,args=(sys.argv[1],))
        except:
            left=threading.Thread(target=start_l)
            right=threading.Thread(target=start_r)
        left.start()
        right.start()
        """
    except KeyboardInterrupt:
        pass
