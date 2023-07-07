# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 07:40:18 2023

@author: mikke
"""
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from re_grid import PropertyInfo, FinancialSummary
# from re_grid import RentalInfoSimple as RentalInfo
from re_grid import RentalInfo
from rentalproperty import RentalProperty

class RE_Tabs(TabbedPanel):
    def __init__(self, **kwargs):
        super(RE_Tabs, self).__init__(**kwargs)
        
        self.pos_hint={'center_x': .5, 'center_y': .5}
        self.do_default_tab = False
        self.tab_width = None
        
        # initialize the RentalProperty class instance
        my_property = RentalProperty()
        
        # make some lists
        name_list = ['Property/Loan Info', 'Rental Info', 'Financials & Plots']
        self.content_list = [PropertyInfo(my_property), RentalInfo(my_property), FinancialSummary(my_property)]
        tabs = [None]*3
        
        for i in range(len(tabs)):
            tabs[i] = TabbedPanelItem(text=name_list[i])
            tabs[i].padding = (10,0)
            tabs[i].texture_update()
            tabs[i].width = tabs[i].texture_size[0]
            tabs[i].size_hint_x = None
            tabs[i].add_widget(self.content_list[i])
            
        self.content_list[0].property_taxes.bind(text=lambda instance, x:self.update_property_taxes(self))
        self.content_list[0].mortgage_payment.bind(text=lambda instance, x:self.update_property_taxes(self))
        self.update_property_taxes(self)
        
        self.content_list[1].monthly_cashflow.bind(text=lambda instance, x:self.content_list[2].clear_summary(self.content_list[2]))

        for tab in tabs:
            self.add_widget(tab)
        
    def update_property_taxes(self, instance):
        # Update the monthly property tax text when annual property tax changes
        if self.content_list[0].property_taxes.text == '':
            self.content_list[1].property_taxes = 0
        else:
            self.content_list[1].property_taxes = float(self.content_list[0].property_taxes.text)/12
        self.content_list[1].property_taxes_text.text = "${:,.2f}".format(self.content_list[1].property_taxes)
            
        # update estimation of fixed expenses with new property tax value. This also clears cashflow estimate
        self.content_list[1].update_fixed_expenses(self.content_list[1])