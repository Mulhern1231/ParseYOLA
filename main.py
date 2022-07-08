from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

import time
from datetime import datetime
from datetime import date

import requests
import json
from bs4 import BeautifulSoup

import os

import pandas as pd
import xlwings as xw




def init():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=OFF")
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("disable-infobars")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--no-sandbox")

    prefs = {'profile.default_content_setting_values': {'cookies': 0,
                                                        'images': 0,
                                                        'javascript': 0,
                                                        'plugins': 0,
                                                        'popups': 0,
                                                        'geolocation': 0,
                                                        'notifications': 0,
                                                        'auto_select_certificate': 0,
                                                        'fullscreen': 0,
                                                        'mouselock': 0,
                                                        'mixed_script': 0,
                                                        'media_stream': 0,
                                                        'media_stream_mic': 0,
                                                        'media_stream_camera': 0,
                                                        'protocol_handlers': 0,
                                                        'ppapi_broker': 0,
                                                        'automatic_downloads': 0,
                                                        'midi_sysex': 0,
                                                        'push_messaging': 0,
                                                        'ssl_cert_decisions': 0,
                                                        'metro_switch_to_desktop': 0,
                                                        'protected_media_identifier': 0,
                                                        'app_banner': 0,
                                                        'site_engagement': 0,
                                                        'durable_storage': 0
                                                        }}

    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_window_size(534, 1080)
    return driver




def reload(driver):
    try:
        listLinkEnd = []
        driver.get("https://youla.ru/?attributes[sort_field]=date_published")
        time.sleep(5)
        list = driver.find_element(By.XPATH, '//*[@id="app"]/div[1]/div[4]/main/div/div[2]/div/section/div/div[2]/div/div/div[2]')
        height = 1000
        for i in range(500, 10):
            driver.execute_script(f"window.scrollTo(0, {i} );")
        for i in range(1,20):
            res = list.find_elements(By.XPATH, f"div[{i}]")
            for q in res:
                linkList = q.find_elements(By.TAG_NAME, "a")
                for x in linkList:
                    listLinkEnd.append(x.get_attribute('href'))
            height=height+200
            driver.execute_script(f"window.scrollTo(0, {height} );")
        print("list done")
        return listLinkEnd
    except:
        return False
        
def loadPageProduct(driver, url_link):
    driver.get(url_link)
    time.sleep(7)
    driver.execute_script(f"window.scrollTo(0, 200 );")
    
    try:
        rating = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/div[1]/div[5]/ul/li[1]/a/div/div[1]/figure/div[2]/div/div/div/span').text
    except:
        rating = 0
    try:
        dataReg = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/div[1]/div[5]/ul/li[1]/a/div/div[1]/figure/div[2]/p[2]').text.replace("на Юле с ","")
    except:
        dataReg = 0
    try:
        views = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/div[1]/div[4]/ul/li[3]/div/dl/dd[2]').text
    except:
        views = 0
    try:
        for i in driver.find_elements(By.CLASS_NAME, 'sc-gqdxRg'):
            print(i.get_attribute(data-test-action))
    except:
        phone = "-"
    
    linkProduct = driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/div[1]/div[5]/ul/li[1]/a').get_attribute('href'),
    
        
    data = {
        "phone": phone,
        "url": url_link,
        "views": views,
        "price": driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/div[1]/div[2]/ul/li[1]/div/div[1]/span/span').text.replace("\u205f", "").replace(" ₽", ""),
        "name": driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/div[1]/div[2]/ul/li[1]/div/h1').text,
        "date": driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/div[1]/div[4]/ul/li[3]/div/dl/dd[3]').text.replace("Сегодня в ", str(date.today())+" " ),
        "profile_url": driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/div[1]/div[5]/ul/li[1]/a').get_attribute('href'),
        "data-reg": dataReg,
        "rating": rating,
        "rating_cnt": driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/div[1]/div[5]/ul/li[1]/a/div/div[1]/figure/div[2]/div/div/button').text,
        "active": driver.find_element(By.XPATH, '/html/body/div[2]/div[1]/div[4]/main/div/div[2]/div[2]/div[1]/div[5]/ul/li[1]/a/div/div[1]/figure/div[2]/p[1]/span').text.split("(")[1].replace(")", "").split()[0],
        "profile_url":linkProduct,
        "sold": "0",
    }
    
    
    driver.get(str(linkProduct[0]))
    time.sleep(3)
    try:
        listSold = driver.find_elements(By.CLASS_NAME, 'sc-iRpACI')
        for iii in listSold:
            if "Продан" in iii.text:
                if len(iii.text.split()) > 1:
                    data["sold"] = iii.text.split()[1]
    except Exception as err:
        print(err)
    print("\033[32m"+f"{data['name']} - {data['url']}")
    
    list_out = []
    for i in data:
        list_out.append(data[i])
    return list_out

    

    
if __name__ == "__main__":
    driver = init()
    d = {
        "phone": 0,
        "url":   0,
        "views": 0,
        "price": 0,
        "name":  0,
        "date":  0,
        "profile_url": 0,
        "data-reg":    0,
        "rating":      0,
        "rating_cnt":  0,
        "active":      0,
        "profile_url": 0,
        "sold":        0,
    }

    df = pd.DataFrame(data=d, index=[0])
    print(df)
    os.system('cls' if os.name=='nt' else 'clear')
    while True:
        try:
            list = reload(driver)
            if list == False:
                print("ERROR: next request in 60 seconds")
                time.sleep(60)
            else:
                for url in list:
                    try:
                        if ("nedvijimost/" in url) or ("auto/" in url):
                            print("\033[31m"+f"AVTO or NEDVIJIMOST: delete ( {url} )")
                        else:
                            listNewFile = loadPageProduct(driver, url)
                            onInList = False
                            for i in range(len(df)):
                                if df.iloc[i, 1] == listNewFile[1]:
                                    onInList = True
                            if onInList == False:
                                df.loc[len(df)] = listNewFile
                            print(df)
                    except Exception as err:
                        print("\033[31m")
                        print(f"ERROR LOAD PAGE")
                        print(f"- {err}")
                        print(f"- {url}")
                        continue
            print("\033[0m")
            writer = pd.ExcelWriter('output.xlsx')
            df.to_excel(writer)
            writer.save()
        except Exception as err:
            print(err)
            print("ERROR: next request in 60 seconds")
            time.sleep(60)
        finally:
            writer = pd.ExcelWriter('output.xlsx')
            df.to_excel(writer)
            writer.save()
        
        
    
