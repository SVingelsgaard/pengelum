import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.properties import NumericProperty
from kivy.properties import ListProperty
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.text import Label
from kivy.graphics import Line

import numpy as np
import matplotlib.pyplot as plt

import time

#window settings
Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics', 'fullscreen', '1')


class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class Pengelum(Image):
    xPos = NumericProperty(0)
    yPos = NumericProperty(0)
    angle = NumericProperty(10)

#load kv file
kv = Builder.load_file("frontend/main.kv")

class GUI(App):
    
    def on_start(self): #variables
        #system variables
        self.setCYCLETIME = 0.02
        self.runTime = 0

        #program variables
        self.slider = self.root.get_screen('mainScreen').ids.slider
        self.pengelum = self.root.get_screen('mainScreen').ids.pengelum

    #continus cycle
    def cycle(self, readCYCLETIME):
        if self.runTime != 0 and self.runTime < .03:
            time.sleep(1)

        self.pengelum.xPos = self.slider.value
        
        self.runTime += readCYCLETIME

    #runns cycle
    def runApp(self):
        Clock.schedule_interval(self.cycle, self.setCYCLETIME)


    #runs myApp(graphics)
    def build(self):
        return kv

#runs program and cycle
if __name__ == '__main__':
    GUI().run()