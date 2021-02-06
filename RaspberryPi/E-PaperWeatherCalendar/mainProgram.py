# -*- coding: utf-8 -*-
"""
Created on Fri Jan 15 22:01:45 2021

@author: Fred Hu
"""

#import libraries
from lib.waveshare_epd import epd4in2
from PIL import Image,ImageDraw,ImageFont
from utils import getMonthX,getCurrentTime,getWeather
from poems import getRandomPoem, getPoemX
import time 

#global variables
global epd, blackFont20, normalFont20, normalFont24, blackFont30, blackFont80

#initialize the epd and fonts
def init():
    try:
        global epd, blackFont20, normalFont20, normalFont24, blackFont30, blackFont80
        epd = epd4in2.EPD()
        epd.init()
        epd.Clear()
        blackFont20 = ImageFont.truetype('/home/pi/waveshare/E-PaperWeatherCalendar/resources/fonts/GeHei.otf', 20)
        normalFont20 = ImageFont.truetype('/home/pi/waveshare/E-PaperWeatherCalendar/resources/fonts/Font.ttc', 20)
        normalFont24 = ImageFont.truetype('/home/pi/waveshare/E-PaperWeatherCalendar/resources/fonts/Font.ttc', 24)
        blackFont30 = ImageFont.truetype('/home/pi/waveshare/E-PaperWeatherCalendar/resources/fonts/GeHei.otf', 30)
        blackFont80 = ImageFont.truetype('/home/pi/waveshare/E-PaperWeatherCalendar/resources/fonts/GeHei.otf', 80)
    except Exception as e:
        print(e)
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd4in2.epdconfig.module_exit()
        exit()
        
#update the information of weather, date and location.
#refresh the information on the screen
def Refresh():
    try:
        #get current time
        dateStr, weekStr, dayStr, monthStr = getCurrentTime()
        #get information of weather
        city, temp, icon, text, tempMin, tempMax = getWeather()
        #initialize the image
        im = Image.new('1', (epd.width, epd.height), 255)
        draw = ImageDraw.Draw(im)
        draw.text((30, 10), dateStr, font = blackFont20, fill = 0)
        draw.text((30, 45), weekStr, font = blackFont20, fill = 0)
        draw.text((30, 80), city, font = normalFont20, fill = 0)
        bmp = Image.open("/home/pi/waveshare/E-PaperWeatherCalendar/resources/pictures/" + icon + ".bmp")
        im.paste(bmp,(30,115))
        draw.text((30, 190), text, font = normalFont20, fill = 0)
        draw.text((30, 225), temp + "°C", font = blackFont20, fill = 0)
        draw.text((30, 260), tempMin + "°C -" + tempMax + "°C", font = blackFont20, fill = 0)
        draw.text((226, 30), dayStr, font = blackFont80, fill = 0)
        draw.text((getMonthX(monthStr),130), monthStr, font = blackFont30, fill = 0)
        poemFirst, poemSecond = getRandomPoem()
        poemX = getPoemX(len(poemFirst))
        draw.text((poemX,200),poemFirst,font = normalFont24, fill = 0)
        draw.text((poemX,240),poemSecond,font = normalFont24, fill = 0)
        epd.display(epd.getbuffer(im))
    except Exception as e:
        print(e)
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd4in2.epdconfig.module_exit()
        exit()

if __name__ == '__main__':
    try:
        time.sleep(30)
        init()
        Refresh()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:    
        print("ctrl + c:")
        epd4in2.epdconfig.module_exit()
        exit()
    