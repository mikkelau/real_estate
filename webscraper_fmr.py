# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 19:57:16 2023

@author: mikke
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def webscraper_fmr(zipcode):
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    FMR_url = 'https://www.rentdata.org/lookup'
    
    # define bath to the driver for your browser
    driver_service = ChromeDriverManager().install() # this updates it with the current driver every time
    
    # open a browser window to find fair market rent for your zipcode
    FMR_browser = webdriver.Chrome(service=Service(driver_service),options=chrome_options)
    FMR_browser.get(FMR_url)
    wait = WebDriverWait(FMR_browser,10).until(EC.presence_of_element_located((By.ID,'zip')))
    location = FMR_browser.find_element(By.ID,'zip')
    location.send_keys(zipcode)
    location.send_keys(Keys.RETURN)
    
    # read and store the table of bedrooms to price
    rental_prices = {}
    # wait = WebDriverWait(FMR_browser, 20).until(EC.presence_of_element_located((By.CLASS_NAME,'text-center'))) # wait till the table is there
    wait = WebDriverWait(FMR_browser, 10).until(EC.presence_of_element_located((By.TAG_NAME,'table'))) # wait till the table is there
    # table = FMR_browser.find_element(By.CLASS_NAME,'text-center') # define the table object
    table = FMR_browser.find_element(By.TAG_NAME,'table') # define the table object
    while (len(rental_prices) < 5): # force it to keep trying till the full table is read
        rows = table.find_elements(By.TAG_NAME,'tr') # identify table rows
        for row in rows:
            if row.text: # only look at rows with text in them
                row_text = row.text
                split_text = row_text.split()
                if 'Studio' in row_text:
                    split_text = row_text.split()
                    for piece in split_text:
                        if '$' in piece:
                            rental_prices['Studio'] = int(piece.strip('$'))
                else:
                    rental_prices[split_text[0]] = int(split_text[1].strip('$'))
                
    # close the rental prices browser
    FMR_browser.close()
    
    return rental_prices