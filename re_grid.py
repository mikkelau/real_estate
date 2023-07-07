# -*- coding: utf-8 -*-
"""
Created on Fri Jun  9 09:40:49 2023

@author: mikke
"""
from rentalproperty import RentalProperty
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import matplotlib.pyplot as plt
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle

class RE_Grid(GridLayout):
    def __init__(self, **kwargs):
        super(RE_Grid, self).__init__(**kwargs)
        
        # initialize the RentalProperty class instance
        my_property = RentalProperty()
        
        self.cols = 1
        self.spacing = 10
        self.padding = 10
    
        self.inside = GridLayout(cols = 2)
        
        self.inside.add_widget(Label(text='Property Info', font_size=40, bold=True))
        self.inside.add_widget(Label(text='Rental Info', font_size=40, bold=True))
        
        self.inside.add_widget(PropertyInfo(my_property))
        
        self.inside.add_widget(RentalInfoSimple(my_property))

        self.add_widget(self.inside)
        
        self.make_plots = Button(text="Make Plots!", font_size=40, height=100, size_hint=(1,None))
        self.make_plots.bind(on_press = lambda x:self.plot_pressed(self, my_property))
        self.add_widget(self.make_plots)
        
        
    def plot_pressed(self, instance, RentalProperty):
        RentalProperty.plot_income()
        RentalProperty.plot_equity()
        plt.show()
        
        
class Tooltip(Label):
    def __init__(self, **kwargs):
        super(Tooltip, self).__init__(**kwargs)
        
        self.size_hint = (None,None)

        with self.canvas.before:
            Color(0.2, 0.2, 0.2)
            self.rect = Rectangle(size=self.texture_size, pos=self.pos)

        self.bind(pos=self.update_rect)
        self.bind(pos=self.update_size)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.texture_size[0]+5,self.texture_size[1]+5)
        
    def update_size(self, *args):
        self.size = (self.texture_size[0]+5,self.texture_size[1]+5)
    

class MyLabel(Label):
    def __init__(self, **kwargs):
        self.helptext = kwargs.pop('helptext')
        super(MyLabel, self).__init__(**kwargs)
                
        Window.bind(mouse_pos=self.on_mouse_pos)
        
        self.tooltip = Tooltip(text=self.helptext)

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return # not sure what this accomplishes
        pos = args[1]
        self.tooltip.pos = pos
        Clock.unschedule(self.display_tooltip) # cancel scheduled event since I moved the cursor
        self.close_tooltip() # close if it's opened
        if self.collide_point(*self.to_widget(*pos)):
            Clock.schedule_once(self.display_tooltip, 0.5)

    def close_tooltip(self, *args):
        Window.remove_widget(self.tooltip)

    def display_tooltip(self, *args):
        Window.add_widget(self.tooltip)
        
