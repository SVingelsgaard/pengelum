from doctest import master
from operator import length_hint
import string
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.clock import Clock
from kivy.config import Config
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import NumericProperty
from kivy.properties import ListProperty, StringProperty
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg


from kivy.graphics import Line


import numpy as np
import matplotlib.pyplot as plt
import time

#window settings
"""Config.set('graphics', 'window_state', 'maximized')
Config.set('graphics', 'fullscreen', '1')"""


class WindowManager(ScreenManager):
    pass

class StartScreen(Screen):
    pass

class MainScreen(Screen):
    pass

class Envirement(FloatLayout):
    g = NumericProperty(-9.81/10)#m/s^2
    M = NumericProperty(10)# how manny pixels in a meter


class Output(Label):
    text = StringProperty("0.0")
    
class Pengelum(Image):
    #for graphics
    xPos = NumericProperty(0)#px
    yPos = NumericProperty(0)#px
    angleDegrees = NumericProperty(0)
    

    #for math shit
    theta = NumericProperty(.99*np.pi)
    L = NumericProperty(15)#length of pengelum. In meters on screen(.06). 325px(to the center of the blub)
    xx = NumericProperty(0.0)#distance of arc form 0deg to pengelum. In meters 
    rotAcc = NumericProperty(0.0)#gravety in the direction of rotation
    rotVel = NumericProperty(0.0)

class Graph(FigureCanvasKivyAgg):
    def __init__(self, **kwargs):
        super().__init__(plt.gcf(), **kwargs)

class GUI(App):
    
    def on_start(self): #variables
        #system variables
        self.setCYCLETIME = 0.02
        self.readCYCLETIME = 0
        self.runTime = 0
        self.env = self.root.get_screen('mainScreen').ids.env

        #program variables
        self.slider = self.root.get_screen('mainScreen').ids.slider
        self.sliderAcc = 0
        self.sliderLast = 0
        self.pengelum = self.root.get_screen('mainScreen').ids.pengelum

        self.output = self.root.get_screen('mainScreen').ids.output

        #graph variables
        self.y = [0,1,2]
        self.x = [0,1,2]
        self.y2 = []

        plt.title("pengelum angle")
        plt.xlabel("t")
        plt.ylabel("angle")
        plt.plot(self.x,self.y)
        


    #continus cycle
    def cycle(self, readCYCLETIME):
        self.readCYCLETIME = readCYCLETIME
        if self.runTime != 0 and self.runTime < .03:
            time.sleep(1)


        self.mafs()



        #graph
        self.x.append(self.runTime)
        self.y2.append(self.pengelum.rotAcc)
        self.y.append(float(self.output.text))
        


        #update grapics
        self.pengelum.angleDegrees = float(np.degrees(self.pengelum.theta))
        self.pengelum.xPos = self.slider.value

        self.runTime += readCYCLETIME 





    def mafs(self):
        self.pengelum.xx = self.pengelum.L * self.pengelum.theta#calc x. do not thik i need it

        if (self.pengelum.theta <.5*np.pi) and (self.pengelum.theta > -.5*np.pi):
            self.sliderAcc = float(((self.slider.value - self.sliderLast)*np.sin(self.pengelum.theta))*self.setCYCLETIME*(1/self.pengelum.L))#constant to get right dim maby. 
        else:
            self.sliderAcc = float(((self.slider.value - self.sliderLast)*np.cos(self.pengelum.theta))*self.setCYCLETIME)#constant to get right dim maby. 

        self.output.text = str((self.pengelum.theta/np.pi))



        self.pengelum.rotAcc = (float((self.env.g/self.pengelum.L) * np.sin(self.pengelum.theta)))-(self.pengelum.rotVel * .01)-self.sliderAcc

        self.pengelum.rotVel += self.pengelum.rotAcc



        

        
        
        
        
        
        self.sliderLast = self.slider.value


        self.pengelum.theta += self.pengelum.rotVel * self.readCYCLETIME

    def showGraph(self):
        
        print(self.x)

    #runns cycle
    def runApp(self):
        Clock.schedule_interval(self.cycle, self.setCYCLETIME)

    #runs myApp(graphics)
    def build(self):
        return Builder.load_file("frontend/main.kv")

#runs program and cycle
if __name__ == '__main__':
    GUI().run()