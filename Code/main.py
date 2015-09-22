"""
@title FIT3140 Assignment 5
@description Sprint 1


@author Loh Hao Bin, Ashley Ong Yik Mun, Varshinee Devi Servansingh
@date 1/9/2015
"""

# Kivy Dependencies
from kivy.app import App
from ui_container import Container


class TuringSimApp(App):
    def build(self):
        return Container()

if __name__ == "__main__":
    TuringSimApp().run()