class PropertyInfo(GridLayout):
    def __init__(self, my_property, **kwargs):
        super(PropertyInfo, self).__init__(**kwargs)
        
        self.cols=2
        self.spacing = 10
        self.padding = 10
        left = GridLayout(cols=1)
        right = GridLayout(cols=1, size_hint=(0.25,1))
                
        self.property_taxes_label = MyLabel(helptext='Typically publicly available on county assessor\'s website')
        self.property_taxes_label.text = 'Annual Property Taxes:'
        left.add_widget(self.property_taxes_label)
        self.property_taxes = TextInput(multiline=False,text="{:.2f}".format(1600.00),input_filter='float')
        self.property_taxes.bind(text=lambda instance, x:self.clear_mortgage(self))
        right.add_widget(self.property_taxes)
        
        left.add_widget(Label(text='Purchase Price:'))
        self.purchase_price = TextInput(multiline=False,text=str(300000),input_filter='float')
        self.purchase_price.bind(text=lambda instance, x:self.clear_mortgage(self))
        right.add_widget(self.purchase_price)
        
        self.property_value_label = MyLabel(helptext='Property may be worth more (or less) than what you paid for it')
        self.property_value_label.text = 'Property Value:'
        left.add_widget(self.property_value_label)
        self.property_value = TextInput(multiline=False,text=str(300000),input_filter='float')
        self.property_value.bind(text=lambda instance, x:self.clear_mortgage(self))
        right.add_widget(self.property_value)
        
        self.closing_costs_label = MyLabel(helptext='Typically $1500-$2500')
        self.closing_costs_label.text = 'Closing Costs:'
        left.add_widget(self.closing_costs_label)
        self.closing_costs = TextInput(multiline=False,text=str(2000.00),input_filter='float')
        self.closing_costs.bind(text=lambda instance, x:self.clear_mortgage(self))
        right.add_widget(self.closing_costs)
        
        self.repair_costs_label = MyLabel(helptext='Generally properties need some immediate small repairs before renting')
        self.repair_costs_label.text = 'Estimated Repair Costs:'
        left.add_widget(self.repair_costs_label)
        self.repair_costs = TextInput(multiline=False,text=str(2000.00),input_filter='float')
        self.repair_costs.bind(text=lambda instance, x:self.clear_mortgage(self))
        right.add_widget(self.repair_costs)
        
        left.add_widget(Label(text='Down Payment:'))
        self.down_payment = TextInput(multiline=False,text=str(20000),input_filter='float')
        self.down_payment.bind(text=lambda instance, x:self.clear_mortgage(self))
        right.add_widget(self.down_payment)
        
        left.add_widget(Label(text='Interest Rate (%):'))
        self.interest_rate = TextInput(multiline=False,text=str(5.5),input_filter='float')
        self.interest_rate.bind(text=lambda instance, x:self.clear_mortgage(self))
        right.add_widget(self.interest_rate)
        
        left.add_widget(Label(text='Amortization Period (years):'))
        self.amort_period = TextInput(multiline=False,text=str(30),input_filter='float')
        self.amort_period.bind(text=lambda instance, x:self.clear_mortgage(self))
        right.add_widget(self.amort_period)
        
        self.calculate_mortgage = Button(text="Calculate Mortgage")
        self.mortgage_payment = Label()
        self.calculate_mortgage.bind(on_press = lambda x:self.calculate_mortgage_pressed(self, my_property))
        left.add_widget(self.calculate_mortgage)
        right.add_widget(self.mortgage_payment)
        
        self.add_widget(left)
        self.add_widget(right)
    
    def clear_mortgage(self, instance):
        self.mortgage_payment.text = ''
        
    def calculate_mortgage_pressed(self, instance, RentalProperty):
        # set the variables in the class using the text inputs
        RentalProperty.prop_taxes = float(self.property_taxes.text)
        RentalProperty.purchase_price = float(self.purchase_price.text)
        RentalProperty.property_value = float(self.property_value.text)
        RentalProperty.closing_costs = float(self.closing_costs.text)
        RentalProperty.repair_costs = float(self.repair_costs.text)
        RentalProperty.down_payment = float(self.down_payment.text)
        RentalProperty.interest_rate = float(self.interest_rate.text)
        RentalProperty.amortization_period = int(self.amort_period.text)
        
        RentalProperty.calculate_mortgage_payment()
        self.mortgage_payment.text = "${:,.2f}".format(RentalProperty.mortgage_payment)    
        
