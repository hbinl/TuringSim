"""
@title FIT3140 Assignment 5
@description Sprint 2
@author Loh Hao Bin, Ashley Ong Yik Mun, Varshinee Devi Servansingh
@date 17/10/2015
"""
import kivy
kivy.require('1.9.0')
from kivy.app import App
from ui_container import Container

class TuringSimApp(App):
    def build(self):
        return Container()

if __name__ == "__main__":
    TuringSimApp().run()
