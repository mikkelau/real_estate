# -*- coding: utf-8 -*-
"""
Created on Thu May  5 17:51:19 2022

@author: mikke
"""

import webscrapers as ws

zipcode = '84044'

# call the utahrealestate webscraper.
# creates a list of objects of type RentalProperty and fill in:
# days_on_URE, listing_price, num_beds, sqr_feet, num_baths, MLS_ID
prop_lst = ws.utah_re(zipcode)

# call the fair market rent webscraper.
# creates a dictionary with the following keys: 'Studio', '1-Bedroom', 
# '2-Bedroom', '3_Bedroom', '4-Bedroom', and possibly higher if needed
rental_prices = ws.fmr(zipcode)

# evaluate all current deals to see if anything cashflows        
for property in prop_lst:
    property.down_payment = 30000
    property.purchase_price = property.listing_price
    property.interest_rate = 5.5
    property.amortization_period = 30
    property.fixed_landlord_expenses = 300
    property.calculate_mortgage_payment()
    # populate gross_monthly_income using rent pricing
    for k in rental_prices:
        if property.num_beds in k:
            property.gross_monthly_income = rental_prices[k]
            break # break out of the inner for loop
    if not property.gross_monthly_income:
        print(f'Could not calculate rent for MLS# {property.MLS_ID}!')
        # need to calculate for higher number of bedrooms
    property.calculate_cashflow()
    property.fifty_perc_cashflow
    if property.monthly_cashflow > 0:
        print(f'MLS #{property.MLS_ID} projected to cashflow {property.monthly_cashflow} per month.\n'+
        f'By the 50% rule, it is projected to cashflow {property.fifty_perc_cashflow} per month.\n')

# FURHTER IDEAS
# Display properties that ahve been on the market for the longest (might be more open to a low bid)
# Make into an app where down payment, interest rate, amortization, and monthly expenses can be added separately
# Display more property info on properties that are projected to cash flow
# Display properties by price per square foot
            
            