class RentalInfo(GridLayout):
    def __init__(self, my_property, **kwargs):
        super(RentalInfo, self).__init__(**kwargs)
        
        self.cols=2
        self.spacing = 10
        self.padding = 10
        left = GridLayout(cols=1)
        right = GridLayout(cols=1, size_hint=(0.25,1))
        
        percentage_hint = 0.2
        cost_hint = 0.33
        
        left.add_widget(Label(text='Gross Monthly Rent:'))
        self.gross_rent = TextInput(multiline=False,text=str(2000),input_filter='float')
        self.gross_rent.bind(text=lambda instance, x:self.update_variable_expenses(self))
        right.add_widget(self.gross_rent)
        
        self.monthly_cashflow = Label()
        
        prop_taxes = GridLayout(cols=2)
        self.property_taxes_label = MyLabel(helptext='Previously calculated')
        self.property_taxes_label.text = 'Property Taxes:'
        prop_taxes.add_widget(self.property_taxes_label)
        self.property_taxes_text = Label()
        self.property_taxes_text.size_hint_x = cost_hint
        self.property_taxes_text.bind(text=lambda instance, x:self.update_fixed_expenses(self))
        prop_taxes.add_widget(self.property_taxes_text)
        left.add_widget(prop_taxes)
        right.add_widget(Label())

        services = GridLayout(cols=2)
        self.services_label = MyLabel(helptext='Electricity, Water, Gas, Sewer, Garbage, etc.')
        self.services_label.text = 'Services/Utilities:'
        services.add_widget(self.services_label)
        self.services_expenses = TextInput(multiline=False,text=str(150),input_filter='float')
        self.services_expenses.size_hint_x = cost_hint
        self.services_expenses.bind(text=lambda instance, x:self.update_fixed_expenses(self))
        services.add_widget(self.services_expenses)
        left.add_widget(services)
        right.add_widget(Label())
        
        hoa = GridLayout(cols=2)
        hoa.add_widget(Label(text='HOA:'))
        self.hoa_expenses = TextInput(multiline=False,text=str(0),input_filter='float')
        self.hoa_expenses.size_hint_x = cost_hint
        self.hoa_expenses.bind(text=lambda instance, x:self.update_fixed_expenses(self))
        hoa.add_widget(self.hoa_expenses)
        left.add_widget(hoa)
        right.add_widget(Label())
        
        insurance = GridLayout(cols=2)
        insurance.add_widget(Label(text='Home Owner''s Insurance:'))
        self.home_insurance = TextInput(multiline=False,text=str(100),input_filter='float')
        self.home_insurance.size_hint_x = cost_hint
        self.home_insurance.bind(text=lambda instance, x:self.update_fixed_expenses(self))
        insurance.add_widget(self.home_insurance)
        left.add_widget(insurance)
        right.add_widget(Label())
        
        other = GridLayout(cols=2)
        self.other_expenses_label = MyLabel(helptext='Snow removal, lawn care, flood insurance, etc.')
        self.other_expenses_label.text = 'Other:'
        other.add_widget(self.other_expenses_label)
        self.other_expenses = TextInput(multiline=False,text=str(0),input_filter='float')
        self.other_expenses.size_hint_x = cost_hint
        self.other_expenses.bind(text=lambda instance, x:self.update_fixed_expenses(self))
        other.add_widget(self.other_expenses)
        left.add_widget(other)
        right.add_widget(Label())
        
        self.fixed_expenses_label = MyLabel(helptext='Expenses that are predictable or paid every month')
        self.fixed_expenses_label.text = 'Total Fixed Landlord Expenses:'
        left.add_widget(self.fixed_expenses_label)
        self.total_fixed_expenses = Label()
        right.add_widget(self.total_fixed_expenses)
        
        self.update_fixed_expenses(self)
        
        vacancy = GridLayout(cols=3)
        self.vacancy_label = MyLabel(helptext = 'Typically 3-7% of rental income depending on desirability and location')
        self.vacancy_label.text = 'Vacancy (%)'
        vacancy.add_widget(self.vacancy_label)
        self.vacancy_percentage = TextInput(multiline=False,text=str(5),input_filter='float')
        self.vacancy_percentage.size_hint_x = percentage_hint
        vacancy.add_widget(self.vacancy_percentage)
        self.vacancy_cost_text = Label()
        self.vacancy_cost_text.size_hint_x = cost_hint
        self.vacancy_percentage.bind(text=lambda instance, x:self.update_variable_expenses(self))
        vacancy.add_widget(self.vacancy_cost_text)
        left.add_widget(vacancy)
        right.add_widget(Label())
        
        maintenance = GridLayout(cols=3)
        self.maintenance_label = MyLabel(helptext='Typically 5-10% of rental income depending on age of the unit')
        self.maintenance_label.text = 'Repairs & Maintenance (%)'
        maintenance.add_widget(self.maintenance_label)
        self.maintenance_percentage = TextInput(multiline=False,text=str(7.5),input_filter='float')
        self.maintenance_percentage.size_hint_x = percentage_hint
        maintenance.add_widget(self.maintenance_percentage)
        self.maintenance_cost_text = Label()
        self.maintenance_cost_text.size_hint_x = cost_hint
        self.maintenance_percentage.bind(text=lambda instance, x:self.update_variable_expenses(self))
        maintenance.add_widget(self.maintenance_cost_text)
        left.add_widget(maintenance)
        right.add_widget(Label())
        
        capex = GridLayout(cols=3)
        self.capex_label = MyLabel(helptext='Big expenses that need to be saved up for (windows, roof, appliances, plumbing, etc). Typically 5-10% of rental income.')
        self.capex_label.text = 'Capital Expenditures (%)'
        capex.add_widget(self.capex_label)
        self.capex_percentage = TextInput(multiline=False,text=str(7.5),input_filter='float')
        self.capex_percentage.size_hint_x = percentage_hint
        capex.add_widget(self.capex_percentage)
        self.capex_cost_text = Label()
        self.capex_cost_text.size_hint_x = cost_hint
        self.capex_percentage.bind(text=lambda instance, x:self.update_variable_expenses(self))
        capex.add_widget(self.capex_cost_text)
        left.add_widget(capex)
        right.add_widget(Label())
        
        managementfees = GridLayout(cols=3)
        self.managementfees_label = MyLabel(helptext='Typically 10% of rental income.')
        self.managementfees_label.text = 'Management Fees (%)'
        managementfees.add_widget(self.managementfees_label)
        self.managementfees_percentage = TextInput(multiline=False,text=str(10),input_filter='float')
        self.managementfees_percentage.size_hint_x = percentage_hint
        managementfees.add_widget(self.managementfees_percentage)
        self.managementfees_cost_text = Label()
        self.managementfees_cost_text.size_hint_x = cost_hint
        self.managementfees_percentage.bind(text=lambda instance, x:self.update_variable_expenses(self))
        managementfees.add_widget(self.managementfees_cost_text)
        left.add_widget(managementfees)
        right.add_widget(Label())
        
        self.variable_expenses_label = MyLabel(helptext='Expenses that occur unexpectedly')
        self.variable_expenses_label.text = 'Total Variable Landlord Expenses:'
        left.add_widget(self.variable_expenses_label)
        self.total_variable_expenses = Label()
        right.add_widget(self.total_variable_expenses)
        
        self.update_variable_expenses(self)
        
        left.add_widget(Label(text='Rent Increase per Year (%):'))
        self.yearly_rent_increase = TextInput(multiline=False,text=str(2.0),input_filter='float')
        right.add_widget(self.yearly_rent_increase)
        
        left.add_widget(Label(text='Expense Increase per Year (%):'))
        self.yearly_expense_increase = TextInput(multiline=False,text=str(2.0),input_filter='float')
        right.add_widget(self.yearly_expense_increase)
        
        left.add_widget(Label(text='Property Appreciation per Year (%):'))
        self.yearly_appreciation = TextInput(multiline=False,text=str(2.0),input_filter='float')
        right.add_widget(self.yearly_appreciation)
        
        self.calculate_cashflow = Button(text="Calculate Cashflow")
        self.calculate_cashflow.bind(on_press = lambda x:self.calculate_cashflow_pressed(self, my_property))
        left.add_widget(self.calculate_cashflow)
        right.add_widget(self.monthly_cashflow)
        
        self.add_widget(left)
        self.add_widget(right)
        
    def update_variable_expenses(self, instance):
        if (self.vacancy_percentage.text == '') or (self.gross_rent.text == ''):
            self.vacancy_cost = 0
        else:
            self.vacancy_cost = float(self.gross_rent.text)*float(self.vacancy_percentage.text)/100
        self.vacancy_cost_text.text = "${:,.2f}".format(self.vacancy_cost)
            
        if (self.maintenance_percentage.text == '') or (self.gross_rent.text == ''):
            self.maintenance_cost = 0
        else:
            self.maintenance_cost = float(self.gross_rent.text)*float(self.maintenance_percentage.text)/100
        self.maintenance_cost_text.text = "${:,.2f}".format(self.maintenance_cost)
            
        if (self.capex_percentage.text == '') or (self.gross_rent.text == ''):
            self.capex_cost = 0
        else:
            self.capex_cost = float(self.gross_rent.text)*float(self.capex_percentage.text)/100
        self.capex_cost_text.text = "${:,.2f}".format(self.capex_cost)
            
        if (self.managementfees_percentage.text == '') or (self.gross_rent.text == ''):
            self.managementfees_cost = 0
        else:
            self.managementfees_cost = float(self.gross_rent.text)*float(self.managementfees_percentage.text)/100
        self.managementfees_cost_text.text = "${:,.2f}".format(self.managementfees_cost)
            
        self.total_variable_expenses.text =  "${:,.2f}".format(sum([self.vacancy_cost, self.maintenance_cost,
                                                            self.capex_cost, self.managementfees_cost]))
        self.monthly_cashflow.text = ''
        
    def update_fixed_expenses(self, instance):
        if (self.services_expenses.text == ''):
            self.total_fixed_expenses.text = "${:,.2f}".format(sum([float(self.hoa_expenses.text),float(self.home_insurance.text), 
                                                            self.property_taxes,float(self.other_expenses.text)]))
        elif (self.hoa_expenses.text == ''):
            self.total_fixed_expenses.text = "${:,.2f}".format(sum([float(self.services_expenses.text),float(self.home_insurance.text), 
                                                            self.property_taxes,float(self.other_expenses.text)]))
        elif (self.home_insurance.text == ''):
            self.total_fixed_expenses.text = "${:,.2f}".format(sum([float(self.services_expenses.text),float(self.hoa_expenses.text), 
                                                            self.property_taxes,float(self.other_expenses.text)]))
        elif (self.property_taxes_text.text == ''):
            self.total_fixed_expenses.text = "${:,.2f}".format(sum([float(self.services_expenses.text),float(self.hoa_expenses.text), 
                                                            float(self.home_insurance.text),float(self.other_expenses.text)]))
        elif (self.other_expenses.text == ''):
            self.total_fixed_expenses.text = "${:,.2f}".format(sum([float(self.services_expenses.text),float(self.hoa_expenses.text), 
                                                            float(self.home_insurance.text),self.property_taxes]))
        else:
            self.total_fixed_expenses.text = "${:,.2f}".format(sum([float(self.services_expenses.text), float(self.hoa_expenses.text),
                                                            float(self.home_insurance.text), self.property_taxes, float(self.other_expenses.text)]))
        self.monthly_cashflow.text = ''
        
    def calculate_cashflow_pressed(self, instance, RentalProperty):
        RentalProperty.gross_monthly_income = float(self.gross_rent.text)
        RentalProperty.fixed_landlord_expenses = sum([float(self.services_expenses.text), float(self.hoa_expenses.text),
                                                      float(self.home_insurance.text),self.property_taxes, float(self.other_expenses.text)])
        RentalProperty.variable_landlord_expenses = sum([self.vacancy_cost, self.maintenance_cost, self.capex_cost, self.managementfees_cost])
        RentalProperty.annual_percent_rent_increase = float(self.yearly_rent_increase.text)
        RentalProperty.annual_percent_expense_increase = float(self.yearly_expense_increase.text)
        RentalProperty.annual_percent_appreciation = float(self.yearly_appreciation.text)
        
        RentalProperty.calculate_cashflow()
        self.monthly_cashflow.text = "${:,.2f}".format(RentalProperty.monthly_cashflow)
        self.total_fixed_expenses.text = "${:,.2f}".format(RentalProperty.fixed_landlord_expenses)
        self.total_variable_expenses.text = "${:,.2f}".format(RentalProperty.variable_landlord_expenses)
        
