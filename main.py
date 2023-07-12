# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 20:51:57 2022

@author: mikke
"""
from kivy.app import App
from kivy.core.window import Window
from re_grid import RE_Grid  
from re_tabs import RE_Tabs

# Window.size = (400, Window.size[1])
        
class RE_App(App):
    def build(self):
        # return RE_Grid()
        return RE_Tabs()

if __name__ == "__main__":
   # main()
   RE_App().run()
   Window.close()
   
