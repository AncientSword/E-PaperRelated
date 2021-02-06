# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 22:41:40 2021

@author: Fred Hu
"""
#import libraries
from lib.waveshare_epd import epd4in2
from PIL import Image
import time
import os
global epd, imageList
#initialize the epd
def init():
    try:
        global epd, imageList
        imageList = os.listdir("/home/pi/waveshare/E-PaperDigitalAlbum/resources/pictures/")
        epd = epd4in2.EPD()
        epd.init()
        epd.Clear()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd4in2.epdconfig.module_exit()
        exit()

#show the image on the screen
def showImage(fileName):
    try:
        im = Image.new('1', (epd.width, epd.height), 255)
        bg = Image.open("/home/pi/waveshare/E-PaperDigitalAlbum/resources/pictures/" + fileName)
        bg = bg.convert(mode = "1", dither = Image.FLOYDSTEINBERG)
        im.paste(bg,(20,15))
        epd.display(epd.getbuffer(im))
        
    except Exception as e:
        print(e)
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd4in2.epdconfig.module_exit()
        exit()

if __name__ == '__main__':
    try:
        init()
        for image in imageList:
            showImage(image)
            time.sleep(12)
        epd.Clear()
        epd.sleep()
        time.sleep(3)
        epd.Dev_exit()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd4in2.epdconfig.module_exit()
        exit()
    