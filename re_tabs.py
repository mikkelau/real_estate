# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 07:40:18 2023

@author: mikke
"""
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from re_grid import PropertyInfo
from rentalproperty import RentalProperty

class RE_Tabs(TabbedPanel):
    def __init__(self, **kwargs):
        super(RE_Tabs, self).__init__(**kwargs)
        
        self.pos_hint={'center_x': .5, 'center_y': .5}
        self.do_default_tab = False
        
        # initialize the RentalProperty class instance
        my_property = RentalProperty()
        
        tab1 = TabbedPanelItem(text='Property/Loan Info')
        tab1_content = PropertyInfo(my_property)
        tab1.add_widget(tab1_content)
        
        tab2 = TabbedPanelItem(text='Rental Info')
        
        tab3 = TabbedPanelItem(text='Financials & Plots')
        
        self.add_widget(tab1)
        self.add_widget(tab2)
        self.add_widget(tab3)
        
