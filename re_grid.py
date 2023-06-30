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
        right = GridLayout(cols=1, width=100, size_hint=(None,1))
                
        self.property_taxes_label = MyLabel(helptext='Typically publicly available on county assessor\'s website')
        self.property_taxes_label.text = 'Annual Property Taxes:'
        left.add_widget(self.property_taxes_label)
        self.property_taxes = TextInput(multiline=False,text=str(1600.00))
        right.add_widget(self.property_taxes)
        
        left.add_widget(Label(text='Purchase Price:'))
        self.purchase_price = TextInput(multiline=False,text=str(300000))
        right.add_widget(self.purchase_price)
        
        self.closing_costs_label = MyLabel(helptext='Typically $1500-$2500')
        self.closing_costs_label.text = 'Closing Costs:'
        left.add_widget(self.closing_costs_label)
        self.closing_costs = TextInput(multiline=False,text=str(2000.00))
        right.add_widget(self.closing_costs)
        
        left.add_widget(Label(text='Down Payment:'))
        self.down_payment = TextInput(multiline=False,text=str(20000))
        right.add_widget(self.down_payment)
        
        left.add_widget(Label(text='Interest Rate (%):'))
        self.interest_rate = TextInput(multiline=False,text=str(5.5))
        right.add_widget(self.interest_rate)
        
        left.add_widget(Label(text='Amortization Period (years):'))
        self.amort_period = TextInput(multiline=False,text=str(30))
        right.add_widget(self.amort_period)
        
        self.calculate_mortgage = Button(text="Calculate Mortgage")
        self.mortgage_payment = Label()
        self.calculate_mortgage.bind(on_press = lambda x:self.calculate_mortgage_pressed(self, my_property))
        left.add_widget(self.calculate_mortgage)
        right.add_widget(self.mortgage_payment)
        
        self.add_widget(left)
        self.add_widget(right)
        
    def calculate_mortgage_pressed(self, instance, RentalProperty):
        # set the variables in the class using the text inputs
        RentalProperty.prop_taxes = float(self.property_taxes.text)
        RentalProperty.purchase_price = float(self.purchase_price.text)
        RentalProperty.closing_costs = float(self.closing_costs.text)
        RentalProperty.down_payment = float(self.down_payment.text)
        RentalProperty.interest_rate = float(self.interest_rate.text)
        RentalProperty.amortization_period = int(self.amort_period.text)
        
        RentalProperty.calculate_mortgage_payment()
        self.mortgage_payment.text = str(round(RentalProperty.mortgage_payment,2))
        
