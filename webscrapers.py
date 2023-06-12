# -*- coding: utf-8 -*-
"""
Created on Wed Jan 25 12:12:56 2023

@author: mikke
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from rentalproperty import RentalProperty
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def utah_re(zipcode):
    chrome_options = Options()
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    url = 'https://www.utahrealestate.com/search/map.search'
    
    # define bath to the driver for your browser
    driver_service = ChromeDriverManager().install() # this updates it with the current driver every time
    browser = webdriver.Chrome(service=Service(driver_service),options=chrome_options)
    browser.get(url)

    wait = WebDriverWait(browser,10).until(EC.presence_of_element_located((By.ID,'geolocation')))
    location = browser.find_element(By.ID,'geolocation')
    location.send_keys(zipcode)
    location.send_keys(Keys.RETURN)
    
    wait = WebDriverWait(browser,10) # this might not be needed
    
    prop_lst = []
    
    # while there exists a "Next" button
    next_button = True
    while next_button:
    
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,'criteria-wrap')))
        results = wait.until(EC.presence_of_element_located((By.ID,'results-listings')))
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,'property___details')))
        listings = results.find_elements(By.CLASS_NAME,'property___details')
        for item in range(len(listings)):
            prop_lst.append(RentalProperty())
    
        # cycle through all points on the map and get beds, bath, sq feet, and listing price
        for listing in range(len(listings)):
            # print(listing.text)
            lines = listings[listing].text.split('\n')
            for line in lines:
                # figure out days on market
                if 'URE:' in line:
                    URE_line = line.split(':')
                    if 'Just' in URE_line[1]:
                        prop_lst[listing].days_on_URE = 0
                    else:
                        prop_lst[listing].days_on_URE = int(URE_line[1])
                # figure out listing price
                if '•' in line: # should this be an elif?
                    details_line = line.split('•')
                    for item in details_line:
                        if '$' in item:
                            price_part = item.split()
                            for piece in price_part:
                                if '$' in piece:
                                    price = piece.strip('$') # get rid of dollar sign
                                    price = price.replace(',','') # get rid of commas
                                    prop_lst[listing].listing_price = int(price)
                            # figure out number of bedrooms
                            prop_lst[listing].num_beds = price_part[1]
                        # figure out square footage
                        if 'SqFt.' in item: # should this be an elif?
                            square_feet_part = item.split()
                            prop_lst[listing].sqr_feet = int(square_feet_part[0])
                        # figure out number of bathrooms
                        if 'ba' in item:
                            baths_part = item.split()
                            prop_lst[listing].num_baths = int(baths_part[0]) # can this be a decimal? (e.g. 2.5 baths)
                if 'MLS#' in line:
                    MLS_part = line.split()
                    prop_lst[listing].MLS_ID = MLS_part[1] # can't think of a reason this has to be an int, keep as string for now
                    
        # figure out if there's a next button
        next_button = browser.find_elements(By.CSS_SELECTOR,'#paginator-wrap > ul > li:nth-child(2) > a')
        if len(next_button) > 0:
            # see if the cookie banner is in the way and click it if so
            close_banner = browser.find_element(By.CLASS_NAME,'cookie-close')
            if close_banner:
                close_banner.click()
                WebDriverWait(browser,1)
                browser.switch_to.active_element # need to switch back to the active page
            next_button[0].click()

                        
    # click off of all symbols
    browser.find_element(By.ID, 'jquery_ui_map_div').click()
    
    return prop_lst

def fmr(zipcode):
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