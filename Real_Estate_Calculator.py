# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 20:51:57 2022

@author: mikke
"""
# from kivy.config import Config
# Config.set('kivy','keyboard_mode','systemanddock')
from kivy.core.window import Window
from kivy.app import App
from re_grid import RE_Grid  
        
class RE_App(App):
    def build(self):
        return RE_Grid()

if __name__ == "__main__":
   # main()
   RE_App().run()
   Window.close()
   
