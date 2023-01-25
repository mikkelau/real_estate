# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 19:47:16 2023

@author: mikke
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from RentalProperty import RentalProperty
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

def webscraper_utahrealestate(zipcode):
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
    
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'criteria-wrap')))
    results = wait.until(EC.presence_of_element_located((By.ID,'results-listings')))
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,'property___details')))
    listings = results.find_elements(By.CLASS_NAME,'property___details')
    prop_lst = [RentalProperty() for _ in range(len(listings))] # '_' indicates that the variable is not important
    
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

                        
    # click off of all symbols
    browser.find_element(By.ID, 'jquery_ui_map_div').click()
    
    return prop_lst