class FinancialSummary(GridLayout):
    def __init__(self, my_property, **kwargs):
        super(FinancialSummary, self).__init__(**kwargs)
        
        self.cols = 1
        self.spacing = 10
        self.padding = 10
        
        grid = GridLayout(cols=2)
        
        left = GridLayout(cols=1)
        right = GridLayout(cols=1, size_hint=(0.25,1))
        
        left.add_widget(Label(text="Purchase Price:"))
        self.purchase_price = Label()
        right.add_widget(self.purchase_price)
        
        left.add_widget(Label(text="Total Costs:"))
        self.total_costs = Label()
        right.add_widget(self.total_costs)
        
        left.add_widget(Label(text="Loan Amount:"))
        self.loan_amount = Label()
        right.add_widget(self.loan_amount)
        
        left.add_widget(Label(text="Monthly Mortgage Payment:"))
        self.mortgage_payment = Label()
        right.add_widget(self.mortgage_payment)
        
        left.add_widget(Label(text="Gross Monthly Income:"))
        self.monthly_income = Label()
        right.add_widget(self.monthly_income)
        
        left.add_widget(Label(text="Approximate Monthly Expenses:"))
        self.monthly_expenses = Label()
        right.add_widget(self.monthly_expenses)
        
        left.add_widget(Label(text="Monthly Cashflow:"))
        self.monthly_cashflow = Label()
        right.add_widget(self.monthly_cashflow)
        
        left.add_widget(Label(text="Total Cash Needed:"))
        self.cash_needed = Label()
        right.add_widget(self.cash_needed)
        
        NOI_label = MyLabel(helptext='Annual Cashflow sans Mortgage Payments')
        NOI_label.text = 'Net Operating Income (NOI):'
        left.add_widget(NOI_label)
        self.NOI = Label()
        right.add_widget(self.NOI)
        
        cash_on_cash_ROI_label = MyLabel(helptext='Usually want to see 10-15%, unless there is a good reason to believe the property will appreciate substantially')
        cash_on_cash_ROI_label.text = 'Cash on Cash Return on Investment (ROI)'
        left.add_widget(cash_on_cash_ROI_label)
        self.cash_on_cash = Label()
        right.add_widget(self.cash_on_cash)
        
        monthly_cashflow_50pct_label = MyLabel(helptext='Assumes that half of the gross monthly income will go towards things other than the mortgage when evaluating cashflow potential')
        monthly_cashflow_50pct_label.text = 'Monthly Cashflow (50% Rule):'
        left.add_widget(monthly_cashflow_50pct_label)
        self.monthly_cashflow_50pct = Label()
        right.add_widget(self.monthly_cashflow_50pct)
        
        income_to_expense_label = MyLabel(helptext='The gross monthly income should be around 2% of the purchase cost')
        income_to_expense_label.text = 'Income/Expense Ratio (2% Rule):'
        left.add_widget(income_to_expense_label)
        self.income_to_expense = Label()
        right.add_widget(self.income_to_expense)

        grid.add_widget(left)   
        grid.add_widget(right) 
        
        self.add_widget(grid)

        # add buttons        
        self.make_summary = Button(text="Generate Financial Summary!", font_size=20, height=60, size_hint=(1,None))
        self.make_summary.bind(on_press = lambda x:self.summary_pressed(self, my_property))
        self.add_widget(self.make_summary)
        
        self.make_plots = Button(text="Generate Plots!", font_size=20, height=60, size_hint=(1,None))
        self.make_plots.bind(on_press = lambda x:self.plots_pressed(self, my_property))
        self.add_widget(self.make_plots)
        
    def clear_summary(self,instance):
        self.purchase_price.text = ''
        self.total_costs.text = ''
        self.loan_amount.text = ''
        self.mortgage_payment.text = ''
        self.monthly_income.text = ''
        self.monthly_expenses.text = ''
        self.monthly_cashflow.text = ''
        self.cash_needed.text = ''
        self.NOI.text = ''
        self.cash_on_cash.text = ''
        self.monthly_cashflow_50pct.text = ''
        self.income_to_expense.text = ''
        
    def summary_pressed(self, instance, RentalProperty):
        self.purchase_price.text = "${:,.2f}".format(RentalProperty.purchase_price)
        self.total_costs.text = "${:,.2f}".format(RentalProperty.purchase_price+RentalProperty.closing_costs+RentalProperty.repair_costs)
        self.loan_amount.text = "${:,.2f}".format(RentalProperty.loan_amount)
        self.mortgage_payment.text = "${:,.2f}".format(RentalProperty.mortgage_payment)
        self.monthly_income.text = "${:,.2f}".format(RentalProperty.gross_monthly_income)
        self.monthly_expenses.text = "${:,.2f}".format(RentalProperty.monthly_expenses)
        self.monthly_cashflow.text = "${:,.2f}".format(RentalProperty.monthly_cashflow)
        self.cash_needed.text = "${:,.2f}".format(RentalProperty.down_payment+RentalProperty.closing_costs+RentalProperty.repair_costs)
        self.NOI.text = "${:,.2f}".format(RentalProperty.net_operating_income)
        self.cash_on_cash.text = str(round(12*RentalProperty.monthly_cashflow/(RentalProperty.down_payment+RentalProperty.closing_costs+RentalProperty.repair_costs)*100,2))+'%'
        self.monthly_cashflow_50pct.text = "${:,.2f}".format(RentalProperty.gross_monthly_income-(0.5*RentalProperty.gross_monthly_income+RentalProperty.mortgage_payment))
        self.income_to_expense.text = str(round(RentalProperty.gross_monthly_income/RentalProperty.purchase_price*100,2))+'%'
        
    def plots_pressed(self, instance, RentalProperty):
        RentalProperty.plot_income()
        RentalProperty.plot_equity()
        plt.show()
        
