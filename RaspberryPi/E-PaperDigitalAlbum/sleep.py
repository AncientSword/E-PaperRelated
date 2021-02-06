# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 19:04:03 2021

@author: ASUS
"""

from lib.waveshare_epd import epd4in2
import time


epd = epd4in2.EPD()
epd.init()
epd.Clear()
epd.sleep()
time.sleep(3)
epd.Dev_exit()