class RentalInfo(GridLayout):
    def __init__(self, my_property, **kwargs):
        super(RentalInfo, self).__init__(**kwargs)
        
        self.cols=2
        self.spacing = 10
        self.padding = 10
        left = GridLayout(cols=1)
        right = GridLayout(cols=1, width=100, size_hint=(None,1))
        
        left.add_widget(Label(text='Gross Monthly Rent:'))
        self.gross_rent = TextInput(multiline=False,text=str(2000))
        right.add_widget(self.gross_rent)
        self.gross_rent.bind(text=lambda instance, x:self.update_vacancy_cost(self))
        self.gross_rent.bind(text=lambda instance, x:self.update_maintenance_cost(self))
        self.gross_rent.bind(text=lambda instance, x:self.update_capex_cost(self))
        self.gross_rent.bind(text=lambda instance, x:self.update_managementfees_cost(self))
        
        self.monthly_cashflow = Label()
        
        self.fixed_expenses_label = MyLabel(helptext='Expenses that are predictable or paid every month')
        self.fixed_expenses_label.text = 'Fixed Landlord Expenses:'
        left.add_widget(self.fixed_expenses_label)
        self.total_fixed_expenses = Label()
        right.add_widget(self.total_fixed_expenses)
        
        self.services_label = MyLabel(helptext='Electricity, Water, Gas, Sewer, Garbage, etc.')
        self.services_label.text = 'Services/Utilities:'
        left.add_widget(self.services_label)
        self.services_expenses = TextInput(multiline=False,text=str(150))
        right.add_widget(self.services_expenses)
        
        left.add_widget(Label(text='HOA:'))
        self.hoa_expenses = TextInput(multiline=False,text=str(0))
        right.add_widget(self.hoa_expenses)
        
        left.add_widget(Label(text='Home Owner''s Insurance:'))
        self.home_insurance = TextInput(multiline=False,text=str(100))
        right.add_widget(self.home_insurance)
        
        self.property_taxes_label = MyLabel(helptext='Previously calculated')
        self.property_taxes_label.text = 'Property Taxes:'
        left.add_widget(self.property_taxes_label)
        self.property_taxes = Label()
        right.add_widget(self.property_taxes)
        
        self.other_expenses_label = MyLabel(helptext='Snow removal, lawn care, flood insurance, etc.')
        self.other_expenses_label.text = 'Other:'
        left.add_widget(self.other_expenses_label)
        self.other_expenses = TextInput(multiline=False,text=str(0))
        right.add_widget(self.other_expenses)
        
        self.variable_expenses_label = MyLabel(helptext='Expenses that occur unexpectedly')
        self.variable_expenses_label.text = 'Variable Landlord Expenses:'
        left.add_widget(self.variable_expenses_label)
        self.total_variable_expenses = Label()
        right.add_widget(self.total_variable_expenses)
        
        vacancy = GridLayout(cols=2)
        self.vacancy_label = MyLabel(helptext = 'Typically 3-7% of rental income depending on desirability and location')
        self.vacancy_label.text = 'Vacancy (%)'
        vacancy.add_widget(self.vacancy_label)
        self.vacancy_percentage = TextInput(multiline=False,text=str(5))
        vacancy.add_widget(self.vacancy_percentage)
        left.add_widget(vacancy)
        self.vacancy_cost = Label()
        self.update_vacancy_cost(self)
        self.vacancy_percentage.bind(text=lambda instance, x:self.update_vacancy_cost(self))
        right.add_widget(self.vacancy_cost)
        
        maintenance = GridLayout(cols=2)
        self.maintenance_label = MyLabel(helptext='Typically 5-10% of rental income depending on age of the unit')
        self.maintenance_label.text = 'Repairs & Maintenance (%)'
        maintenance.add_widget(self.maintenance_label)
        self.maintenance_percentage = TextInput(multiline=False,text=str(7))
        maintenance.add_widget(self.maintenance_percentage)
        left.add_widget(maintenance)
        self.maintenance_cost = Label()
        self.update_maintenance_cost(self)
        self.maintenance_percentage.bind(text=lambda instance, x:self.update_maintenance_cost(self))
        right.add_widget(self.maintenance_cost)
        
        capex = GridLayout(cols=2)
        self.capex_label = MyLabel(helptext='Big expenses that need to be saved up for (windows, roof, appliances, plumbing, etc). Typically 5-10% of rental income.')
        self.capex_label.text = 'Capital Expenditures (%)'
        capex.add_widget(self.capex_label)
        self.capex_percentage = TextInput(multiline=False,text=str(7))
        capex.add_widget(self.capex_percentage)
        left.add_widget(capex)
        self.capex_cost = Label()
        self.update_capex_cost(self)
        self.capex_percentage.bind(text=lambda instance, x:self.update_capex_cost(self))
        right.add_widget(self.capex_cost)
        
        managementfees = GridLayout(cols=2)
        self.managementfees_label = MyLabel(helptext='Typically 10% of rental income.')
        self.managementfees_label.text = 'Management Fees (%)'
        managementfees.add_widget(self.managementfees_label)
        self.managementfees_percentage = TextInput(multiline=False,text=str(7))
        managementfees.add_widget(self.managementfees_percentage)
        left.add_widget(managementfees)
        self.managementfees_cost = Label()
        self.update_managementfees_cost(self)
        self.managementfees_percentage.bind(text=lambda instance, x:self.update_managementfees_cost(self))
        right.add_widget(self.managementfees_cost)
        
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
        left.add_widget(self.calculate_cashflow)
        right.add_widget(self.monthly_cashflow)
        
        self.add_widget(left)
        self.add_widget(right)
        
    def update_vacancy_cost(self, instance):
        if (self.vacancy_percentage.text == '') or (self.gross_rent.text == ''):
            self.vacancy_cost.text = str(round(float(0)))
        else:
            self.vacancy_cost.text = str(round(float(self.gross_rent.text)*float(self.vacancy_percentage.text)/100))
        self.monthly_cashflow.text = ''
            
    def update_maintenance_cost(self, instance):
        if (self.maintenance_percentage.text == '') or (self.gross_rent.text == ''):
            self.maintenance_cost.text = str(round(float(0)))
        else:
            self.maintenance_cost.text = str(round(float(self.gross_rent.text)*float(self.maintenance_percentage.text)/100))
        self.monthly_cashflow.text = ''
            
    def update_capex_cost(self, instance):
        if (self.capex_percentage.text == '') or (self.gross_rent.text == ''):
            self.capex_cost.text = str(round(float(0)))
        else:
            self.capex_cost.text = str(round(float(self.gross_rent.text)*float(self.capex_percentage.text)/100))
        self.monthly_cashflow.text = ''
            
    def update_managementfees_cost(self, instance):
        if (self.managementfees_percentage.text == '') or (self.gross_rent.text == ''):
            self.managementfees_cost.text = str(round(float(0)))
        else:
            self.managementfees_cost.text = str(round(float(self.gross_rent.text)*float(self.managementfees_percentage.text)/100))
        self.monthly_cashflow.text = ''
        
    def calculate_cashflow_pressed(self, instance, RentalProperty):
        RentalProperty.gross_monthly_income = float(self.gross_rent.text)
        RentalProperty.fixed_landlord_expenses = sum([float(self.services_expenses.text), float(self.hoa_expenses.text),
                                                      float(self.home_insurance.text), RentalProperty.prop_taxes/12,
                                                      float(self.other_expenses.text)])
        RentalProperty.variable_landlord_expenses = sum([float(self.vacancy_cost.text), float(self.maintenance_cost.text),
                                                         float(self.capex_cost.text), float(self.managementfees_cost.text)])
        RentalProperty.annual_percent_rent_increase = float(self.yearly_rent_increase.text)
        RentalProperty.annual_percent_expense_increase = float(self.yearly_expense_increase.text)
        RentalProperty.annual_percent_appreciation = float(self.yearly_appreciation.text)
        
        RentalProperty.calculate_cashflow()
        self.monthly_cashflow.text = str(round(RentalProperty.monthly_cashflow,2))
        self.total_fixed_expenses.text = str(round(RentalProperty.fixed_landlord_expenses,2))
        self.total_variable_expenses.text = str(round(RentalProperty.variable_landlord_expenses,2))
        
