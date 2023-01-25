# -*- coding: utf-8 -*-
"""
Created on Sun May 15 20:09:28 2022

@author: mikke
"""

class RentalProperty:
    def __init__(self):
        # set by the user
        self.prop_taxes = float('NaN')
        self.purchase_price = float('NaN')
        self.closing_costs = float('NaN')
        self.down_payment = float('NaN')
        self.interest_rate = float('NaN') # this should be in percent (i.e. 3.5 means 3.5% interest)
        self.amortization_period = float('NaN')
        self.gross_monthly_income = float('NaN')
        self.fixed_landlord_expenses = 0
        self.variable_landlord_expenses = 0 # This is to account for things like vacancy, capX, property management fees, maintenance, etc.
        self.annual_percent_rent_increase = float('NaN')
        self.annual_percent_expense_increase = float('NaN')
        self.annual_percent_appreciation = float('NaN')
        self.num_beds = float('NaN')
        self.num_baths = float('NaN')
        self.sqr_feet = float('NaN')
        self.listing_price = float('NaN')
        self.days_on_URE = float('NaN')
        self.MLS_ID = float('NaN')
        
        # determined by the app
        self.loan_amount = float('NaN')
        self.mortgage_payment = float('NaN')
        self.monthly_cashflow = float('NaN')
        self.fifty_perc_cashflow = float('NaN')
        
    # The user should set loan amount, interest rate, and amortization period before this gets called
    def calculate_mortgage_payment(self):
        self.loan_amount = self.purchase_price-self.down_payment
        self.mortgage_payment = self.loan_amount*(self.interest_rate/100/12)*(1+self.interest_rate/100/12)**(self.amortization_period*12)/ \
                                             ((1+self.interest_rate/100/12)**(self.amortization_period*12)-1)
    
    def calculate_cashflow(self):
        self.monthly_cashflow = self.gross_monthly_income-(self.fixed_landlord_expenses+self.variable_landlord_expenses+self.mortgage_payment)
        self.fifty_perc_cashflow = 0.5*self.gross_monthly_income-self.mortgage_payment