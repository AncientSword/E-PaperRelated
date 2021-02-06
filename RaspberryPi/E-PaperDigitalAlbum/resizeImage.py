# -*- coding: utf-8 -*-
"""
Created on Wed Jan 20 22:50:40 2021

@author: Fred Hu
"""
#import libraries
from PIL import Image
import os

#resize the image
def resizeImage(fileName):
    try:
        im = Image.open("resources/pictures/" + fileName)
        im = im.resize((360,270))
        im.show()
        im.save("resources/pictures/" + fileName)
        
    except Exception as e:
        print(e)

if __name__ == '__main__':
    for img in os.listdir("./resources/pictures"):
        print(img)
        resizeImage(img)
    