class FinancialSummary(GridLayout):
    def __init__(self, my_property, **kwargs):
        super(FinancialSummary, self).__init__(**kwargs)
        
        self.cols = 1
        self.spacing = 10
        self.padding = 10
        
        grid = GridLayout(cols=2)
        
        grid.add_widget(Label(text="Purchase Price:"))
        self.purchase_price = Label()
        grid.add_widget(self.purchase_price)
        
        grid.add_widget(Label(text="Total Costs:"))
        self.total_costs = Label()
        grid.add_widget(self.total_costs)
        
        grid.add_widget(Label(text="Loan Amount:"))
        self.loan_amount = Label()
        grid.add_widget(self.loan_amount)
        
        grid.add_widget(Label(text="Monthly Mortgage Payment:"))
        self.mortgage_payment = Label()
        grid.add_widget(self.mortgage_payment)
        
        grid.add_widget(Label(text="Gross Monthly Income:"))
        self.monthly_income = Label()
        grid.add_widget(self.monthly_income)
        
        grid.add_widget(Label(text="Approximate Monthly Expenses:"))
        self.monthly_expenses = Label()
        grid.add_widget(self.monthly_expenses)
        
        grid.add_widget(Label(text="Monthly Cashflow:"))
        self.monthly_cashflow = Label()
        grid.add_widget(self.monthly_cashflow)
        
        grid.add_widget(Label(text="Total Cash Needed:"))
        self.cash_needed = Label()
        grid.add_widget(self.cash_needed)
        
        NOI_label = MyLabel(helptext='Annual Cashflow sans Mortgage Payments')
        NOI_label.text = 'Net Operating Income (NOI):'
        grid.add_widget(NOI_label)
        self.NOI = Label()
        grid.add_widget(self.NOI)
        
        cash_on_cash_ROI_label = MyLabel(helptext='Usually want to see 10-15%, unless there is a good reason to believe the property will appreciate substantially')
        cash_on_cash_ROI_label.text = 'Cash on Cash Return on Investment (ROI)'
        grid.add_widget(cash_on_cash_ROI_label)
        self.cash_on_cash = Label()
        grid.add_widget(self.cash_on_cash)
        
        monthly_cashflow_50pct_label = MyLabel(helptext='Assumes that half of the gross monthly income will go towards things other than the mortgage when evaluating cashflow potential')
        monthly_cashflow_50pct_label.text = 'Monthly Cashflow (50% Rule):'
        grid.add_widget(monthly_cashflow_50pct_label)
        self.monthly_cashflow_50pct = Label()
        grid.add_widget(self.monthly_cashflow_50pct)
        
        income_to_expense_label = MyLabel(helptext='The gross monthly income should be around 2% of the purchase cost')
        income_to_expense_label.text = 'Income/Expense Ratio (2% Rule):'
        grid.add_widget(income_to_expense_label)
        self.income_to_expense = Label()
        grid.add_widget(self.income_to_expense)

        self.add_widget(grid)        
        
        self.make_summary = Button(text="Generate Financial Summary!", font_size=40, height=100, size_hint=(1,None))
        self.make_summary.bind(on_press = lambda x:self.summary_pressed(self, my_property))
        self.add_widget(self.make_summary)
        
    def summary_pressed(self, instance, RentalProperty):
        self.purchase_price.text = str(round(RentalProperty.purchase_price))
        self.total_costs.text = str(round(RentalProperty.purchase_price+RentalProperty.closing_costs))
        self.loan_amount.text = str(round(RentalProperty.loan_amount))
        self.mortgage_payment.text=str(round(RentalProperty.mortgage_payment))
        self.monthly_income.text = str(round(RentalProperty.gross_monthly_income))
        self.monthly_expenses.text = str(round(RentalProperty.monthly_expenses))
        self.monthly_cashflow.text = str(round(RentalProperty.monthly_cashflow))
        self.cash_needed.text = str(round(RentalProperty.down_payment+RentalProperty.closing_costs))
        self.NOI.text = str(round(RentalProperty.net_operating_income))
        self.cash_on_cash.text = str(round(12*RentalProperty.monthly_cashflow/(RentalProperty.down_payment+RentalProperty.closing_costs)*100))+'%'
        self.monthly_cashflow_50pct.text = str(round(RentalProperty.gross_monthly_income-(0.5*RentalProperty.gross_monthly_income+RentalProperty.mortgage_payment)))
        self.income_to_expense.text = str(round(RentalProperty.gross_monthly_income/RentalProperty.purchase_price*100,2))+'%'

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
