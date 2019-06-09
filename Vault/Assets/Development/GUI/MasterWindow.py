import kivy
kivy.require("1.10.1")

import cProfile

from kivy.app import App
from kivy.lang import Builder
from kivy.graphics.instructions import InstructionGroup
from kivy.uix.colorpicker import Color
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.slider import Slider

from kivy.uix.actionbar import ActionBar
from kivy.uix.actionbar import ActionItem
from kivy.uix.actionbar import ActionSeparator
from kivy.uix.actionbar import ActionOverflow

from HoverEvent import HoverEvent

from kivy.properties import ObjectProperty, StringProperty



class MasterWindow(FloatLayout):
  def __init__(self):
    super(MasterWindow, self).__init__()