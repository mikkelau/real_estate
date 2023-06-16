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
        
        self.inside_left = GridLayout(cols=2)
        self.far_left = GridLayout(cols=1)
        self.center_left = GridLayout(cols=1, width=100, size_hint=(None,1))
                
        self.property_taxes_label = MyLabel(helptext='Typically publicly available on county assessor\'s website')
        self.property_taxes_label.text = 'Annual Property Taxes:'
        self.far_left.add_widget(self.property_taxes_label)
        self.property_taxes = TextInput(multiline=False,text=str(1600.00))
        self.center_left.add_widget(self.property_taxes)
        
        self.far_left.add_widget(Label(text='Purchase Price:'))
        self.purchase_price = TextInput(multiline=False,text=str(300000))
        self.center_left.add_widget(self.purchase_price)
        
        self.closing_costs_label = MyLabel(helptext='Typically $1500-$2500')
        self.closing_costs_label.text = 'Closing Costs:'
        self.far_left.add_widget(self.closing_costs_label)
        self.closing_costs = TextInput(multiline=False,text=str(2000.00))
        self.center_left.add_widget(self.closing_costs)
        
        self.far_left.add_widget(Label(text='Down Payment:'))
        self.down_payment = TextInput(multiline=False,text=str(20000))
        self.center_left.add_widget(self.down_payment)
        
        self.far_left.add_widget(Label(text='Interest Rate (%):'))
        self.interest_rate = TextInput(multiline=False,text=str(5.5))
        self.center_left.add_widget(self.interest_rate)
        
        self.far_left.add_widget(Label(text='Amortization Period (years):'))
        self.amort_period = TextInput(multiline=False,text=str(30))
        self.center_left.add_widget(self.amort_period)
        
        self.calculate_mortgage = Button(text="Calculate Mortgage")
        self.mortgage_payment = Label()
        self.calculate_mortgage.bind(on_press = lambda x:self.calculate_mortgage_pressed(self, my_property))
        self.far_left.add_widget(self.calculate_mortgage)
        self.center_left.add_widget(self.mortgage_payment)
        
        self.inside_left.add_widget(self.far_left)
        self.inside_left.add_widget(self.center_left)
        self.inside.add_widget(self.inside_left)

                
        self.inside_right = GridLayout(cols=2)
        self.center_right = GridLayout(cols=1)
        self.far_right = GridLayout(cols=1, width=100, size_hint=(None,1))
        
        self.center_right.add_widget(Label(text='Gross Monthly Rent:'))
        self.gross_rent = TextInput(multiline=False,text=str(2000))
        self.far_right.add_widget(self.gross_rent)
        
        self.center_right.add_widget(Label(text='Fixed Landlord Expenses:'))
        self.fixed_expenses = TextInput(multiline=False,text=str(150))
        self.far_right.add_widget(self.fixed_expenses)
        
        self.center_right.add_widget(Label(text='Variable Landlord Expenses:'))
        self.variable_expenses = TextInput(multiline=False,text=str(300))
        self.far_right.add_widget(self.variable_expenses)
        
        self.center_right.add_widget(Label(text='Rent Increase per Year (%):'))
        self.yearly_rent_increase = TextInput(multiline=False,text=str(2.0))
        self.far_right.add_widget(self.yearly_rent_increase)
        
        self.center_right.add_widget(Label(text='Expense Increase per Year (%):'))
        self.yearly_expense_increase = TextInput(multiline=False,text=str(2.0))
        self.far_right.add_widget(self.yearly_expense_increase)
        
        self.center_right.add_widget(Label(text='Property Appreciation per Year (%):'))
        self.yearly_appreciation = TextInput(multiline=False,text=str(2.0))
        self.far_right.add_widget(self.yearly_appreciation)
        
        self.calculate_cashflow = Button(text="Calculate Cashflow")
        self.calculate_cashflow.bind(on_press = lambda x:self.calculate_cashflow_pressed(self, my_property))
        self.monthly_cashflow = Label()
        self.center_right.add_widget(self.calculate_cashflow)
        self.far_right.add_widget(self.monthly_cashflow)
        
        self.inside_right.add_widget(self.center_right)
        self.inside_right.add_widget(self.far_right)
        self.inside.add_widget(self.inside_right)

        self.add_widget(self.inside)
        
        self.make_plots = Button(text="Make Plots!", font_size=40, height=100, size_hint=(1,None))
        self.make_plots.bind(on_press = lambda x:self.plot_pressed(self, my_property))
        self.add_widget(self.make_plots)
        
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
        
    def calculate_cashflow_pressed(self, instance, RentalProperty):
        RentalProperty.gross_monthly_income = float(self.gross_rent.text)
        RentalProperty.fixed_landlord_expenses = float(self.fixed_expenses.text)
        RentalProperty.variable_landlord_expenses = float(self.variable_expenses.text)
        RentalProperty.annual_percent_rent_increase = float(self.yearly_rent_increase.text)
        RentalProperty.annual_percent_expense_increase = float(self.yearly_expense_increase.text)
        RentalProperty.annual_percent_appreciation = float(self.yearly_appreciation.text)
        
        RentalProperty.calculate_cashflow()
        self.monthly_cashflow.text = str(round(RentalProperty.monthly_cashflow,2))
        
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