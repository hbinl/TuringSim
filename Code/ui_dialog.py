"""
@title FIT3140 Assignment 5
@description Sprint 1
@author Loh Hao Bin, Ashley Ong Yik Mun, Varshinee Devi Servansingh
@date 1/9/2015
"""
# Kivy Dependencies
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.factory import Factory
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.graphics import *
from kivy.uix.label import Label
from kivy.graphics.transformation import Matrix
from kivy.animation import Animation
import os
import xml.etree.ElementTree as ET

class HomeScreenWindow(FloatLayout):
    """
    @purpose A FloatLayout for implementing Load file dialogs
    """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = None
    string = "TuringSim v0.3\n" +\
    "Developed by Loh Hao Bin, Ashley Ong Yik Mun & Varshinee Servansingh \n" +\
    "FIT3140 Advanced Programming, Semester 2, 2015\n\n" +\
    "TuringSim supports loading and saving programs, executing, stepping, and creating custom programs.\n"+\
    "TuringSim supports deterministic and non-deterministic Turing Machines. \n\n" +\
    "Please select one of the option below to proceed."



class SaveFileChooserWindow(FloatLayout):
    """
    @purpose A FloatLayout for implementing Save file dialogs
    """
    save = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = None


class BrowseFileChooserWindow(FloatLayout):
    """
    @purpose A FloatLayout for implementing Load file dialogs
    """
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    path = None

    def load_file(self, path, filename):
        # saving the path into this object for future use

        self.path = os.path.join(path,filename[0])
        self.cancel_dialog()

    def cancel_dialog(self):
        # used for dismissing the dialog box
        self.parent.parent.parent.dismiss()







