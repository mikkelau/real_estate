# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 07:40:18 2023

@author: mikke
"""
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from re_grid import PropertyInfo
# from re_grid import RentalInfoSimple as RentalInfo
from re_grid import RentalInfo
from rentalproperty import RentalProperty

class RE_Tabs(TabbedPanel):
    def __init__(self, **kwargs):
        super(RE_Tabs, self).__init__(**kwargs)
        
        self.pos_hint={'center_x': .5, 'center_y': .5}
        self.do_default_tab = False
        
        # initialize the RentalProperty class instance
        my_property = RentalProperty()
        
        tab1 = TabbedPanelItem(text='Property/Loan Info')
        self.tab1_content = PropertyInfo(my_property)
        tab1.add_widget(self.tab1_content)
        
        tab2 = TabbedPanelItem(text='Rental Info')
        self.tab2_content = RentalInfo(my_property)
        self.update_property_taxes(self,my_property)
        tab2.add_widget(self.tab2_content)
        
        self.tab1_content.property_taxes.bind(text=lambda instance, x:self.update_property_taxes(self,my_property))
        
        tab3 = TabbedPanelItem(text='Financials & Plots')
        
        self.add_widget(tab1)
        self.add_widget(tab2)
        self.add_widget(tab3)
        
    def update_property_taxes(self, instance, RentalProperty):
        # Update the label's text when the variable changes
        if self.tab1_content.property_taxes.text == '':
            RentalProperty.prop_taxes = 0.0
        else:
            RentalProperty.prop_taxes = float(self.tab1_content.property_taxes.text)
            
        self.tab2_content.property_taxes.text = str(round(RentalProperty.prop_taxes/12,2))
        self.tab2_content.monthly_cashflow.text = ''
