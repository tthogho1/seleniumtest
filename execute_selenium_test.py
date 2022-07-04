import io
import json
from re import X
import time
from time import sleep
import FunctionS
import os
import sys
import datetime
from typing import List, Tuple, Optional
from PIL import Image
import selenium.webdriver
from selenium import webdriver

import configparser
config = configparser.ConfigParser()
config.read('setting.ini')

URL=config['DEFAULT']['Url']
INPUTFILE=config['DEFAULT']['InputFile']
SAVEFOLDER=config['DEFAULT']['CaptureFolderName'] + "/"
DRIVEREXE=config['DEFAULT']['Driver']

#start main
print('start,selenium...')

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

openf = open(INPUTFILE, 'r')
json_load = json.load(openf)

url = URL
driver = webdriver.Chrome(resource_path(DRIVEREXE))
driver.get(url)


funcs = FunctionS.Functions()

def setItem(screenInput):
    for item in screenInput:
        print(item)
        func = item["func"]
        name = item["name"]
        value = item["value"]
        funcs.execute_function(func)(name,value)


def captureScreen(intX):
    page_width = driver.execute_script('return document.body.scrollWidth')
    page_height = driver.execute_script('return document.body.scrollHeight')        
    driver.set_window_size(page_width, page_height)

    #ファイル名用に現在時刻の取得
    now = datetime.datetime.now()
    zikan = now.strftime('%Y%m%d_%H%M%S')
    filename = str(intX) + "_" + zikan + ".png"   
    # 
    driver.save_screenshot(SAVEFOLDER + filename)

# not used function
def get_full_screenshot_image(driver, reverse=False, driverss_contains_scrollbar=None):
    # type: (selenium.webdriver.remote.webdriver.WebDriver, bool, Optional[bool]) -> Image.Image
    """
    take full screenshot and get its Pillow instance

    :param driver: Selenium WebDriver
    :param reverse: Paste from bottom direction when combining images. The default is False.
    :param driverss_contains_scrollbar: Set to True if the screenshot taken by WebDriver contains a horizontal scroll bar. Default is determined automatically.
    """
    if driverss_contains_scrollbar is None:
        driverss_contains_scrollbar = isinstance(driver, selenium.webdriver.Chrome)
    # Scroll to the bottom of the page once
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(1)
    scroll_height, document_client_width, document_client_height, inner_width, inner_height = driver.execute_script("return [document.documentElement.scrollHeight, document.documentElement.clientWidth, document.documentElement.clientHeight, window.innerWidth, window.innerHeight]")
    streams_to_be_closed = []   # type: List[io.BytesIO]
    images = [] # type: List[Tuple[Image.Image, int]]
    try:
        loopCnt = 0
        for y_coord in range(0, scroll_height, inner_height):
            driver.execute_script("window.scrollTo(0, arguments[0]);", y_coord)
            stream = io.BytesIO(driver.get_screenshot_as_png())
            streams_to_be_closed.append(stream)
            img = Image.open(stream)

            scroll_offsetYheight,  = driver.execute_script("return [window.pageYOffset]")
            if (y_coord + inner_height > scroll_height):
                scroll_offsetYheight,  = driver.execute_script("return [window.pageYOffset]")
                images.append((img,scroll_offsetYheight))  # Image, y_coord
                break
            else:
                images.append((img, y_coord))  # Image, y_coord
            loopCnt=loopCnt+1
            #images.append((img, min(y_coord, scroll_height - y_coord)))

        img_dst = Image.new(mode='RGBA', size=(int(document_client_width ), int(scroll_height )))

        for img, y_coord in (reversed(images) if reverse else images):
            print(y_coord)
            img_dst.paste(img, (0, int(y_coord)))
        return img_dst
    finally:
        for stream in streams_to_be_closed:
            stream.close()
        for img, y_coord in images:
            img.close()
#########################################################################################
# 
# main loop
#
#########################################################################################

intX=0
while True:
    strX = input('input or 9999 for exit ([x] capture browser)>> ')
    if strX == "9999":
        break
        
    if strX == "r":
        try:
            openf = open(INPUTFILE, 'r')
            json_load = json.load(openf)
        except Exception as err:
            print('Exception ' + strX)
            print(err)
        
        continue
    
    if strX == "x":
        driver.switch_to.window(driver.window_handles[-1])
        img_dst = get_full_screenshot_image(driver,False,True)
        img_dst.show()
        now = datetime.datetime.now()
        zikan = now.strftime('%Y%m%d_%H%M%S')
        filename = str(intX) + "_" + zikan + ".png"   
        img_dst.save(SAVEFOLDER + filename)
        #captureScreen(intX)
        continue
    
    if strX == "l":
        for params in json_load:
            for item in params:
                if item["func"] == "print":
                    print(item["value"])
        
        continue
    
    try:
        intX = int(strX)
        screenInput = json_load[intX]
        print(json_load[intX])

        driver.switch_to.window(driver.window_handles[-1])
        # print(driver.page_source)
        funcs.set_driver(driver)
        setItem(screenInput)
    except Exception as err:
        print('Exception ' + strX )
        print(err)

print('finished')