class RentalInfoSimple(GridLayout):
    def __init__(self, my_property, **kwargs):
        super(RentalInfoSimple, self).__init__(**kwargs)
        
        self.cols=2
        left = GridLayout(cols=1)
        right = GridLayout(cols=1, width=100, size_hint=(None,1))
        
        left.add_widget(Label(text='Gross Monthly Rent:'))
        self.gross_rent = TextInput(multiline=False,text=str(2000))
        right.add_widget(self.gross_rent)
        
        left.add_widget(Label(text='Fixed Landlord Expenses:'))
        self.fixed_expenses = TextInput(multiline=False,text=str(150))
        right.add_widget(self.fixed_expenses)
        
        left.add_widget(Label(text='Variable Landlord Expenses:'))
        self.variable_expenses = TextInput(multiline=False,text=str(300))
        right.add_widget(self.variable_expenses)
        
        left.add_widget(Label(text='Rent Increase per Year (%):'))
        self.yearly_rent_increase = TextInput(multiline=False,text=str(2.0))
        right.add_widget(self.yearly_rent_increase)
        
        left.add_widget(Label(text='Expense Increase per Year (%):'))
        self.yearly_expense_increase = TextInput(multiline=False,text=str(2.0))
        right.add_widget(self.yearly_expense_increase)
        
        left.add_widget(Label(text='Property Appreciation per Year (%):'))
        self.yearly_appreciation = TextInput(multiline=False,text=str(2.0))
        right.add_widget(self.yearly_appreciation)
        
        self.calculate_cashflow = Button(text="Calculate Cashflow")
        self.calculate_cashflow.bind(on_press = lambda x:self.calculate_cashflow_pressed(self, my_property))
        self.monthly_cashflow = Label()
        left.add_widget(self.calculate_cashflow)
        right.add_widget(self.monthly_cashflow)
        
        self.add_widget(left)
        self.add_widget(right)
        
    def calculate_cashflow_pressed(self, instance, RentalProperty):
        RentalProperty.gross_monthly_income = float(self.gross_rent.text)
        RentalProperty.fixed_landlord_expenses = float(self.fixed_expenses.text)
        RentalProperty.variable_landlord_expenses = float(self.variable_expenses.text)
        RentalProperty.annual_percent_rent_increase = float(self.yearly_rent_increase.text)
        RentalProperty.annual_percent_expense_increase = float(self.yearly_expense_increase.text)
        RentalProperty.annual_percent_appreciation = float(self.yearly_appreciation.text)
        
        RentalProperty.calculate_cashflow()
        self.monthly_cashflow.text = str(round(RentalProperty.monthly_cashflow,2))