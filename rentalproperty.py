# -*- coding: utf-8 -*-
"""
Created on Sun May 15 20:09:28 2022

@author: mikke
"""

import matplotlib.pyplot as plt

class RentalProperty:
    def __init__(self):
        # set by the user
        self.prop_taxes = float('NaN')
        self.purchase_price = float('NaN')
        self.property_value = float('NaN')
        self.closing_costs = float('NaN')
        self.repair_costs = float('NaN')
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
        self.net_operating_income = float('NaN')
        self.monthly_expenses = float('NaN')

        
    # The user should set loan amount, interest rate, and amortization period before this gets called
    def calculate_mortgage_payment(self):
        self.loan_amount = self.purchase_price-self.down_payment
        self.mortgage_payment = self.loan_amount*(self.interest_rate/100/12)*(1+self.interest_rate/100/12)**(self.amortization_period*12)/ \
                                             ((1+self.interest_rate/100/12)**(self.amortization_period*12)-1)
    
    def calculate_cashflow(self):
        self.monthly_expenses = self.fixed_landlord_expenses+self.variable_landlord_expenses+self.mortgage_payment
        self.monthly_cashflow = self.gross_monthly_income-self.monthly_expenses
        self.fifty_perc_cashflow = 0.5*self.gross_monthly_income-self.mortgage_payment
        self.net_operating_income = 12*(self.gross_monthly_income-(self.monthly_expenses-self.mortgage_payment))
        
    def plot_income(self):
        loan_length = self.amortization_period
        self.annual_cashflow = [float('NaN')]*(loan_length+2)
        gross_income = ['NaN']*(loan_length+2)
        operating_expenses = ['NaN']*(loan_length+2)
        mortgage_payment = ['NaN']*(loan_length+2)
        total_expenses = ['NaN']*(loan_length+2)
        NOI = ['NaN']*(loan_length+2) # net operating income
        for year in range(loan_length+2):
            if year==0:
                gross_income[year] = 0
                operating_expenses[year] = 0
                mortgage_payment[year] = 0
            else:
                gross_income[year] = self.gross_monthly_income*12*(1+self.annual_percent_rent_increase/100)**(year-1)
                operating_expenses[year] = (self.fixed_landlord_expenses+self.variable_landlord_expenses)*12*(1+self.annual_percent_expense_increase/100)**(year-1)
                if (year <= loan_length):
                    mortgage_payment[year] = self.mortgage_payment*12
                else:
                    mortgage_payment[year] = 0
            total_expenses[year] = operating_expenses[year]+mortgage_payment[year]
            self.annual_cashflow[year] = gross_income[year]-total_expenses[year]
            NOI[year] = gross_income[year]-operating_expenses[year]
            
        # plot stuff
        fig, ax = plt.subplots(1,1)
        ax.plot([year for year in range(loan_length+2)],[i/1000 for i in gross_income], label = 'Gross Income')
        ax.plot([year for year in range(loan_length+2)],[i/1000 for i in total_expenses], label = 'Total Expenses')
        ax.plot([year for year in range(loan_length+2)],[i/1000 for i in self.annual_cashflow], label = 'Cashflow')
        ax.plot([year for year in range(loan_length+2)],[i/1000 for i in NOI], label = 'Net Operating Income')
        
        # format ytick labels
        labels = [item.get_text() for item in ax.get_yticklabels()]
        labels = ['$'+label+'k' for label in labels]
        ax.set_yticks(ax.get_yticks().tolist()) # this line is unnecessary but prevents a warning
        ax.set_yticklabels(labels)
        
        ax.legend()
        plt.xlabel('Years Since Purchase')
        ax.grid()
        
    def plot_equity(self):
        loan_length = self.amortization_period
        property_value = ['NaN']*(loan_length+2)
        loan_balance = ['NaN']*(loan_length+2)
        equity = ['NaN']*(loan_length+2)
        total_rental_profit = ['NaN']*(loan_length+2)
        total_profit = ['NaN']*(loan_length+2)
        for year in range(loan_length+2):
            property_value[year] = self.property_value*(1+self.annual_percent_appreciation/100)**(year)
            # same as property_value[year] = property_value[year-1]*(1+self.annual_percent_appreciation/100)
            
            loan_balance[year] = max(0,self.loan_amount*(((1+self.interest_rate/100/12)**(loan_length*12))-
                                                                  ((1+self.interest_rate/100/12)**(year*12)))/
                                                                 (((1+self.interest_rate/100/12)**(loan_length*12))-1))
            equity[year] = property_value[year]-loan_balance[year]
            if (year == 0):
                total_rental_profit[year] = 0
            else:
                total_rental_profit[year] = total_rental_profit[year-1]+self.annual_cashflow[year]

            total_profit[year] = total_rental_profit[year]+(property_value[year]-(self.purchase_price+self.closing_costs+self.repair_costs))
        
        # plot stuff
        fig, ax = plt.subplots(1,1)
        ax.plot([year for year in range(loan_length+2)],[i/1000 for i in property_value], label = 'Property Value')
        ax.plot([year for year in range(loan_length+2)],[i/1000 for i in loan_balance], label = 'Loan Balance')
        ax.plot([year for year in range(loan_length+2)],[i/1000 for i in equity], label = 'Equity')
        ax.plot([year for year in range(loan_length+2)],[i/1000 for i in total_rental_profit], label = 'Total Rental Profit')
        ax.plot([year for year in range(loan_length+2)],[i/1000 for i in total_profit], label = 'Total Profit')
        
        # format ytick labels
        labels = [item.get_text() for item in ax.get_yticklabels()]
        labels = ['$'+label+'k' for label in labels]
        ax.set_yticks(ax.get_yticks().tolist()) # this line is unnecessary but prevents a warning
        ax.set_yticklabels(labels)
        
        ax.legend()
        plt.xlabel('Years Since Purchase')
        ax.grid()